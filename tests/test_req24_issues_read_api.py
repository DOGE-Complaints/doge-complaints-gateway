from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.domain import StoryGeoSnapshot
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteIssueProjectionStore
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from core.projection.read_filters import filter_projection_rows, normalize_geo_token
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict
from tests.geo_propagation_fixtures import (
    build_orchestrator,
    geo_kalamaja,
    geo_mustamae,
    story_record,
)
from tests.story_draft_intake_helpers import post_intake_via_story_drafts


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch.setenv("SERVICE_API_TOKEN", "req24-test-token")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer req24-test-token"}


def _app_story_repository():
    return get_api_dependencies().story_cluster_orchestrator.story_repository


def _seed_via_intake(client: TestClient) -> str:
    payload = intake_payload_simple(
        external_user_id="req24-user",
        original_text="Broken pavement near Kalamaja street lights",
        title_en="Kalamaja pavement",
    )
    payload["narrative"]["location_query"] = "Kalamaja, Tallinn"
    response = post_intake_via_story_drafts(
        client, json=payload)
    assert response.status_code == 202
    story_id = str(response.json()["data"]["story_id"])
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()
    deps = get_api_dependencies()
    store = deps.issue_create_service.issue_projection_store
    assert store is not None
    rows = getattr(store, "_rows")
    assert rows
    return str(next(iter(rows.keys())))


def _projection_payload(
    issue_id: str,
    *,
    geo: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": issue_id,
        "status": "PUBLISHED",
        "type": "INCIDENT",
        "labels": ["infrastructure"],
        "title": {"et": "t", "ru": "t", "en": "t"},
        "summary": {"et": "s", "ru": "s", "en": "s"},
        "description": {"et": "d", "ru": "d", "en": "d"},
    }
    if geo is not None:
        payload["geo"] = geo
    return payload


def _save_projection(
    issue_id: str,
    *,
    geo: dict[str, object] | None = None,
) -> None:
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    store.save_projection(
        issue_id=issue_id,
        status="PUBLISHED",
        payload=_projection_payload(issue_id, geo=geo),
        policy_version="m3.doge_issue_derivation.v1",
    )


def test_req24_ac1_sqlite_doge_issues_table_exists(tmp_path: Path) -> None:
    db_path = tmp_path / "req24.sqlite"
    db = SqliteDatabase.from_url(f"sqlite:///{db_path}")
    db.ensure_schema()
    row = db.connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='doge_issues'"
    ).fetchone()
    assert row is not None
    db.connection.close()


def test_req24_ac2_write_path_uses_doge_issues(client: TestClient) -> None:
    payload = intake_payload_simple(
        external_user_id="req24-ac2-user",
        original_text="write path regression for doge_issues table",
        title_en="AC2 write path",
    )
    payload["narrative"]["location_query"] = "Kalamaja, Tallinn"
    response = post_intake_via_story_drafts(
        client, json=payload)
    assert response.status_code == 202
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()
    in_memory = get_api_dependencies().issue_create_service.issue_projection_store
    assert in_memory is not None
    rows = getattr(in_memory, "_rows", {})
    assert rows, "intake write path must persist at least one projection row"


def test_req24_ac2_sqlite_write_path_uses_doge_issues_table(tmp_path: Path) -> None:
    db = SqliteDatabase.from_url(f"sqlite:///{tmp_path / 'ac2.sqlite'}")
    db.ensure_schema()
    store = SqliteIssueProjectionStore(db)
    payload = _projection_payload("sqlite-ac2-1")
    store.save_projection(
        issue_id="sqlite-ac2-1",
        status="PUBLISHED",
        payload=payload,
        policy_version="m3.doge_issue_derivation.v1",
    )
    row = db.connection.execute(
        "SELECT issue_id FROM doge_issues WHERE issue_id = ?",
        ("sqlite-ac2-1",),
    ).fetchone()
    assert row is not None
    result = store.get_projection("sqlite-ac2-1")
    assert result is not None
    assert result["id"] == "sqlite-ac2-1"
    assert result["status"] == "PUBLISHED"
    assert "created_at" in result
    for key, value in payload.items():
        assert result[key] == value
    db.connection.close()


def test_req24_ac3_empty_list(client: TestClient) -> None:
    response = client.get("/node/issues")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["issues"] == []


def test_req24_ac4_list_after_intake(client: TestClient) -> None:
    issue_id = _seed_via_intake(client)
    response = client.get("/node/issues")
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert any(item["id"] == issue_id for item in issues)
    issue = next(item for item in issues if item["id"] == issue_id)
    for key in ("id", "status", "type", "labels", "title", "summary", "description"):
        assert key in issue


def test_req24_ac5_status_filter(client: TestClient) -> None:
    issue_id = _seed_via_intake(client)
    listed = client.get("/node/issues").json()["data"]["issues"]
    issue = next(item for item in listed if item["id"] == issue_id)
    status = str(issue["status"])
    response = client.get("/node/issues", params={"status": status})
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert issues
    assert all(item["status"] == status for item in issues)


