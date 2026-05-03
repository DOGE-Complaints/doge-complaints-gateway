"""Civic clustering vocabulary (gap layer3 / story-label-taxonomy alignment)."""

from __future__ import annotations

CIVIC_DOMAIN_VOCABULARY: frozenset[str] = frozenset(
    {
        "transport",
        "roads",
        "parking",
        "public_space",
        "waste",
        "environment",
        "housing",
        "education",
        "healthcare",
        "digital_service",
        "safety",
        "accessibility",
    }
)

FAILURE_PATTERN_VOCABULARY: frozenset[str] = frozenset(
    {
        "delay",
        "access_blocked",
        "information_gap",
        "broken_infrastructure",
        "unsafe_condition",
        "bureaucratic_loop",
        "unclear_rules",
        "service_unavailable",
        "maintenance_gap",
    }
)

CIVIC_SIGNAL_VOCABULARY: frozenset[str] = frozenset(
    {
        "recurring_issue",
        "systemic_pattern",
        "public_cost",
        "not_only_me",
        "equity_access",
        "trust_in_services",
        "city_for_people",
    }
)

CIVIC_SIGNAL_PRIORITY: tuple[str, ...] = (
    "systemic_pattern",
    "public_cost",
    "not_only_me",
    "recurring_issue",
    "equity_access",
    "trust_in_services",
    "city_for_people",
)
CIVIC_WEIGHT_DEFAULT = "isolated"

DESIRED_OUTCOME_VOCABULARY: frozenset[str] = frozenset(
    {
        "clear_rules",
        "faster_response",
        "safer_space",
        "better_maintenance",
        "accessible_service",
        "transparent_process",
        "human_contact",
        "digital_fix",
    }
)

AFFECTED_SCOPE_VOCABULARY: frozenset[str] = frozenset(
    {
        "pedestrians",
        "parents",
        "children_context",
        "elderly_context",
        "drivers",
        "residents",
        "visitors",
        "small_business",
        "public_users",
    }
)
AFFECTED_GROUP_DEFAULT = "general_public"

CANONICAL_EXTRACTION_POLICY = "v2.canonical"
KEYWORD_EXTRACTION_POLICY = "v1.keyword"
