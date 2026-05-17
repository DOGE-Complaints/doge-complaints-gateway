from __future__ import annotations

PII_REDACTED = "[REDACTED]"


def redact_pii(text: str, contains_pii: bool) -> str:
    """Return redacted placeholder when PII flag is set (REQ-37 §2.2)."""
    if contains_pii:
        return PII_REDACTED
    return text