def test_req24_ac6_type_filter(client: TestClient) -> None:
    issue_id = _seed_via_intake(client)
    issue = get_api_dependencies().issue_projection_read_store.get_projection(issue_id)
    assert issue is not None
    issue_type = str(issue["type"])
    response = client.get("/node/issues", params={"type": issue_type})
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert all(item["type"] == issue_type for item in issues)


def test_req24_ac7_get_by_id(client: TestClient) -> None:
    issue_id = _seed_via_intake(client)
    response = client.get(f"/node/issues/{issue_id}")
    assert response.status_code == 200
    assert response.json()["data"]["issue"]["id"] == issue_id


def test_req24_ac8_get_missing_returns_404(client: TestClient) -> None:
    response = client.get("/node/issues/nonexistent-issue-id")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "DOMAIN_ERROR"


def test_req24_ac9_cors_options(client: TestClient) -> None:
    response = client.options(
        "/node/issues",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "*"


@pytest.mark.gauth_raw_client
def test_req24_ac10_post_without_bearer_returns_401(client: TestClient) -> None:
    response = client.post(
        "/node/issues",
        json={
            "cluster_id": "cluster:test",
            "story_ids": ["s1"],
            "title": {"et": "t", "ru": "t", "en": "t"},
            "type": "complaint",
        },
    )
    assert response.status_code == 401


def test_req24_ac11_post_with_bearer_creates_issue(client: TestClient) -> None:
    story_id = "manual-s1"
    _app_story_repository().save_story(
        story_record(
            story_id,
            text="manual story for operator create",
            title_hint="Manual",
            geo=geo_kalamaja(),
        )
    )
    response = client.post(
        "/node/issues",
        headers=_auth_headers(),
        json={
            "cluster_id": "cluster:manual-1",
            "story_ids": [story_id],
            "title": {"et": "Katki", "ru": "Сломано", "en": "Broken"},
            "type": "complaint",
        },
    )
    assert response.status_code == 201
    issue_id = response.json()["data"]["issue_id"]
    assert issue_id


def test_req24_ac12_manual_issue_appears_in_list(client: TestClient) -> None:
    _app_story_repository().save_story(
        story_record(
            "manual-s2",
            text="second manual path",
            title_hint="Manual two",
            geo=geo_kalamaja(),
        )
    )
    create = client.post(
        "/node/issues",
        headers=_auth_headers(),
        json={
            "cluster_id": "cluster:manual-2",
            "story_ids": ["manual-s2"],
            "title": {"et": "t", "ru": "t", "en": "Manual list"},
            "type": "complaint",
        },
    )
    assert create.status_code == 201
    issue_id = create.json()["data"]["issue_id"]
    listed = client.get("/node/issues").json()["data"]["issues"]
    assert any(item["id"] == issue_id for item in listed)


def test_req24_ac14_bbox_filter(client: TestClient) -> None:
    deps = get_api_dependencies()
    stories = deps.story_cluster_orchestrator.story_repository
    stories.save_story(
        story_record(
            "geo-in",
            text="unique kalamaja bbox seed alpha",
            title_hint="In",
            geo=geo_kalamaja(),
        )
    )
    stories.save_story(
        story_record(
            "geo-out",
            text="unique mustamae bbox seed beta",
            title_hint="Out",
            geo=geo_mustamae(),
        )
    )
    deps.story_cluster_orchestrator.process_all_pending()
    response = client.get(
        "/node/issues",
        params={
            "geo_lat_min": 59.43,
            "geo_lat_max": 59.46,
            "geo_lon_min": 24.72,
            "geo_lon_max": 24.77,
        },
    )
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert issues
    for item in issues:
        assert "geo" in item
        assert 59.43 <= float(item["geo"]["lat"]) <= 59.46
        assert 24.72 <= float(item["geo"]["lon"]) <= 24.77


def test_req24_ac15_geo_less_excluded_when_bbox_active(client: TestClient) -> None:
    _save_projection("geo-yes", geo={"lat": 59.44, "lon": 24.75, "district": "Põhja-Tallinn"})
    _save_projection("geo-no")
    response = client.get("/node/issues", params={"geo_lat_min": 59.43})
    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["data"]["issues"]}
    assert "geo-yes" in ids
    assert "geo-no" not in ids


def test_req24_ac16_district_normalized(client: TestClient) -> None:
    _app_story_repository().save_story(
        story_record(
            "dist-1",
            text="district filter unique seed gamma",
            title_hint="District",
            geo=geo_kalamaja(),
        )
    )
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()
    response = client.get(
        "/node/issues",
        params={"geo_district": "põhja-tallinn"},
    )
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert len(issues) >= 1
    assert normalize_geo_token("põhja-tallinn") == normalize_geo_token("Põhja-Tallinn")


