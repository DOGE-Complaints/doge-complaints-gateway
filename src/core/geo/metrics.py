from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class GeoMetrics(Protocol):
    def record_cache_hit(self) -> None: ...
    def record_cache_miss(self) -> None: ...
    def record_provider_success(self, provider_id: str) -> None: ...
    def record_provider_failure(self, provider_id: str) -> None: ...
    def record_resolve_miss(self) -> None: ...
    def record_intake_degraded_geo(self) -> None: ...


@dataclass
class InMemoryGeoMetrics:
    cache_hits: int = 0
    cache_misses: int = 0
    provider_successes: dict[str, int] = field(default_factory=dict)
    provider_failures: dict[str, int] = field(default_factory=dict)
    resolve_misses: int = 0
    intake_degraded_geo: int = 0

    def record_cache_hit(self) -> None:
        self.cache_hits += 1

    def record_cache_miss(self) -> None:
        self.cache_misses += 1

    def record_provider_success(self, provider_id: str) -> None:
        self.provider_successes[provider_id] = self.provider_successes.get(provider_id, 0) + 1

    def record_provider_failure(self, provider_id: str) -> None:
        self.provider_failures[provider_id] = self.provider_failures.get(provider_id, 0) + 1

    def record_resolve_miss(self) -> None:
        self.resolve_misses += 1

    def record_intake_degraded_geo(self) -> None:
        self.intake_degraded_geo += 1
