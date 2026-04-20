from __future__ import annotations

from dataclasses import dataclass

from core.application import HealthService
from core.domain import HealthRepository


@dataclass(frozen=True)
class DefaultServiceFactory:
    """Default factory wiring infrastructure into application services."""

    health_repository: HealthRepository

    def get_health_service(self) -> HealthService:
        return HealthService(repository=self.health_repository)

