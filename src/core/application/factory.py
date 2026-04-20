from __future__ import annotations

from typing import Protocol

from core.application.services import HealthService


class ServiceFactory(Protocol):
    """Factory contract for application services."""

    def get_health_service(self) -> HealthService:
        """Build and return health service instance."""

