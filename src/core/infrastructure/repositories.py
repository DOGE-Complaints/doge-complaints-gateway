from __future__ import annotations

from dataclasses import dataclass

from core.domain import HealthReport


@dataclass(frozen=True)
class InMemoryHealthRepository:
    default_status: str = "ok"

    def get_health(self) -> HealthReport:
        return HealthReport(status=self.default_status)

