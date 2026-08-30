"""GW-SSR-22: civic geo-gate — no silent skip when pack geo_scope + geo_service None."""

from __future__ import annotations

from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.api.dependencies import build_api_dependencies
from core.cluster import ClusterLens
from tests.test_gw_ssr_04_schema_driven_cluster_lens import CLUSTERLENS_BASELINE
from tests.intake_v2_fixtures import valid_v2_intake_payload
from tests.story_draft_intake_helpers import post_intake_via_story_drafts


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    _clear_api_dependencies_cache()


def _intake_with_location(location: str) -> dict:
    return valid_v2_intake_payload(
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


def _deps_without_geo_service():
    base = build_api_dependencies()
    intake = replace(base.story_intake_service, geo_service=None)
    return replace(base, story_intake_service=intake)


def test_clusterlens_still_ten_members() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE
    assert len(ClusterLens) == 10


def test_scope_plus_no_geo_service_does_not_accept(client: TestClient) -> None:
    deps = _deps_without_geo_service()
    app.dependency_overrides[get_api_dependencies] = lambda: deps
    response = post_intake_via_story_drafts(
        client,
        json=_intake_with_location("Tallinn, Estonia"),
        headers={"idempotency-key": "ssr22-scope-no-service"},
    )
    assert response.status_code != 202
    assert response.status_code == 400
    assert "geo unavailable" in response.json()["error"]["message"]


def test_no_scope_plus_no_geo_service_still_accepts(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    from core.config import schema as config_schema

    real = config_schema.civic_clustering_from_active_node

    def _no_scope(*, schema_id: str, schema_version: str):
        return replace(real(schema_id=schema_id, schema_version=schema_version), geo_scope=None)

    monkeypatch.setattr(config_schema, "civic_clustering_from_active_node", _no_scope)
    deps = _deps_without_geo_service()
    app.dependency_overrides[get_api_dependencies] = lambda: deps
    response = post_intake_via_story_drafts(
        client,
        json=_intake_with_location("Tallinn, Estonia"),
        headers={"idempotency-key": "ssr22-no-scope-no-service"},
    )
    assert response.status_code == 202
