from __future__ import annotations

from core.infrastructure import DefaultServiceFactory, InMemoryHealthRepository
from core.infrastructure.providers import provide_app_config
from core.infrastructure.repositories import (
    InMemoryIdempotencyRepository,
    InMemorySignalProfileRepository,
    InMemoryStoryRepository,
)
from core.evidence import InMemoryEvidencePackRepository
from core.infrastructure.providers import provide_geo_service
from core.promotion.repositories import InMemoryIssueCandidateStore, InMemoryReviewAuditLogRepository


def _factory() -> DefaultServiceFactory:
    return DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
        issue_candidate_store=InMemoryIssueCandidateStore(),
        review_audit_log_repository=InMemoryReviewAuditLogRepository(),
        evidence_pack_repository=InMemoryEvidencePackRepository(),
        geo_service=provide_geo_service(),
        config=provide_app_config(),
    )


def test_default_service_factory_resolves_health_service() -> None:
    factory = _factory()
    service = factory.get_health_service()
    assert service.get_status() == "ok"


def test_default_service_factory_resolves_story_intake_service() -> None:
    factory = _factory()
    service = factory.get_story_intake_service()
    assert service.repository is not None


def test_default_service_factory_resolves_signal_profile_service() -> None:
    factory = _factory()
    service = factory.get_signal_profile_service()
    assert service.repository is not None


def test_default_service_factory_resolves_clustering_engine() -> None:
    factory = _factory()
    engine = factory.get_clustering_engine()
    assert engine is not None


def test_default_service_factory_resolves_evidence_pack_service() -> None:
    factory = _factory()
    ev = factory.get_evidence_pack_service()
    assert ev.repository is not None


def test_default_service_factory_resolves_issue_projection_service() -> None:
    factory = _factory()
    proj = factory.get_issue_projection_service()
    assert proj.policy_version


def test_default_service_factory_resolves_story_projection_policy() -> None:
    factory = _factory()
    policy = factory.get_story_projection_policy()
    draft = policy.build_draft(
        promoted_title="Road safety request",
        aggregate_text="Road safety request in district",
    )
    assert draft.policy_version
    assert draft.labels


def test_default_service_factory_resolves_issue_promotion_service() -> None:
    factory = _factory()
    promotion = factory.get_issue_promotion_service()
    assert promotion.candidates is not None
    assert promotion.audit_log is not None


def test_default_service_factory_resolves_geo_service() -> None:
    factory = _factory()
    geo = factory.get_geo_service()
    assert geo.resolve_for_story("Tallinn") is not None


def test_default_service_factory_has_centralized_app_config() -> None:
    factory = _factory()
    assert factory.config.profile.value in {"demo", "pilot"}
    assert factory.config.api_base_url.startswith("http")

