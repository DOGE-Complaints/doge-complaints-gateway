from __future__ import annotations

from enum import StrEnum


class LabelDisposition(StrEnum):
    CANONICAL = "canonical"
    METADATA_ONLY = "metadata_only"
    NEEDS_CLARIFICATION = "needs_clarification"
    REJECTED = "rejected"
    INTERNAL = "internal"


LABEL_DISPOSITION_VALUES = frozenset(item.value for item in LabelDisposition)

# §18.4 / §24 — only canonical labels belong on public card surfaces.
PUBLIC_LABEL_DISPOSITIONS = frozenset({LabelDisposition.CANONICAL.value})


def is_public_label_disposition(disposition: str) -> bool:
    return disposition.strip().lower() in PUBLIC_LABEL_DISPOSITIONS


def normalize_disposition(raw: object) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("disposition must be a non-empty string.")
    normalized = raw.strip().lower()
    if normalized not in LABEL_DISPOSITION_VALUES:
        raise ValueError(f"Unsupported disposition: {raw!r}.")
    return normalized
