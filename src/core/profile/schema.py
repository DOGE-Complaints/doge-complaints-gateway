from __future__ import annotations

from core.domain import SignalDimension


REQUIRED_SIGNAL_DIMENSIONS: tuple[SignalDimension, ...] = (
    SignalDimension.TOPIC,
    SignalDimension.SYSTEM_FAILURE,
    SignalDimension.NEED,
    SignalDimension.DESIRED_STATE,
    SignalDimension.REPEATABILITY,
    SignalDimension.RELEVANCE,
)


def normalize_signal_map(payload: dict[str, str] | None) -> dict[str, str]:
    if payload is None:
        return {}
    return {
        key.strip(): value.strip()
        for key, value in payload.items()
        if key.strip() and value.strip()
    }

