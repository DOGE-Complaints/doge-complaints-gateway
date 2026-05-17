from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import logging
from typing import TYPE_CHECKING

from core.domain import StoryGeoSnapshot
from core.geo.chain import GeoResolverChain
from core.geo.metrics import GeoMetrics
from core.geo.normalize import normalize_location_query
from core.geo.repositories import GeoCacheRepository

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from core.logging_setup import StoryPipelineDebugLog


def _geo_debug_data(snapshot: StoryGeoSnapshot) -> dict[str, object]:
    return {
        "provider": snapshot.provider,
        "normalized_label": snapshot.normalized_label,
        "confidence": snapshot.confidence,
        "admin_district": snapshot.admin_district,
        "admin_settlement": snapshot.admin_settlement,
        "admin_region": snapshot.admin_region,
        "admin_country": snapshot.admin_country,
    }


@dataclass(frozen=True)
class GeoService:
    """Cache-first geocoding facade for intake and downstream lenses."""

    cache: GeoCacheRepository
    resolver: GeoResolverChain
    metrics: GeoMetrics

    def resolve_for_story(
        self,
        location_query: str | None,
        *,
        debug_logger: StoryPipelineDebugLog | None = None,
    ) -> StoryGeoSnapshot | None:
        if not location_query or not location_query.strip():
            logger.debug("geo.resolve_skipped_empty_query")
            if debug_logger is not None:
                debug_logger.log("geo", "skipped", {"reason": "empty_query"})
            return None
        raw = location_query.strip()
        canonical = normalize_location_query(raw)
        logger.debug(
            "geo.resolve_start",
            extra={"raw_query": raw[:80], "canonical_query": canonical},
        )
        entry = self.cache.get(canonical)
        if entry is not None:
            self.metrics.record_cache_hit()
            logger.debug("geo.cache_hit", extra={"canonical_query": canonical})
            if debug_logger is not None:
                debug_logger.log("geo", "resolved", _geo_debug_data(entry.snapshot))
            return entry.snapshot

        self.metrics.record_cache_miss()
        snapshot = self.resolver.resolve(canonical_key=canonical, original_query=raw)
        if snapshot is None:
            self.metrics.record_resolve_miss()
            self.metrics.record_intake_degraded_geo()
            logger.debug("geo.resolve_miss", extra={"canonical_query": canonical})
            if debug_logger is not None:
                debug_logger.log("geo", "skipped", {"reason": "resolve_miss"})
            return None

        now = datetime.now(UTC)
        self.cache.put(canonical, snapshot, stored_at=now)
        logger.debug(
            "geo.resolve_success",
            extra={
                "canonical_query": canonical,
                "provider": snapshot.provider,
                "confidence": snapshot.confidence,
            },
        )
        if debug_logger is not None:
            debug_logger.log("geo", "resolved", _geo_debug_data(snapshot))
        return snapshot
