from __future__ import annotations

from enum import StrEnum


class DOGEIssueStatus(StrEnum):
    """Board-visible status values (minimal governed set for MVP)."""

    NEW = "NEW"
    IN_REVIEW = "IN_REVIEW"
    PUBLISHED = "PUBLISHED"


class DOGEIssueType(StrEnum):
    """Distinct issue type vocabulary aligned with UI filters."""

    IMPROVEMENT = "IMPROVEMENT"
    SERVICE_REQUEST = "SERVICE_REQUEST"
    INCIDENT = "INCIDENT"


class DOGEIssueLabel(StrEnum):
    """Governed label set (lowercase tokens; extend via version bump)."""

    WASTE = "waste"
    DISTRICT = "district"
    INFRASTRUCTURE = "infrastructure"
    SAFETY = "safety"
