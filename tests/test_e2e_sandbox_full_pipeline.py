"""REQ-39 Zone N: E2E sandbox canvas → intake → clustering → GET /node/issues."""

from __future__ import annotations
from tests.civic_pack_overrides import monkeypatch_civic_knobs

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from tests.story_draft_intake_helpers import post_intake_via_story_drafts
from simulation_runner import _scenario_to_payload

_CANVAS_PATH = Path(__file__).resolve().parent / "sandbox" / "dogestonia_simulation_canvas_v0_1.json"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch_civic_knobs(monkeypatch, min_size=int("1"), readiness_threshold=int("1"))
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _load_canvas() -> list[dict[str, Any]]:
    raw = json.loads(_CANVAS_PATH.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    return raw


def _intake_and_cluster_all_canvas(client: TestClient) -> None:
    for scenario in _load_canvas():
        payload = _scenario_to_payload(scenario)
        response = post_intake_via_story_drafts(
        client, json=payload)
        assert response.status_code == 202, (
            f"Intake failed for scenario {scenario.get('simulation_id', '?')}: {response.text}"
        )
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()


def test_n01_all_canvas_scenarios_intake_without_errors(client: TestClient) -> None:
    for scenario in _load_canvas():
        payload = _scenario_to_payload(scenario)
        response = post_intake_via_story_drafts(
        client, json=payload)
        assert response.status_code == 202, scenario.get("simulation_id", "?")


def test_n02_after_clustering_issues_exist(client: TestClient) -> None:
    _intake_and_cluster_all_canvas(client)
    store = get_api_dependencies().issue_projection_read_store
    issues = store.list_projections()
    assert len(issues) > 0, "No issues created after clustering full canvas"


def test_n03_get_node_issues_returns_results(client: TestClient) -> None:
    _intake_and_cluster_all_canvas(client)
    response = client.get("/node/issues")
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert len(issues) > 0


def test_n04_status_filter_works_on_real_data(client: TestClient) -> None:
    _intake_and_cluster_all_canvas(client)
    response = client.get("/node/issues", params={"status": "PUBLISHED"})
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert issues
    assert all(item["status"] == "PUBLISHED" for item in issues)


def test_n05_every_issue_has_required_fields(client: TestClient) -> None:
    _intake_and_cluster_all_canvas(client)
    response = client.get("/node/issues")
    issues = response.json()["data"]["issues"]
    required_fields = {"id", "status", "type", "labels", "title", "summary", "description"}
    for issue in issues:
        missing = required_fields - set(issue.keys())
        assert not missing, f"Issue {issue.get('id', '?')} missing fields: {missing}"


def test_n06_geo_filter_matches_real_data(client: TestClient) -> None:
    _intake_and_cluster_all_canvas(client)
    response_all = client.get("/node/issues")
    issues_all = response_all.json()["data"]["issues"]
    geo_issues = [
        item
        for item in issues_all
        if isinstance(item.get("geo"), dict) and item["geo"].get("district")
    ]
    if not geo_issues:
        pytest.skip("No geo-district issues in canvas — skip geo filter test")
    district = str(geo_issues[0]["geo"]["district"])
    response_filtered = client.get("/node/issues", params={"geo_district": district})
    assert response_filtered.status_code == 200
    filtered_ids = {item["id"] for item in response_filtered.json()["data"]["issues"]}
    assert geo_issues[0]["id"] in filtered_ids
