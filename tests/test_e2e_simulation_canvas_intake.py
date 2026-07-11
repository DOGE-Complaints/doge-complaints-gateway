from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest  # pyright: ignore[reportMissingImports]
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
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _load_canvas() -> list[dict[str, Any]]:
    raw = json.loads(_CANVAS_PATH.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    return raw


def _expected_summary_map(canonical: dict[str, Any]) -> dict[str, str]:
    summary_map = canonical.get("summary", {})
    if not isinstance(summary_map, dict):
        return {}
    out: dict[str, str] = {}
    for lang in ("et", "ru", "en"):
        sv = summary_map.get(lang)
        if isinstance(sv, str) and sv.strip():
            out[lang] = sv.strip()
    return out


def test_e2e_simulation_canvas_intake_trilingual_narrative_persisted(client: TestClient) -> None:
    """STORY-M2-02-06 T08: canvas scenarios → intake → repository matches title/summary/origin/lifecycle/embeddings.

    Scenarios used:
    - DOGE-EST-SC-001: infrastructure/school_crossing, language=ru
    - DOGE-EST-SC-003: infrastructure/school_crossing, language=en  (same subgroup → will cluster)
    - DOGE-EST-FU-001: environment/flooded_underpass, language=ru   (alone → no cluster)
    """
    canvas = _load_canvas()
    by_id = {str(s["simulation_id"]): s for s in canvas}

    collected: dict[str, tuple[dict[str, Any], str]] = {}  # sim_id → (payload, story_id)

    # ── Phase 1: POST all three scenarios ────────────────────────────────────
    for sim_id in ("DOGE-EST-SC-001", "DOGE-EST-SC-003", "DOGE-EST-FU-001"):
        assert sim_id in by_id, f"missing {sim_id} in {_CANVAS_PATH.name}"
        scenario = by_id[sim_id]
        payload = _scenario_to_payload(scenario)
        trace = f"trace-sim-canvas-{sim_id}"
        idem = f"idem-sim-canvas-{sim_id}"
        response = post_intake_via_story_drafts(
        client,
            json=payload,
            headers={"x-trace-id": trace, "idempotency-key": idem},
        )
        assert response.status_code == 202, response.text
        envelope = response.json()
        assert envelope["trace_id"] == trace
        collected[sim_id] = (payload, envelope["data"]["story_id"])

    deps = get_api_dependencies()
    repo = deps.story_intake_service.repository
    emb_store = deps.story_intake_service.story_embedding_store

    # ── Phase 2: per-story repository + embedding assertions ─────────────────
    for sim_id, (payload, story_id) in collected.items():
        scenario = by_id[sim_id]
        cp = scenario["normalized_issue_payload"]["canonical_payload"]
        title_map = cp["title"]
        assert isinstance(title_map, dict)
        lang = str(
            scenario["normalized_issue_payload"]["normalization_metadata"]["session_language"]
        ).strip()

        saved = repo.get_story(story_id)
        assert saved is not None

        # ── narrative fields ──────────────────────────────────────────────────
        assert saved.narrative_language == lang.lower()
        assert saved.narrative_original_text == payload["narrative"]["original_text"]

        assert saved.narrative_session_language == lang.lower()
        assert saved.narrative_title is not None
        for key in ("et", "ru", "en"):
            raw_t = title_map.get(key)
            expected = raw_t.strip() if isinstance(raw_t, str) and raw_t.strip() else ""
            assert saved.narrative_title.get(key) == expected, f"{sim_id}: title.{key} mismatch"

        expected_summary = _expected_summary_map(cp)
        assert expected_summary, f"{sim_id}: test data missing summary"
        assert saved.narrative_summary == expected_summary, (
            f"{sim_id}: narrative_summary mismatch"
        )

        # GAP-04: origin fields persisted
        assert saved.origin_source == "simulation"
        assert saved.origin_conversation_id == sim_id

        # ── lifecycle ─────────────────────────────────────────────────────────
        # All 3 scenarios have complete v2 narrative → narrative_complete=True
        assert saved.lifecycle_status.value == "ready_for_profile", (
            f"{sim_id}: expected ready_for_profile, got {saved.lifecycle_status.value}"
        )

        # ── story-level embedding ─────────────────────────────────────────────
        # InMemoryStoryEmbeddingStore._rows populated by services.py after lifecycle advance
        story_emb_rows: list[dict[str, Any]] = getattr(emb_store, "_rows", None) or []
        matching = [r for r in story_emb_rows if str(r.get("story_id")) == story_id]
        assert len(matching) == 1, f"{sim_id}: expected 1 story embedding row, got {len(matching)}"
        assert matching[0]["embedding_policy_version"] == "m2.story_embedding_policy.v1"

    # ── Phase 3: cluster pipeline ─────────────────────────────────────────────
    # SC-001 + SC-003 share subgroup infrastructure/school_crossing → CLUSTER_MIN_SIZE=2 satisfied
    # FU-001 is alone in environment/flooded_underpass → no cluster expected
    deps.story_cluster_orchestrator.process_all_pending()
    issue_create = deps.story_cluster_orchestrator.issue_create_service

    proj_rows: dict[str, Any] = getattr(issue_create.issue_projection_store, "_rows", {}) or {}
    assert len(proj_rows) >= 1, "SC-001+SC-003 must form at least 1 issue cluster after process_all_pending()"

    issue_emb_rows: list[dict[str, Any]] = (
        getattr(issue_create.issue_projection_embedding_store, "_rows", None) or []
    )
    assert len(issue_emb_rows) >= 1, "issue cluster must generate an embedding"
    assert issue_emb_rows[0]["embedding_policy_version"] == "m3.doge_issue_embedding_policy.v1"

    # Total story embeddings: exactly 3 (one per story, no duplicates)
    story_emb_rows_final: list[dict[str, Any]] = getattr(emb_store, "_rows", None) or []
    assert len(story_emb_rows_final) == len(collected), (
        f"expected {len(collected)} story embedding rows, got {len(story_emb_rows_final)}"
    )
