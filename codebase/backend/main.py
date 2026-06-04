from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from chat_log import log_conversation, log_report

load_dotenv()

app = FastAPI(title="Long Chau AI Triage API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RISK_KEYWORDS = [
    "tiểu đường", "huyết áp", "đang uống", "bệnh mãn tính",
    "tim mạch", "suy thận", "gan", "dị ứng", "thai kỳ", "mang thai",
    "đang điều trị", "tương tác", "liều cao",
]

FACTUAL_KEYWORDS = ["tác dụng", "thành phần", "dùng như thế nào", "công dụng", "là gì"]

PHARMACIST_NAMES = ["Dược sĩ Lan", "Dược sĩ Minh", "Dược sĩ Hương"]


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


class ReportRequest(BaseModel):
    user_message: str
    bot_reply: str
    route: str = ""
    model: str = ""
    description: str = ""


def stub_route(message: str) -> dict:
    """Keyword heuristic stub — replaced by real AI in Phase 3."""
    msg_lower = message.lower()

    if any(kw in msg_lower for kw in RISK_KEYWORDS):
        return {
            "route": "advisory_handoff",
            "reply": "⚠️ Câu hỏi của bạn liên quan đến tình trạng sức khoẻ cụ thể. Đang chuyển cho dược sĩ để tư vấn chính xác hơn.",
            "handoff_summary": (
                "Khách hỏi về tương tác thuốc / liều dùng trong bối cảnh bệnh lý cụ thể. "
                "Cần tư vấn trực tiếp để đảm bảo an toàn."
            ),
            "safety_gate_triggered": True,
            "model": "stub",
        }

    if any(kw in msg_lower for kw in FACTUAL_KEYWORDS):
        return {
            "route": "factual",
            "reply": (
                "Đây là thông tin chung về thuốc bạn hỏi. "
                "Thuốc được dùng theo liều chỉ định, uống sau bữa ăn để tránh kích ứng dạ dày. "
                "\n\n_Lưu ý: Nếu bạn đang điều trị bệnh cụ thể, hãy hỏi dược sĩ để được tư vấn chính xác hơn._"
            ),
            "handoff_summary": None,
            "safety_gate_triggered": False,
            "model": "stub",
        }

    return {
        "route": "advisory_gather",
        "reply": "Để tư vấn chính xác hơn, bạn có thể cho tôi biết bạn đang dùng thuốc này để điều trị bệnh gì không?",
        "handoff_summary": None,
        "safety_gate_triggered": False,
        "model": "stub",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/report")
async def report(req: ReportRequest):
    log_report(req.user_message, req.bot_reply, req.route, req.model, req.description)
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        try:
            from triage import triage
            result = await triage(req.message, req.history)
        except ImportError:
            result = stub_route(req.message)

        log_conversation(req.message, req.history, result)
        return result

    except Exception as exc:
        # Graceful fallback: never return 500 to the UI
        result = {
            "route": "advisory_handoff",
            "reply": "Xin lỗi, hệ thống đang gặp sự cố. Đang chuyển cho dược sĩ hỗ trợ bạn.",
            "handoff_summary": f"Lỗi hệ thống: {str(exc)[:100]}. Khách cần được tư vấn trực tiếp.",
            "safety_gate_triggered": False,
            "model": "fallback",
        }
        log_conversation(req.message, req.history, result)
        return result
