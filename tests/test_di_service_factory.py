from __future__ import annotations

from core.infrastructure import DefaultServiceFactory, InMemoryHealthRepository
from core.infrastructure.repositories import (
    InMemoryIdempotencyRepository,
    InMemorySignalProfileRepository,
    InMemoryStoryRepository,
)
from core.evidence import InMemoryEvidencePackRepository
from core.promotion.repositories import InMemoryIssueCandidateStore, InMemoryReviewAuditLogRepository


def test_default_service_factory_resolves_health_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
        issue_candidate_store=InMemoryIssueCandidateStore(),
        review_audit_log_repository=InMemoryReviewAuditLogRepository(),
        evidence_pack_repository=InMemoryEvidencePackRepository(),
    )
    service = factory.get_health_service()
    assert service.get_status() == "ok"


def test_default_service_factory_resolves_story_intake_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
        issue_candidate_store=InMemoryIssueCandidateStore(),
        review_audit_log_repository=InMemoryReviewAuditLogRepository(),
        evidence_pack_repository=InMemoryEvidencePackRepository(),
    )
    service = factory.get_story_intake_service()
    assert service.repository is not None


def test_default_service_factory_resolves_signal_profile_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
        issue_candidate_store=InMemoryIssueCandidateStore(),
        review_audit_log_repository=InMemoryReviewAuditLogRepository(),
        evidence_pack_repository=InMemoryEvidencePackRepository(),
    )
    service = factory.get_signal_profile_service()
    assert service.repository is not None


def test_default_service_factory_resolves_clustering_engine() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
        issue_candidate_store=InMemoryIssueCandidateStore(),
        review_audit_log_repository=InMemoryReviewAuditLogRepository(),
        evidence_pack_repository=InMemoryEvidencePackRepository(),
    )
    engine = factory.get_clustering_engine()
    assert engine is not None


def test_default_service_factory_resolves_evidence_pack_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
        issue_candidate_store=InMemoryIssueCandidateStore(),
        review_audit_log_repository=InMemoryReviewAuditLogRepository(),
        evidence_pack_repository=InMemoryEvidencePackRepository(),
    )
    ev = factory.get_evidence_pack_service()
    assert ev.repository is not None


def test_default_service_factory_resolves_issue_projection_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
        issue_candidate_store=InMemoryIssueCandidateStore(),
        review_audit_log_repository=InMemoryReviewAuditLogRepository(),
        evidence_pack_repository=InMemoryEvidencePackRepository(),
    )
    proj = factory.get_issue_projection_service()
    assert proj.policy_version


def test_default_service_factory_resolves_issue_promotion_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
        issue_candidate_store=InMemoryIssueCandidateStore(),
        review_audit_log_repository=InMemoryReviewAuditLogRepository(),
        evidence_pack_repository=InMemoryEvidencePackRepository(),
    )
    promotion = factory.get_issue_promotion_service()
    assert promotion.candidates is not None
    assert promotion.audit_log is not None

