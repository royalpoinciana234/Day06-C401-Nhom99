"""
Conversation logging — two append-only JSONL files:
  conversation-log.jsonl  every /chat request + response
  handoff-log.jsonl       advisory_handoff events only
"""

import json
import os
from datetime import datetime, timezone

_DIR = os.path.dirname(__file__)
_CONV_LOG = os.path.join(_DIR, "conversation-log.jsonl")
_HANDOFF_LOG = os.path.join(_DIR, "handoff-log.jsonl")
_REPORT_LOG = os.path.join(_DIR, "report-log.jsonl")


def _append(path: str, entry: dict) -> None:
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass  # non-critical — never crash the request


def log_conversation(message: str, history: list[dict], response: dict) -> None:
    """Log every /chat request and its triage outcome."""
    _append(_CONV_LOG, {
        "ts": datetime.now(timezone.utc).isoformat(),
        "route": response.get("route"),
        "model": response.get("model"),
        "safety_triggered": response.get("safety_gate_triggered", False),
        "message": message[:500],
        "reply": (response.get("reply") or "")[:500],
        "history_len": len(history),
    })


def log_handoff(message: str, history: list[dict], summary: str, pharmacist: str, safety_triggered: bool) -> None:
    """Log advisory_handoff events with full summary for pharmacist review."""
    _append(_HANDOFF_LOG, {
        "ts": datetime.now(timezone.utc).isoformat(),
        "pharmacist": pharmacist,
        "safety_triggered": safety_triggered,
        "summary": summary,
        "last_message": message[:500],
        "history_len": len(history),
    })


def log_report(user_message: str, bot_reply: str, route: str, model: str, description: str = "") -> None:
    """Log user-flagged bot replies."""
    _append(_REPORT_LOG, {
        "ts": datetime.now(timezone.utc).isoformat(),
        "route": route,
        "model": model,
        "user_message": user_message[:500],
        "bot_reply": bot_reply[:500],
        "description": description[:300],
    })
