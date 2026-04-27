from __future__ import annotations

from dataclasses import dataclass

from core.application import StoryIntakeService
from core.domain import StoryGeoSnapshot
from core.geo import (
    GeoResolverChain,
    GeoResolverPolicy,
    GeoService,
    InMemoryGeoCacheRepository,
    InMemoryGeoMetrics,
    default_provider_chain,
)
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION, parse_story_intake_request


def _geo_service() -> tuple[GeoService, InMemoryGeoMetrics]:
    metrics = InMemoryGeoMetrics()
    cache = InMemoryGeoCacheRepository()
    chain = GeoResolverChain(
        providers=default_provider_chain(),
        policy=GeoResolverPolicy(max_attempts_per_provider=2),
        metrics=metrics,
    )
    svc = GeoService(cache=cache, resolver=chain, metrics=metrics)
    return svc, metrics


def test_geo_cache_second_request_is_cache_hit() -> None:
    svc, metrics = _geo_service()
    a = svc.resolve_for_story("Tallinn")
    b = svc.resolve_for_story("tallinn")
    assert a == b
    assert a is not None
    assert metrics.cache_hits == 1
    assert metrics.cache_misses == 1


def test_resolver_falls_back_to_second_provider_for_narva() -> None:
    svc, metrics = _geo_service()
    snap = svc.resolve_for_story("Narva old town")
    assert snap is not None
    assert snap.provider == "nominatim_stub"
    assert metrics.provider_successes.get("nominatim_stub") == 1


def test_unknown_location_does_not_break_and_records_degraded() -> None:
    svc, metrics = _geo_service()
    assert svc.resolve_for_story("unknown-place-xyz-123") is None
    assert metrics.resolve_misses == 1
    assert metrics.intake_degraded_geo == 1


def test_intake_attaches_geo_when_location_query_present() -> None:
    geo, _ = _geo_service()
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=geo,
    )
    req = parse_story_intake_request(
        {
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {"external_user_id": "u1"},
            "narrative": {
                "original_text": "Issue in capital",
                "language": "en",
                "title_hint": "Issue in capital",
                "location_query": "Tallinn",
            },
        }
    )
    saved = service.create_story(req)
    assert saved.geo is not None
    assert saved.geo.normalized_label == "Tallinn, EE"
    assert saved.geo.cluster_tags


def test_story_geo_snapshot_is_frozen_value_object() -> None:
    g = StoryGeoSnapshot(
        normalized_label="X",
        latitude=1.0,
        longitude=2.0,
        confidence=0.5,
        provider="p",
        cluster_tags=("a",),
    )
    assert g.cluster_tags == ("a",)


@dataclass
class _FlakyProvider:
    provider_id: str = "flaky"
    attempts: int = 0

    def resolve(
        self, original_query: str, *, canonical_key: str
    ) -> StoryGeoSnapshot | None:
        self.attempts += 1
        if self.attempts == 1:
            raise TimeoutError("simulated timeout")
        return StoryGeoSnapshot(
            normalized_label="Recovered",
            latitude=0.0,
            longitude=0.0,
            confidence=0.5,
            provider=self.provider_id,
            cluster_tags=("recovered",),
        )


def test_geo_resolver_retries_after_timeout_with_backoff_callback() -> None:
    metrics = InMemoryGeoMetrics()
    sleeper_calls: list[float] = []
    flaky = _FlakyProvider()
    chain = GeoResolverChain(
        providers=(flaky,),
        policy=GeoResolverPolicy(max_attempts_per_provider=2, base_backoff_ms=10),
        metrics=metrics,
        sleep=lambda seconds: sleeper_calls.append(seconds),
    )
    snap = chain.resolve(canonical_key="x", original_query="x")
    assert snap is not None
    assert snap.provider == "flaky"
    assert metrics.provider_failures.get("flaky") == 1
    assert metrics.provider_successes.get("flaky") == 1
    assert sleeper_calls == [0.01]
