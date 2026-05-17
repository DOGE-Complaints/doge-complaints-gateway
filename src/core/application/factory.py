from __future__ import annotations

from typing import Protocol

from core.application.services import HealthService, SignalProfileService, StoryIntakeService
from core.application.issue_create import IssueCreateService, IssueProjectionReadStore
from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.cluster import ClusteringEngine
from core.evidence import EvidencePackService
from core.geo import GeoService
from core.projection import IssueProjectionService, StoryToProjectionPolicy
from core.promotion import IssuePromotionService
from core.config import AppConfig


class ServiceFactory(Protocol):
    """Factory contract for application services."""

    @property
    def config(self) -> AppConfig:
        """Return centralized runtime configuration used by resolved services."""
        ...

    def get_health_service(self) -> HealthService:
        """Build and return health service instance."""
        ...

    def get_story_intake_service(self) -> StoryIntakeService:
        """Build and return story intake service instance."""
        ...

    def get_signal_profile_service(self) -> SignalProfileService:
        """Build and return signal profile service instance."""
        ...

    def get_clustering_engine(self) -> ClusteringEngine:
        """Build and return clustering engine instance."""
        ...

    def get_issue_promotion_service(self) -> IssuePromotionService:
        """Build and return issue promotion orchestration service."""
        ...

    def get_issue_projection_service(self) -> IssueProjectionService:
        """Build and return SPA issue projection service."""
        ...

    def get_story_projection_policy(self) -> StoryToProjectionPolicy:
        """Build and return story->projection policy boundary implementation."""
        ...

    def get_evidence_pack_service(self) -> EvidencePackService:
        """Build and return evidence pack / lineage service."""
        ...

    def get_geo_service(self) -> GeoService:
        """Build and return geo intelligence service."""
        ...

    def get_issue_create_service(self) -> IssueCreateService:
        """Build and return issue create orchestration service."""
        ...

    def get_issue_projection_read_store(self) -> IssueProjectionReadStore:
        """Build and return issue projection read store (same backend as write store)."""
        ...

    def get_story_cluster_orchestrator(self) -> StoryClusterOrchestrator:
        """Build and return story-first cluster->issue orchestrator."""
        ...

