from __future__ import annotations

from core.domain import SignalDimension


REQUIRED_SIGNAL_DIMENSIONS: tuple[SignalDimension, ...] = (
    SignalDimension.CIVIC_DOMAIN,
    SignalDimension.FAILURE_PATTERN,
    SignalDimension.CIVIC_WEIGHT,
    SignalDimension.DESIRED_OUTCOME,
    SignalDimension.AFFECTED_GROUP,
    SignalDimension.GEOGRAPHIC_DISTRICT,
)


def normalize_signal_map(payload: dict[str, str] | None) -> dict[str, str]:
    if payload is None:
        return {}
    return {
        key.strip(): value.strip()
        for key, value in payload.items()
        if key.strip() and value.strip()
    }

