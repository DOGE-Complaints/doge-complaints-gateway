from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from core.domain import StoryGeoSnapshot
from core.geo.chain import GeoResolverChain
from core.geo.metrics import GeoMetrics
from core.geo.normalize import normalize_location_query
from core.geo.repositories import GeoCacheRepository


@dataclass(frozen=True)
class GeoService:
    """Cache-first geocoding facade for intake and downstream lenses."""

    cache: GeoCacheRepository
    resolver: GeoResolverChain
    metrics: GeoMetrics

    def resolve_for_story(self, location_query: str | None) -> StoryGeoSnapshot | None:
        if not location_query or not location_query.strip():
            return None
        raw = location_query.strip()
        canonical = normalize_location_query(raw)
        entry = self.cache.get(canonical)
        if entry is not None:
            self.metrics.record_cache_hit()
            return entry.snapshot

        self.metrics.record_cache_miss()
        snapshot = self.resolver.resolve(canonical_key=canonical, original_query=raw)
        if snapshot is None:
            self.metrics.record_resolve_miss()
            self.metrics.record_intake_degraded_geo()
            return None

        now = datetime.now(UTC)
        self.cache.put(canonical, snapshot, stored_at=now)
        return snapshot
