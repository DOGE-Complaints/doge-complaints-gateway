from __future__ import annotations

from copy import deepcopy

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.cluster import ClusterLens, ClusteringEngine, StoryProfileSignals
from core.domain import StoryGeoSnapshot
from core.geo.providers import _EstoniaGeoLookup
from core.geo.scope import geo_filter_bucket, parse_cluster_geo_filter
from tests.intake_v2_fixtures import valid_v2_intake_payload
from tests.story_draft_intake_helpers import post_intake_via_story_drafts


def _civic_signals() -> dict[str, str]:
    return {
        "civic_domain": "roads",
        "failure_pattern": "broken_infrastructure",
        "civic_weight": "recurring_issue",
        "desired_outcome": "safer_space",
        "affected_group": "general_public",
        "geographic_district": "unknown",
        "canonical_type": "complaint",
    }


def _lookup() -> _EstoniaGeoLookup:
    return _EstoniaGeoLookup()


def _tallinn_geo() -> StoryGeoSnapshot:
    snap = _lookup().resolve("Tallinn", canonical_key="tallinn")
    assert snap is not None
    return snap


def _narva_geo() -> StoryGeoSnapshot:
    snap = _lookup().resolve("Narva", canonical_key="narva")
    assert snap is not None
    return snap


def test_demo_stubs_expose_admin_levels() -> None:
    tallinn = _tallinn_geo()
    narva = _narva_geo()
    assert tallinn.admin_settlement == "tallinn"
    assert tallinn.admin_country == "EE"
    assert narva.admin_settlement == "narva"
    assert narva.admin_country == "EE"


def test_parse_cluster_geo_filter_maps_legacy_any_to_country() -> None:
    assert parse_cluster_geo_filter("any") == "country"
    assert parse_cluster_geo_filter("country") == "country"


def test_geo_filter_settlement_splits_tallinn_and_narva() -> None:
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO,),
        primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        geo_filter="settlement",
    )
    signals = _civic_signals()
    profiles = (
        StoryProfileSignals(story_id="tallinn-1", signals=signals, geo=_tallinn_geo()),
        StoryProfileSignals(story_id="narva-1", signals=signals, geo=_narva_geo()),
    )
    memberships = engine.memberships(profiles)
    tallinn_cluster = memberships["tallinn-1"]["civic_domain_micro"]
    narva_cluster = memberships["narva-1"]["civic_domain_micro"]
    assert tallinn_cluster != narva_cluster


def test_geo_filter_country_groups_estonian_settlements() -> None:
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO,),
        primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        geo_filter="country",
    )
    signals = _civic_signals()
    profiles = (
        StoryProfileSignals(story_id="tallinn-1", signals=signals, geo=_tallinn_geo()),
        StoryProfileSignals(story_id="narva-1", signals=signals, geo=_narva_geo()),
    )
    memberships = engine.memberships(profiles)
    assert (
        memberships["tallinn-1"]["civic_domain_micro"]
        == memberships["narva-1"]["civic_domain_micro"]
    )


def test_geo_agnostic_profiles_share_bucket() -> None:
    assert geo_filter_bucket(None, "settlement") == "geo:agnostic"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _intake_with_location(location: str) -> dict:
    payload = valid_v2_intake_payload(
        narrative={
            "original_text": "Road damage near the center.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "Tee", "ru": "Дорога", "en": "Road"},
            "description": {"et": "Kahju", "ru": "Повреждение", "en": "Damage"},
            "location_query": location,
            "canonical_type": "complaint",
            "canonical_labels": ["roads"],
        },
    )
    return payload


def test_intake_geo_scope_rejects_narva_when_tallinn_node(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    # Scope from active pack node_clustering.civic (tallinn_civic), not CLUSTER_GEO_SCOPE env.
    _ = monkeypatch
    _clear_api_dependencies_cache()
    response = post_intake_via_story_drafts(
        client,
        json=_intake_with_location("Narva, Estonia"),
        headers={"idempotency-key": "req35-scope-narva"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "GEO_SCOPE_MISMATCH"


def test_intake_geo_scope_allows_story_without_location(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    # Optional / no location stays geo-agnostic (REQ-35). No global require-geo.
    _ = monkeypatch
    _clear_api_dependencies_cache()
    payload = _intake_with_location("")
    payload["narrative"].pop("location_query", None)
    response = post_intake_via_story_drafts(
        client,
        json=payload,
        headers={"idempotency-key": "req35-scope-no-geo"},
    )
    assert response.status_code == 202


def test_intake_geo_scope_accepts_tallinn_location(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    _ = monkeypatch
    _clear_api_dependencies_cache()
    payload = deepcopy(_intake_with_location("Tallinn, Estonia"))
    payload["submitter"] = {
        "external_user_id": "req35-tallinn-user",
        "identity_issuer": "https://idp.example.com/eid",
    }
    response = post_intake_via_story_drafts(
        client,
        json=payload,
        headers={"idempotency-key": "req35-scope-tallinn"},
    )
    assert response.status_code == 202
