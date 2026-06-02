from __future__ import annotations

from core.application import StoryIntakeService
from core.geo import GeoResolverChain, GeoResolverPolicy, GeoService, default_provider_chain
from core.geo.repositories import InMemoryGeoCacheRepository
from core.geo.metrics import InMemoryGeoMetrics
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION, parse_story_intake_request


def _geo_service() -> GeoService:
    metrics = InMemoryGeoMetrics()
    chain = GeoResolverChain(
        providers=default_provider_chain(),
        policy=GeoResolverPolicy(max_attempts_per_provider=2),
        metrics=metrics,
    )
    return GeoService(
        cache=InMemoryGeoCacheRepository(),
        resolver=chain,
        metrics=metrics,
    )


def _intake_with_location(location_query: str) -> StoryIntakeService:
    return StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=_geo_service(),
    )


def _payload(location_query: str | None) -> dict:
    narrative: dict = {
        "original_text": "Issue",
        "language": "en",
        "session_language": "en",
        "title": {"et": "t", "ru": "t", "en": "Issue"},
        "description": {"et": "d", "ru": "d", "en": "Issue"},
    }
    if location_query is not None:
        narrative["location_query"] = location_query
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {
            "external_user_id": "u-geo",
            "identity_issuer": "https://idp.example.com/eid",
        },
        "narrative": narrative,
    }


def test_estonia_lookup_resolves_tallinn_ru_alias() -> None:
    svc = _intake_with_location("Таллин")
    saved = svc.create_story(parse_story_intake_request(_payload("Таллин"))).story
    assert saved.geo is not None
    assert saved.geo.admin_settlement == "tallinn"
    assert saved.geo.admin_country == "EE"
    assert saved.geo.admin_district is None


def test_estonia_lookup_resolves_kalamaja_district() -> None:
    svc = _intake_with_location("Kalamaja")
    saved = svc.create_story(parse_story_intake_request(_payload("Kalamaja"))).story
    assert saved.geo is not None
    assert saved.geo.admin_district == "kalamaja"
    assert saved.geo.admin_settlement == "tallinn"


def test_estonia_lookup_resolves_tartu_en_and_ru() -> None:
    for query in ("Tartu", "Тарту"):
        saved = _intake_with_location(query).create_story(
            parse_story_intake_request(_payload(query))
        ).story
        assert saved.geo is not None
        assert saved.geo.admin_settlement == "tartu"
        assert saved.geo.admin_country == "EE"


def test_estonia_lookup_resolves_narva_ru() -> None:
    saved = _intake_with_location("Нарва").create_story(
        parse_story_intake_request(_payload("Нарва"))
    ).story
    assert saved.geo is not None
    assert saved.geo.admin_settlement == "narva"


def test_estonia_lookup_empty_location_query_leaves_geo_null() -> None:
    saved = _intake_with_location("").create_story(
        parse_story_intake_request(_payload(""))
    ).story
    assert saved.geo is None


def test_estonia_lookup_pohja_tallinn_resolves_district_not_city() -> None:
    for query in ("Põhja-Tallinn", "põhja-tallinn", "пыхья-таллин"):
        saved = _intake_with_location(query).create_story(
            parse_story_intake_request(_payload(query))
        ).story
        assert saved.geo is not None
        assert saved.geo.admin_district == "põhja-tallinn"
        assert saved.geo.admin_settlement == "tallinn"


def test_estonia_lookup_plain_tallinn_is_city_without_district() -> None:
    saved = _intake_with_location("Tallinn").create_story(
        parse_story_intake_request(_payload("Tallinn"))
    ).story
    assert saved.geo is not None
    assert saved.geo.admin_settlement == "tallinn"
    assert saved.geo.admin_district is None
