from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ApiMetrics:
    """In-process counters for observability smoke tests (demo scope)."""

    health_requests: int = 0
    readiness_requests: int = 0
    protected_requests: int = 0
    metrics_requests: int = 0

    def record_health(self) -> None:
        self.health_requests += 1

    def record_readiness(self) -> None:
        self.readiness_requests += 1

    def record_protected(self) -> None:
        self.protected_requests += 1

    def record_metrics_endpoint(self) -> None:
        self.metrics_requests += 1

    def as_dict(self) -> dict[str, int]:
        return {
            "health_requests": self.health_requests,
            "readiness_requests": self.readiness_requests,
            "protected_requests": self.protected_requests,
            "metrics_requests": self.metrics_requests,
        }
