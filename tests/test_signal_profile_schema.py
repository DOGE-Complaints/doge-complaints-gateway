from __future__ import annotations

from core.domain import SignalDimension
from core.profile import REQUIRED_SIGNAL_DIMENSIONS, normalize_signal_map


def test_signal_profile_required_dimensions_are_complete() -> None:
    assert REQUIRED_SIGNAL_DIMENSIONS == (
        SignalDimension.TOPIC,
        SignalDimension.SYSTEM_FAILURE,
        SignalDimension.NEED,
        SignalDimension.DESIRED_STATE,
        SignalDimension.REPEATABILITY,
        SignalDimension.RELEVANCE,
    )


def test_normalize_signal_map_strips_empty_entries() -> None:
    payload = {" topic ": " infrastructure ", "": "x", "need": " "}
    assert normalize_signal_map(payload) == {"topic": "infrastructure"}

