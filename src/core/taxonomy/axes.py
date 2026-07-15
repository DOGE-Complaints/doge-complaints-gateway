from __future__ import annotations

# REQ-20 §3 + functional spec §18.3 canonical axes (13).
TAXONOMY_AXIS_VALUES = frozenset(
    {
        "topic_domain",
        "service_object",
        "location_context",
        "failure_mode",
        "issue_archetype_support",
        "affected_scope",
        "civic_signal",
        "deep_need",
        "desired_outcome",
        "ecosystem_signal",
        "governance_signal",
        "risk_privacy_safety",
        "confidence_state",
    }
)


def normalize_axis(raw: object) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("axis must be a non-empty string.")
    normalized = raw.strip().lower()
    if normalized not in TAXONOMY_AXIS_VALUES:
        raise ValueError(f"Unsupported taxonomy axis: {raw!r}.")
    return normalized
