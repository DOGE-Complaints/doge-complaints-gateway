from __future__ import annotations

from core.domain import SignalDimension
from core.profile import REQUIRED_SIGNAL_DIMENSIONS, normalize_signal_map


def test_signal_profile_required_dimensions_are_complete() -> None:
    assert REQUIRED_SIGNAL_DIMENSIONS == (
        SignalDimension.CIVIC_DOMAIN,
        SignalDimension.FAILURE_PATTERN,
        SignalDimension.CIVIC_WEIGHT,
        SignalDimension.DESIRED_OUTCOME,
        SignalDimension.AFFECTED_GROUP,
        SignalDimension.GEOGRAPHIC_DISTRICT,
    )


def test_normalize_signal_map_strips_empty_entries() -> None:
    payload = {" topic ": " infrastructure ", "": "x", "need": " "}
    assert normalize_signal_map(payload) == {"topic": "infrastructure"}

