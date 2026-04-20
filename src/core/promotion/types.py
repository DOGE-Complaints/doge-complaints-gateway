from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class IssueCandidateStatus(StrEnum):
    DRAFT = "draft"
    READY_FOR_REVIEW = "ready_for_review"
    IN_REVIEW = "in_review"
    PROMOTED = "promoted"
    REJECTED = "rejected"


class ReviewDecision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"


@dataclass(frozen=True)
class IssueCandidateRecord:
    candidate_id: str
    status: IssueCandidateStatus
    cluster_id: str
    story_ids: tuple[str, ...]
    readiness_score: int
    title: str


@dataclass(frozen=True)
class PromotionGateResult:
    passed: bool
    reasons: tuple[str, ...]
    details: Mapping[str, int]


@dataclass(frozen=True)
class ReviewAuditEntry:
    candidate_id: str
    actor: str
    decision: ReviewDecision
    rationale: str
    related_cluster_id: str
    related_story_ids: tuple[str, ...]
