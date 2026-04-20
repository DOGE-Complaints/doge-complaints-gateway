from __future__ import annotations

from core.application import ServiceFactory
from core.domain import (
    HealthRepository,
    IdempotencyRepository,
    SignalProfileRepository,
    StoryRepository,
)
from core.infrastructure.repositories import (
    InMemoryHealthRepository,
    InMemoryIdempotencyRepository,
    InMemorySignalProfileRepository,
    InMemoryStoryRepository,
)
from core.infrastructure.service_factory import DefaultServiceFactory
from core.evidence import EvidencePackRepository, InMemoryEvidencePackRepository
from core.promotion.repositories import InMemoryIssueCandidateStore, InMemoryReviewAuditLogRepository


def provide_health_repository() -> HealthRepository:
    return InMemoryHealthRepository()


def provide_story_repository() -> StoryRepository:
    return InMemoryStoryRepository()


def provide_idempotency_repository() -> IdempotencyRepository:
    return InMemoryIdempotencyRepository()


def provide_signal_profile_repository() -> SignalProfileRepository:
    return InMemorySignalProfileRepository()


def provide_issue_candidate_store() -> InMemoryIssueCandidateStore:
    return InMemoryIssueCandidateStore()


def provide_review_audit_log_repository() -> InMemoryReviewAuditLogRepository:
    return InMemoryReviewAuditLogRepository()


def provide_evidence_pack_repository() -> EvidencePackRepository:
    return InMemoryEvidencePackRepository()


def provide_service_factory() -> ServiceFactory:
    return DefaultServiceFactory(
        health_repository=provide_health_repository(),
        story_repository=provide_story_repository(),
        idempotency_repository=provide_idempotency_repository(),
        signal_profile_repository=provide_signal_profile_repository(),
        issue_candidate_store=provide_issue_candidate_store(),
        review_audit_log_repository=provide_review_audit_log_repository(),
        evidence_pack_repository=provide_evidence_pack_repository(),
    )

