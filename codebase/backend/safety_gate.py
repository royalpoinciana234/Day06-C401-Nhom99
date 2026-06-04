"""
Safety gate runs BEFORE the AI classifier.
A keyword hit forces route=advisory regardless of what the LLM would decide.
Rationale: a mis-classified advisory question is the most dangerous failure mode
(patient receives confident but wrong drug-interaction advice with no human review).
"""

HIGH_RISK_KEYWORDS = [
    # Chronic disease context
    "tiểu đường", "đái tháo đường", "huyết áp", "tim mạch", "suy tim",
    "suy thận", "suy gan", "ung thư", "động kinh", "parkinson",
    # Drug interaction signals
    "đang uống thuốc", "đang dùng thuốc", "đang điều trị",
    "tương tác thuốc", "kết hợp thuốc", "uống cùng lúc",
    # Vulnerable populations
    "mang thai", "thai kỳ", "cho con bú", "trẻ sơ sinh", "trẻ em dưới",
    # Dose escalation signals
    "liều cao", "tăng liều", "quá liều", "uống nhiều hơn",
    # Allergy / adverse event
    "dị ứng thuốc", "phản ứng thuốc", "tác dụng phụ nghiêm trọng",
    # Explicit advisory request
    "bệnh mãn tính", "bệnh nền",
]


def is_high_risk(message: str) -> bool:
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in HIGH_RISK_KEYWORDS)
