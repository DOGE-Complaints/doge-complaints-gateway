from __future__ import annotations

from dataclasses import dataclass

from core.application import (
    HealthService,
    IssueCreateService,
    SignalProfileService,
    StoryClusterOrchestrator,
    StoryIntakeService,
    StoryPromotionProjectionBridge,
)
from core.application.issue_create import (
    IssueProjectionEmbeddingStore,
    IssueProjectionReadStore,
    IssueProjectionReadWriteStore,
    IssueStoryLinkStore,
)
from core.application.services import StoryEmbeddingStore
from core.cluster import ClusterLens, ClusteringEngine
from core.domain import (
    ClusterMembershipStore,
    HealthRepository,
    IdempotencyRepository,
    LabelTranslationMissStore,
    SignalProfileRepository,
    StoryRepository,
    StorySignalStore,
)
from core.evidence import EvidencePackRepository, EvidencePackService
from core.geo import GeoService
from core.projection import IssueProjectionService
from core.projection import (
    DeterministicStoryToProjectionPolicy,
    StoryToProjectionPolicy,
)
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import IssueCandidateStore, ReviewAuditLogRepository
from core.config import AppConfig


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
    config: AppConfig
    story_embedding_store: StoryEmbeddingStore | None = None
    issue_projection_store: IssueProjectionReadWriteStore | None = None
    issue_projection_embedding_store: IssueProjectionEmbeddingStore | None = None
    issue_story_link_store: IssueStoryLinkStore | None = None
    story_signal_store: StorySignalStore | None = None
    cluster_membership_store: ClusterMembershipStore | None = None
    label_translation_miss_store: LabelTranslationMissStore | None = None

    def get_health_service(self) -> HealthService:
        return HealthService(repository=self.health_repository)

    def get_story_intake_service(self) -> StoryIntakeService:
        return StoryIntakeService(
            repository=self.story_repository,
            idempotency_repository=self.idempotency_repository,
            geo_service=self.geo_service,
            story_embedding_store=self.story_embedding_store,
            story_signal_store=self.story_signal_store,
            log_debug_dir=self.config.log_debug_dir,
        )

    def get_signal_profile_service(self) -> SignalProfileService:
        return SignalProfileService(repository=self.signal_profile_repository)

    def get_clustering_engine(self) -> ClusteringEngine:
        return ClusteringEngine(
            active_lenses=tuple(
                ClusterLens(lens) for lens in self.config.cluster_active_lenses
            ),
            primary_lens=ClusterLens(self.config.cluster_primary_lens),
            id_algorithm=self.config.cluster_id_algorithm,
            signal_source=self.config.cluster_signal_source,
            geo_filter=self.config.cluster_geo_filter,
            tie_breaker=self.config.cluster_tie_breaker,
            type_resolution=self.config.cluster_type_resolution,
        )

    def get_issue_promotion_service(self) -> IssuePromotionService:
        return IssuePromotionService(
            candidates=self.issue_candidate_store,
            audit_log=self.review_audit_log_repository,
            gate_policy=PromotionGatePolicy(
                min_readiness_score=self.config.cluster_readiness_threshold,
                min_stories=self.config.cluster_min_size,
            ),
        )

    def get_issue_projection_service(self) -> IssueProjectionService:
        return IssueProjectionService()

    def get_story_projection_policy(self) -> StoryToProjectionPolicy:
        return DeterministicStoryToProjectionPolicy()

    def get_evidence_pack_service(self) -> EvidencePackService:
        return EvidencePackService(repository=self.evidence_pack_repository)

    def get_geo_service(self) -> GeoService:
        return self.geo_service

    def get_issue_projection_read_store(self) -> IssueProjectionReadStore:
        if self.issue_projection_store is None:
            raise ValueError("issue_projection_store is not configured.")
        return self.issue_projection_store

    def get_issue_create_service(self) -> IssueCreateService:
        return IssueCreateService(
            promotion_service=self.get_issue_promotion_service(),
            projection_service=self.get_issue_projection_service(),
            bridge=StoryPromotionProjectionBridge(
                story_repository=self.story_repository,
                extraction_policy=self.get_story_projection_policy(),
            ),
            issue_projection_store=self.issue_projection_store,
            issue_projection_embedding_store=self.issue_projection_embedding_store,
            issue_story_link_store=self.issue_story_link_store,
        )

    def get_story_cluster_orchestrator(self) -> StoryClusterOrchestrator:
        return StoryClusterOrchestrator(
            story_repository=self.story_repository,
            clustering_engine=self.get_clustering_engine(),
            issue_create_service=self.get_issue_create_service(),
            story_signal_store=self.story_signal_store,
            cluster_membership_store=self.cluster_membership_store,
            log_debug_dir=self.config.log_debug_dir,
        )

