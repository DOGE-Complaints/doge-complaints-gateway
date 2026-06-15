from __future__ import annotations

from typing import Any

VALID_LABEL_MISS_LOCALES: frozenset[str] = frozenset({"et", "ru", "en"})


class LabelMissValidationError(ValueError):
    """Invalid label-miss telemetry payload (GW-L10N-03)."""


def parse_label_miss_payload(body: Any) -> tuple[str, str]:
    if not isinstance(body, dict):
        raise LabelMissValidationError("Invalid request")
    label_key = body.get("label_key")
    locale = body.get("locale")
    if not isinstance(label_key, str) or not label_key.strip():
        raise LabelMissValidationError("Invalid request")
    if not isinstance(locale, str) or locale not in VALID_LABEL_MISS_LOCALES:
        raise LabelMissValidationError("Invalid request")
    return label_key.strip(), locale
