from __future__ import annotations

from dataclasses import dataclass

from core.domain import HealthRepository


@dataclass(frozen=True)
class HealthService:
    repository: HealthRepository

    def get_status(self) -> str:
        """Return health status for API or orchestration layer."""
        return self.repository.get_health().status