def test_req24_ac17_geo_district_multi_value_or(client: TestClient) -> None:
    _save_projection(
        "dist-a",
        geo={"lat": 59.44, "lon": 24.75, "district": "Põhja-Tallinn"},
    )
    _save_projection(
        "dist-b",
        geo={"lat": 59.41, "lon": 24.70, "district": "Mustamäe"},
    )
    response = client.get(
        "/node/issues",
        params=[("geo_district", "põhja-tallinn"), ("geo_district", "mustamäe")],
    )
    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["data"]["issues"]}
    assert ids == {"dist-a", "dist-b"}


def test_req24_ac18_bbox_and_district_and(client: TestClient) -> None:
    _save_projection(
        "and-match",
        geo={"lat": 59.44, "lon": 24.75, "district": "Põhja-Tallinn"},
    )
    _save_projection(
        "district-only-outside-bbox",
        geo={"lat": 59.40, "lon": 24.75, "district": "Põhja-Tallinn"},
    )
    response = client.get(
        "/node/issues",
        params={
            "geo_lat_min": 59.43,
            "geo_lat_max": 59.46,
            "geo_lon_min": 24.72,
            "geo_lon_max": 24.77,
            "geo_district": "põhja-tallinn",
        },
    )
    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["data"]["issues"]}
    assert ids == {"and-match"}


def test_req24_ac19_created_after_before(client: TestClient) -> None:
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    _save_projection("time-old")
    _save_projection("time-new")
    rows = getattr(store, "_rows")
    assert rows is not None
    rows["time-old"]["created_at"] = "2026-01-01T00:00:00+00:00"
    rows["time-new"]["created_at"] = "2026-06-01T00:00:00+00:00"
    after = client.get(
        "/node/issues",
        params={"created_after": "2026-03-01T00:00:00+00:00"},
    )
    assert after.status_code == 200
    after_ids = {item["id"] for item in after.json()["data"]["issues"]}
    assert "time-new" in after_ids
    assert "time-old" not in after_ids
    before = client.get(
        "/node/issues",
        params={"created_before": "2026-03-01T00:00:00+00:00"},
    )
    assert before.status_code == 200
    before_ids = {item["id"] for item in before.json()["data"]["issues"]}
    assert "time-old" in before_ids
    assert "time-new" not in before_ids


def test_req24_ac20_empty_geo_param_ignored(client: TestClient) -> None:
    _seed_via_intake(client)
    all_issues = client.get("/node/issues").json()["data"]["issues"]
    filtered = client.get("/node/issues", params={"geo_district": ""}).json()["data"][
        "issues"
    ]
    assert len(filtered) == len(all_issues)


def test_read_filters_inmemory_store() -> None:
    store = InMemoryIssueProjectionStore()
    store.save_projection(
        issue_id="i1",
        status="NEW",
        payload={
            "id": "i1",
            "status": "NEW",
            "type": "INCIDENT",
            "labels": ["infrastructure"],
            "title": {"et": "t", "ru": "t", "en": "t"},
            "summary": {"et": "s", "ru": "s", "en": "s"},
            "description": {"et": "d", "ru": "d", "en": "d"},
            "geo": {"lat": 59.44, "lon": 24.75, "district": "Põhja-Tallinn"},
        },
        policy_version="m3.doge_issue_derivation.v1",
    )
    rows = store.list_projections(geo_district=["põhja-tallinn"])
    assert len(rows) == 1
    assert store.get_projection("i1") is not None
    assert store.get_projection("missing") is None


def test_sqlite_read_store_roundtrip(tmp_path: Path) -> None:
    db = SqliteDatabase.from_url(f"sqlite:///{tmp_path / 'read.sqlite'}")
    db.ensure_schema()
    store = SqliteIssueProjectionStore(db)
    payload: dict[str, object] = {
        "id": "sqlite-1",
        "status": "NEW",
        "type": "INCIDENT",
        "labels": [],
        "title": {"et": "t", "ru": "t", "en": "t"},
        "summary": {"et": "s", "ru": "s", "en": "s"},
        "description": {"et": "d", "ru": "d", "en": "d"},
    }
    store.save_projection(
        issue_id="sqlite-1",
        status="NEW",
        payload=payload,
        policy_version="m3.doge_issue_derivation.v1",
    )
    listed = store.list_projections(status=["NEW"])
    assert len(listed) == 1
    result = store.get_projection("sqlite-1")
    assert result is not None
    assert result["id"] == "sqlite-1"
    assert result["status"] == "NEW"
    assert "created_at" in result
    for key, value in payload.items():
        assert result[key] == value
    db.connection.close()


def test_openapi_contains_tallinn_paths() -> None:
    text = (
        Path(__file__).resolve().parents[1]
        / "docs/runtime-docs/api-reference/openapi.yaml"
    ).read_text(encoding="utf-8")
    assert "/node/issues:" in text
    assert "get:" in text
    assert "post:" in text
