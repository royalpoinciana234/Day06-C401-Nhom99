"""
AI triage orchestrator. Called by main.py /chat endpoint.
Flow: injection_check → safety_gate → classify → factual_answer | advisory_gather | advisory_handoff
"""

import openrouter_client as llm
import prompts
from chat_log import log_handoff
from longchau_search import search_products
from safety_gate import is_high_risk, is_injection

PHARMACIST_NAMES = ["Dược sĩ Lan", "Dược sĩ Minh", "Dược sĩ Hương"]
_pharmacist_index = 0


def _next_pharmacist() -> str:
    global _pharmacist_index
    name = PHARMACIST_NAMES[_pharmacist_index % len(PHARMACIST_NAMES)]
    _pharmacist_index += 1
    return name



def _format_product_links(products: list[dict]) -> str:
    if not products:
        return ""
    lines = ["\n\n---\n🛒 **Sản phẩm tại Long Châu:**"]
    for p in products:
        lines.append(f"• [{p['name']}]({p['url']}) — {p['price']}")
    return "\n".join(lines)


async def triage(message: str, history: list[dict]) -> dict:
    model_name = llm.get_model_name()

    # 0. Injection detected: don't block — let LLM handle via _ANTI_INJECTION in system prompts.
    # The system prompt already instructs the model to ignore off-topic parts and only answer
    # the pharmacy-relevant portion. Blocking here would also reject legitimate drug questions
    # that happen to contain injection patterns (e.g. "bromhexin info AND write python code").
    injection_detected = is_injection(message)
    _ = injection_detected  # reserved for future logging/metrics

    # 1. Safety gate — always runs first, overrides classifier
    if is_high_risk(message):
        try:
            summary_messages = [
                {"role": "system", "content": prompts.HANDOFF_SUMMARY_SYSTEM},
                *history,
                {"role": "user", "content": message},
            ]
            handoff_summary = await llm.chat(summary_messages)
        except Exception:
            handoff_summary = f"Khách hỏi: {message[:200]}. Cần tư vấn chuyên sâu."

        pharmacist = _next_pharmacist()
        log_handoff(message, history, handoff_summary, pharmacist, safety_triggered=True)
        return {
            "route": "advisory_handoff",
            "reply": f"⚠️ Câu hỏi của bạn liên quan đến tình trạng sức khoẻ cụ thể và cần được tư vấn bởi chuyên gia.\n\nĐang chuyển cho **{pharmacist}** hỗ trợ bạn ngay.",
            "handoff_summary": handoff_summary,
            "safety_gate_triggered": True,
            "model": model_name,
        }

    # 2. Classify
    try:
        classify_messages = [
            {"role": "system", "content": prompts.CLASSIFIER_SYSTEM},
            *history,
            {"role": "user", "content": message},
        ]
        classification = await llm.chat_json(classify_messages)
        question_type = classification.get("type", "advisory")
        needs_context = classification.get("needs_context", True)
        drug_keyword = classification.get("drug_keyword") or None
    except Exception:
        # Fail safe: unknown → advisory
        question_type = "advisory"
        needs_context = True
        drug_keyword = None

    # 3a. Factual → answer + product links in parallel (only when a drug keyword exists)
    if question_type == "factual":
        import asyncio

        answer_messages = [
            {"role": "system", "content": prompts.FACTUAL_ANSWER_SYSTEM},
            *history,
            {"role": "user", "content": message},
        ]

        if drug_keyword:
            try:
                reply, products = await asyncio.gather(
                    llm.chat(answer_messages),
                    search_products(drug_keyword, max_results=3),
                )
            except Exception:
                reply = "Xin lỗi, không thể tải thông tin lúc này. Vui lòng thử lại hoặc hỏi dược sĩ trực tiếp."
                products = []
        else:
            try:
                reply = await llm.chat(answer_messages)
            except Exception:
                reply = "Xin lỗi, không thể tải thông tin lúc này. Vui lòng thử lại hoặc hỏi dược sĩ trực tiếp."
            products = []

        product_md = _format_product_links(products)
        return {
            "route": "factual",
            # reply_md: for text-based UIs (Streamlit) that render markdown
            # reply: clean text for widget (uses structured `products` field)
            "reply": reply,
            "reply_md": reply + product_md,
            "products": products,
            "handoff_summary": None,
            "safety_gate_triggered": False,
            "model": model_name,
        }

    # 3b. Advisory + needs context → ask follow-up
    if needs_context:
        try:
            gather_messages = [
                {"role": "system", "content": prompts.GATHER_CONTEXT_SYSTEM},
                *history,
                {"role": "user", "content": message},
            ]
            reply = await llm.chat(gather_messages)
        except Exception:
            reply = "Để tư vấn chính xác hơn, bạn có thể cho tôi biết bạn đang điều trị bệnh gì và có đang dùng thuốc nào khác không?"

        return {
            "route": "advisory_gather",
            "reply": reply,
            "handoff_summary": None,
            "safety_gate_triggered": False,
            "model": model_name,
        }

    # 3c. Advisory + enough context → handoff summary
    try:
        summary_messages = [
            {"role": "system", "content": prompts.HANDOFF_SUMMARY_SYSTEM},
            *history,
            {"role": "user", "content": message},
        ]
        handoff_summary = await llm.chat(summary_messages)
    except Exception:
        handoff_summary = f"Khách hỏi: {message[:200]}. Cần tư vấn chuyên sâu."

    pharmacist = _next_pharmacist()
    log_handoff(message, history, handoff_summary, pharmacist, safety_triggered=False)
    return {
        "route": "advisory_handoff",
        "reply": f"Cảm ơn bạn đã cung cấp thông tin. Đang chuyển cho **{pharmacist}** tư vấn chi tiết cho bạn.",
        "handoff_summary": handoff_summary,
        "safety_gate_triggered": False,
        "model": model_name,
    }
