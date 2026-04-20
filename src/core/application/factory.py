from __future__ import annotations

from typing import Protocol

from core.application.services import HealthService, SignalProfileService, StoryIntakeService
from core.cluster import ClusteringEngine


class ServiceFactory(Protocol):
    """Factory contract for application services."""

    def get_health_service(self) -> HealthService:
        """Build and return health service instance."""

    def get_story_intake_service(self) -> StoryIntakeService:
        """Build and return story intake service instance."""

    def get_signal_profile_service(self) -> SignalProfileService:
        """Build and return signal profile service instance."""

    def get_clustering_engine(self) -> ClusteringEngine:
        """Build and return clustering engine instance."""

