from __future__ import annotations

from dataclasses import dataclass

from core.domain import StoryGeoSnapshot
from core.geo.metrics import GeoMetrics
from core.geo.providers import GeoProvider


@dataclass(frozen=True)
class GeoResolverPolicy:
    """Retry budget per provider before trying the next adapter."""

    max_attempts_per_provider: int = 2


@dataclass(frozen=True)
class GeoResolverChain:
    providers: tuple[GeoProvider, ...]
    policy: GeoResolverPolicy
    metrics: GeoMetrics

    def resolve(self, *, canonical_key: str, original_query: str) -> StoryGeoSnapshot | None:
        for provider in self.providers:
            attempts = 0
            while attempts < self.policy.max_attempts_per_provider:
                attempts += 1
                try:
                    snap = provider.resolve(original_query, canonical_key=canonical_key)
                except Exception:
                    self.metrics.record_provider_failure(provider.provider_id)
                    continue
                if snap is not None:
                    self.metrics.record_provider_success(provider.provider_id)
                    return snap
                break
        return None
