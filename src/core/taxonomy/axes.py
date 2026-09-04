from __future__ import annotations

# Tallinn/civic reference axes (D-SSR-11 / REQ-20 §3 / §18.3).
# Reference frozenset for docs, tallinn seed, and helpers — NOT Contour1 wire reject SSOT.
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
    """Normalize a Contour1 wire axis id: non-empty str → strip → lower.

    Pack-/node-defined axis ids are accepted. Empty or non-string values still raise.
    """
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("axis must be a non-empty string.")
    return raw.strip().lower()
