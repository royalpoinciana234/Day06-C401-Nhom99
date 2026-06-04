"""
AI triage orchestrator. Called by main.py /chat endpoint.
Flow: injection_check → safety_gate → classify → factual_answer | advisory_gather | advisory_handoff
"""

import openrouter_client as llm
import prompts
from safety_gate import is_high_risk, is_injection

PHARMACIST_NAMES = ["Dược sĩ Lan", "Dược sĩ Minh", "Dược sĩ Hương"]
_pharmacist_index = 0


def _next_pharmacist() -> str:
    global _pharmacist_index
    name = PHARMACIST_NAMES[_pharmacist_index % len(PHARMACIST_NAMES)]
    _pharmacist_index += 1
    return name


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
    except Exception:
        # Fail safe: unknown → advisory
        question_type = "advisory"
        needs_context = True

    # 3a. Factual → answer immediately
    if question_type == "factual":
        try:
            answer_messages = [
                {"role": "system", "content": prompts.FACTUAL_ANSWER_SYSTEM},
                *history,
                {"role": "user", "content": message},
            ]
            reply = await llm.chat(answer_messages)
        except Exception:
            reply = "Xin lỗi, không thể tải thông tin lúc này. Vui lòng thử lại hoặc hỏi dược sĩ trực tiếp."

        return {
            "route": "factual",
            "reply": reply,
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
    return {
        "route": "advisory_handoff",
        "reply": f"Cảm ơn bạn đã cung cấp thông tin. Đang chuyển cho **{pharmacist}** tư vấn chi tiết cho bạn.",
        "handoff_summary": handoff_summary,
        "safety_gate_triggered": False,
        "model": model_name,
    }
