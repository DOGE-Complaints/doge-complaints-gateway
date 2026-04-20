from __future__ import annotations

from dataclasses import dataclass

from core.application import HealthService, StoryIntakeService
from core.domain import HealthRepository, IdempotencyRepository, StoryRepository


@dataclass(frozen=True)
class DefaultServiceFactory:
    """Default factory wiring infrastructure into application services."""

    health_repository: HealthRepository
    story_repository: StoryRepository
    idempotency_repository: IdempotencyRepository

    def get_health_service(self) -> HealthService:
        return HealthService(repository=self.health_repository)

    def get_story_intake_service(self) -> StoryIntakeService:
        return StoryIntakeService(
            repository=self.story_repository,
            idempotency_repository=self.idempotency_repository,
        )

