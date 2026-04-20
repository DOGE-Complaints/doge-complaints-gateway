from __future__ import annotations

from core.domain import SignalDimension
from core.profile.schema import REQUIRED_SIGNAL_DIMENSIONS


def infer_signals_from_narrative(narrative: str) -> dict[str, str]:
    text = narrative.lower()
    inferred: dict[str, str] = {}

    inferred[SignalDimension.TOPIC.value] = (
        "infrastructure" if "road" in text or "water" in text else "public_service"
    )
    inferred[SignalDimension.SYSTEM_FAILURE.value] = (
        "service_disruption" if "blocked" in text or "leak" in text else "quality_gap"
    )
    inferred[SignalDimension.NEED.value] = (
        "restore_access" if "blocked" in text else "resolve_issue"
    )
    inferred[SignalDimension.DESIRED_STATE.value] = "stable_public_service"
    inferred[SignalDimension.REPEATABILITY.value] = (
        "recurrent" if "again" in text or "repeated" in text else "single_or_unknown"
    )
    inferred[SignalDimension.RELEVANCE.value] = "high"

    for dimension in REQUIRED_SIGNAL_DIMENSIONS:
        inferred.setdefault(dimension.value, "unknown")
    return inferred

