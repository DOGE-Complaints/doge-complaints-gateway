from __future__ import annotations

from core.cluster.vocabulary import (
    CIVIC_DOMAIN_VOCABULARY,
    CIVIC_SIGNAL_VOCABULARY,
    FAILURE_PATTERN_VOCABULARY,
)


def test_vocabulary_completeness() -> None:
    assert {
        "roads",
        "transport",
        "safety",
        "housing",
        "waste",
        "environment",
        "public_space",
        "parking",
        "education",
        "healthcare",
        "digital_service",
        "accessibility",
    } <= CIVIC_DOMAIN_VOCABULARY
    assert {
        "broken_infrastructure",
        "delay",
        "access_blocked",
        "unsafe_condition",
        "service_unavailable",
    } <= FAILURE_PATTERN_VOCABULARY
    assert {"recurring_issue", "systemic_pattern", "not_only_me"} <= CIVIC_SIGNAL_VOCABULARY
