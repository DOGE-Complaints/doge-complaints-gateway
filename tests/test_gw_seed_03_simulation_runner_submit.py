"""GW-SEED-03: simulation runner stash+submit contract."""

from __future__ import annotations
from tests.civic_pack_overrides import monkeypatch_civic_knobs

import json
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from simulation_runner import _scenario_to_payload
from tests.story_draft_intake_helpers import patch_identity_me_verified, post_intake_via_story_drafts

CANVAS_V02 = Path(__file__).resolve().parent / "sandbox" / "dogestonia_simulation_canvas_v0_2.json"


def _first_v02_scenario() -> dict:
    scenarios = json.loads(CANVAS_V02.read_text(encoding="utf-8"))
    assert isinstance(scenarios, list) and scenarios
    return scenarios[0]


@pytest.fixture()
def sqlite_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "8")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "8")
    monkeypatch_civic_knobs(monkeypatch, min_size=int("8"), readiness_threshold=int("8"))
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'gw_seed_03_runner.sqlite'}")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    monkeypatch.setenv("SERVICE_API_TOKEN", "test-service-token")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_scenario_payload_stash_submit_materializes_story(
    sqlite_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scenario = _first_v02_scenario()
    payload = _scenario_to_payload(scenario)
    patch_identity_me_verified(monkeypatch, sub="sim-runner-test-sub")
    response = post_intake_via_story_drafts(
        sqlite_client,
        json=payload,
        monkeypatch=monkeypatch,
    )
    assert response.status_code == 202, response.text
    story_id = response.json()["data"]["story_id"]
    assert story_id
    orchestrator = get_api_dependencies().story_cluster_orchestrator
    assert orchestrator.story_repository.get_story(story_id) is not None
