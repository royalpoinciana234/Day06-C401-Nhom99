"""
Append handoff events to handoff-log.jsonl (one JSON object per line).
File is created on first write. Safe for concurrent single-process use.
"""

import json
import os
from datetime import datetime, timezone

_LOG_PATH = os.path.join(os.path.dirname(__file__), "handoff-log.jsonl")


def log_handoff(message: str, history: list[dict], summary: str, pharmacist: str, safety_triggered: bool) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "pharmacist": pharmacist,
        "safety_triggered": safety_triggered,
        "summary": summary,
        "last_message": message[:500],
        "history_len": len(history),
    }
    try:
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass  # non-critical — never crash the request
