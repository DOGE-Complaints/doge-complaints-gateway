from __future__ import annotations

from dataclasses import dataclass

from core.application import HealthService, SignalProfileService, StoryIntakeService
from core.cluster import ClusteringEngine
from core.domain import (
    HealthRepository,
    IdempotencyRepository,
    SignalProfileRepository,
    StoryRepository,
)
from core.evidence import EvidencePackRepository, EvidencePackService
from core.geo import GeoService
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import IssueCandidateStore, ReviewAuditLogRepository


@dataclass(frozen=True)
class DefaultServiceFactory:
    """Default factory wiring infrastructure into application services."""

    health_repository: HealthRepository
    story_repository: StoryRepository
    idempotency_repository: IdempotencyRepository
    signal_profile_repository: SignalProfileRepository
    issue_candidate_store: IssueCandidateStore
    review_audit_log_repository: ReviewAuditLogRepository
    evidence_pack_repository: EvidencePackRepository
    geo_service: GeoService

    def get_health_service(self) -> HealthService:
        return HealthService(repository=self.health_repository)

    def get_story_intake_service(self) -> StoryIntakeService:
        return StoryIntakeService(
            repository=self.story_repository,
            idempotency_repository=self.idempotency_repository,
            geo_service=self.geo_service,
        )

    def get_signal_profile_service(self) -> SignalProfileService:
        return SignalProfileService(repository=self.signal_profile_repository)

    def get_clustering_engine(self) -> ClusteringEngine:
        return ClusteringEngine()

    def get_issue_promotion_service(self) -> IssuePromotionService:
        return IssuePromotionService(
            candidates=self.issue_candidate_store,
            audit_log=self.review_audit_log_repository,
            gate_policy=PromotionGatePolicy(),
        )

    def get_issue_projection_service(self) -> IssueProjectionService:
        return IssueProjectionService()

    def get_evidence_pack_service(self) -> EvidencePackService:
        return EvidencePackService(repository=self.evidence_pack_repository)

    def get_geo_service(self) -> GeoService:
        return self.geo_service

