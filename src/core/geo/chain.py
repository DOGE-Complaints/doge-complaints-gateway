from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from core.domain import StoryGeoSnapshot
from core.geo.metrics import GeoMetrics
from core.geo.providers import GeoProvider


@dataclass(frozen=True)
class GeoResolverPolicy:
    """Retry budget per provider before trying the next adapter."""

    max_attempts_per_provider: int = 2
    request_timeout_ms: int = 1200
    base_backoff_ms: int = 50


@dataclass(frozen=True)
class GeoResolverChain:
    providers: tuple[GeoProvider, ...]
    policy: GeoResolverPolicy
    metrics: GeoMetrics
    sleep: Callable[[float], None] | None = None

    def _backoff_seconds(self, *, attempt: int) -> float:
        backoff_ms = self.policy.base_backoff_ms * max(attempt, 1)
        return backoff_ms / 1000.0

    def resolve(self, *, canonical_key: str, original_query: str) -> StoryGeoSnapshot | None:
        for provider in self.providers:
            attempts = 0
            while attempts < self.policy.max_attempts_per_provider:
                attempts += 1
                try:
                    snap = provider.resolve(original_query, canonical_key=canonical_key)
                except TimeoutError:
                    self.metrics.record_provider_failure(provider.provider_id)
                    if self.sleep is not None and attempts < self.policy.max_attempts_per_provider:
                        self.sleep(self._backoff_seconds(attempt=attempts))
                    continue
                except Exception:
                    self.metrics.record_provider_failure(provider.provider_id)
                    if self.sleep is not None and attempts < self.policy.max_attempts_per_provider:
                        self.sleep(self._backoff_seconds(attempt=attempts))
                    continue
                if snap is not None:
                    self.metrics.record_provider_success(provider.provider_id)
                    return snap
                break
        return None
