"""GW-REQ56-01: D-S1 search filter on GET /node/issues (unit + ASGI)."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.projection.issue_search_match import (
    collect_issue_searchable_text,
    issue_matches_search_query,
)
from core.projection.read_filters import filter_projection_rows
from tests.civic_pack_overrides import monkeypatch_civic_knobs


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch_civic_knobs(monkeypatch, min_size=1, readiness_threshold=1)
    monkeypatch.setenv("SERVICE_API_TOKEN", "req56-test-token")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _row(
    issue_id: str,
    *,
    status: str = "PUBLISHED",
    issue_type: str = "INCIDENT",
    title_en: str = "noise",
    description_ru: str = "шум",
    created_at: str = "2026-10-01T12:00:00Z",
) -> tuple[str, str, dict[str, object], str]:
    payload: dict[str, object] = {
        "id": issue_id,
        "status": status,
        "type": issue_type,
        "labels": ["infrastructure"],
        "title": {"et": "", "ru": "", "en": title_en},
        "summary": {"et": "s", "ru": "s", "en": "s"},
        "description": {"et": "", "ru": description_ru, "en": ""},
    }
    return (issue_id, status, payload, created_at)


def _save_projection(
    issue_id: str,
    *,
    status: str = "PUBLISHED",
    issue_type: str = "INCIDENT",
    title_en: str = "noise",
    description_ru: str = "шум",
) -> None:
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    store.save_projection(
        issue_id=issue_id,
        status=status,
        payload={
            "id": issue_id,
            "status": status,
            "type": issue_type,
            "labels": ["infrastructure"],
            "title": {"et": "", "ru": "", "en": title_en},
            "summary": {"et": "s", "ru": "s", "en": "s"},
            "description": {"et": "", "ru": description_ru, "en": ""},
        },
        policy_version="m3.doge_issue_derivation.v1",
    )


# --- T04 unit: match + compose ---


def test_req56_01_empty_search_matches_all() -> None:
    issue = {"title": {"en": "Hello"}, "description": {"ru": "мир"}}
    assert issue_matches_search_query(issue, "") is True
    assert issue_matches_search_query(issue, "   ") is True
    assert issue_matches_search_query(issue, None) is True


def test_req56_01_case_insensitive_substring() -> None:
    issue = {"title": {"en": "Broken Pavement"}, "description": {"et": "auk"}}
    assert issue_matches_search_query(issue, "pavement") is True
    assert issue_matches_search_query(issue, "PAVE") is True
    assert issue_matches_search_query(issue, "zzz") is False


def test_req56_01_haystack_et_ru_en_title_description() -> None:
    issue = {
        "title": {"et": "Tänav", "ru": "", "en": ""},
        "description": {"et": "", "ru": "яма", "en": "hole"},
    }
    haystack = collect_issue_searchable_text(issue).lower()
    assert "tänav" in haystack
    assert "яма" in haystack
    assert "hole" in haystack
    assert issue_matches_search_query(issue, "яма") is True
    assert issue_matches_search_query(issue, "HOLE") is True


def test_req56_01_filter_compose_and_with_status() -> None:
    rows = [
        _row("a", status="PUBLISHED", title_en="noise complaint"),
        _row("b", status="NEW", title_en="noise complaint"),
        _row("c", status="PUBLISHED", title_en="traffic light"),
    ]
    filtered = filter_projection_rows(
        rows, status=["PUBLISHED"], search="noise"
    )
    ids = {str(item["id"]) for item in filtered}
    assert ids == {"a"}


def test_req56_01_filter_compose_and_with_issue_type() -> None:
    """AC-02 soft evidence: search AND non-status structural (issue_type)."""
    rows = [
        _row("a", issue_type="INCIDENT", title_en="noise complaint"),
        _row("b", issue_type="IMPROVEMENT", title_en="noise complaint"),
        _row("c", issue_type="INCIDENT", title_en="traffic light"),
    ]
    filtered = filter_projection_rows(
        rows, issue_type="INCIDENT", search="noise"
    )
    ids = {str(item["id"]) for item in filtered}
    assert ids == {"a"}


def test_req56_01_filter_empty_search_no_text_restrict() -> None:
    rows = [
        _row("a", title_en="noise"),
        _row("b", title_en="traffic"),
    ]
    assert len(filter_projection_rows(rows, search=None)) == 2
    assert len(filter_projection_rows(rows, search="")) == 2
    assert len(filter_projection_rows(rows, search="  ")) == 2


def test_req56_01_filter_search_does_not_widen_vs_status() -> None:
    rows = [
        _row("pub", status="PUBLISHED", title_en="unique-needle-xyz"),
        _row("new", status="NEW", title_en="unique-needle-xyz"),
    ]
    without = {
        str(item["id"])
        for item in filter_projection_rows(rows, status=["PUBLISHED"])
    }
    with_search = {
        str(item["id"])
        for item in filter_projection_rows(
            rows, status=["PUBLISHED"], search="unique-needle-xyz"
        )
    }
    assert with_search.issubset(without)
    assert with_search == {"pub"}
    assert "new" not in with_search


# --- T05 ASGI / production entry ---


def test_req56_01_asgi_search_filters_published(client: TestClient) -> None:
    _save_projection("req56-match", title_en="special-search-token")
    _save_projection("req56-miss", title_en="other topic")
    response = client.get(
        "/node/issues",
        params={"status": "PUBLISHED", "search": "special-search-token"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "issues" in body["data"]
    ids = {str(item["id"]) for item in body["data"]["issues"]}
    assert "req56-match" in ids
    assert "req56-miss" not in ids


def test_req56_01_asgi_search_non_widening(client: TestClient) -> None:
    _save_projection("req56-pub", status="PUBLISHED", title_en="shared-token")
    _save_projection("req56-new", status="NEW", title_en="shared-token")
    base = client.get("/node/issues", params={"status": "PUBLISHED"})
    assert base.status_code == 200
    base_ids = {str(item["id"]) for item in base.json()["data"]["issues"]}
    searched = client.get(
        "/node/issues",
        params={"status": "PUBLISHED", "search": "shared-token"},
    )
    assert searched.status_code == 200
    search_ids = {str(item["id"]) for item in searched.json()["data"]["issues"]}
    assert search_ids.issubset(base_ids)
    assert "req56-pub" in search_ids
    assert "req56-new" not in search_ids


def test_req56_01_asgi_whitespace_search_no_restrict(client: TestClient) -> None:
    _save_projection("req56-keep", title_en="alpha")
    _save_projection("req56-keep2", title_en="beta")
    response = client.get(
        "/node/issues",
        params={"status": "PUBLISHED", "search": "   "},
    )
    assert response.status_code == 200
    ids = {str(item["id"]) for item in response.json()["data"]["issues"]}
    assert "req56-keep" in ids
    assert "req56-keep2" in ids


def test_req56_01_no_separate_search_route(client: TestClient) -> None:
    response = client.get("/node/search")
    assert response.status_code == 404
