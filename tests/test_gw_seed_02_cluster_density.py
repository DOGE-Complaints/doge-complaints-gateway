"""GW-SEED-02: v0_2 canvas produces clusters ≥8 under CLUSTER_MIN_SIZE=8."""

from __future__ import annotations
from tests.civic_pack_overrides import monkeypatch_civic_knobs

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine, ClusterLens
from core.domain import StoryGeoSnapshot, StoryLifecycleStatus, StoryRecord
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryRepository,
)
from core.profile.enrichment import infer_signals_from_canonical
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from tests.intake_v2_fixtures import narrative_dict
from tests.simulation_runner import _scenario_to_payload
from tests.story_draft_intake_helpers import post_intake_via_story_drafts

CANVAS_V02 = Path(__file__).resolve().parent / "sandbox" / "dogestonia_simulation_canvas_v0_2.json"
CLUSTER_MIN_SIZE = 8
READINESS_THRESHOLD = 70


def _load_v02_scenarios() -> list[dict[str, Any]]:
    raw = json.loads(CANVAS_V02.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    return raw


def _district_for_cluster(seed_cluster_target: str) -> str:
    if seed_cluster_target == "C1-waste-kalamaja":
        return "Kalamaja"
    if seed_cluster_target == "C2-roads-lasnamae":
        return "Lasnamäe"
    raise ValueError(seed_cluster_target)


def _story_from_scenario(scenario: dict[str, Any], *, story_id: str) -> StoryRecord:
    payload = _scenario_to_payload(scenario)
    narrative = payload["narrative"]
    simulation_id = str(scenario.get("simulation_id", story_id))
    submitter = payload.get("submitter") or {}
    submitter_external = str(
        submitter.get("external_user_id") or f"sim:{simulation_id}"
    )
    submitter_issuer = str(
        submitter.get("identity_issuer") or "https://simulation.dogestonia/eid"
    )
    cluster_target = str(scenario.get("test_metadata", {}).get("seed_cluster_target", ""))
    now = datetime.now(UTC)
    return StoryRecord(
        story_id=story_id,
        schema_version=str(payload["schema_version"]),
        narrative_original_text=str(narrative["original_text"]),
        submitter_external_user_id=submitter_external,
        submitter_identity_issuer=submitter_issuer,
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        created_at=now,
        updated_at=now,
        narrative_language=str(narrative["language"]),
        narrative_session_language=str(narrative["session_language"]),
        narrative_title=dict(narrative["title"]),
        narrative_description=dict(narrative["description"]),
        narrative_canonical_type=str(narrative.get("canonical_type") or "complaint"),
        narrative_canonical_labels=tuple(narrative.get("canonical_labels") or ()),
        geo=StoryGeoSnapshot(
            normalized_label=_district_for_cluster(cluster_target),
            latitude=59.44,
            longitude=24.75,
            confidence=0.9,
            provider="simulation",
            admin_district=_district_for_cluster(cluster_target),
            admin_settlement="Tallinn",
            admin_country="Estonia",
        ),
        origin_source="simulation",
        origin_conversation_id=str(scenario.get("simulation_id", story_id)),
    )


def _build_orchestrator(stories: InMemoryStoryRepository) -> StoryClusterOrchestrator:
    projection_store = InMemoryIssueProjectionStore()
    promotion_service = IssuePromotionService(
        candidates=InMemoryIssueCandidateStore(),
        audit_log=InMemoryReviewAuditLogRepository(),
        gate_policy=PromotionGatePolicy(
            min_readiness_score=READINESS_THRESHOLD,
            min_stories=CLUSTER_MIN_SIZE,
        ),
    )
    issue_create = IssueCreateService(
        promotion_service=promotion_service,
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
        issue_projection_store=projection_store,
        issue_story_link_store=InMemoryIssueStoryLinkStore(),
    )
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.COMPOSITE_PRIMARY_MICRO,),
        primary_lens=ClusterLens.COMPOSITE_PRIMARY_MICRO,
        geo_filter="district",
    )
    return StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=engine,
        issue_create_service=issue_create,
        cluster_min_size_by_lens={"composite_primary_micro": CLUSTER_MIN_SIZE},
        default_cluster_min_size=CLUSTER_MIN_SIZE,
    )


def test_v02_canvas_file_exists_and_v01_unchanged() -> None:
    assert CANVAS_V02.is_file()
    scenarios = _load_v02_scenarios()
    assert len(scenarios) == 18
    v01 = Path(__file__).resolve().parent / "sandbox" / "dogestonia_simulation_canvas_v0_1.json"
    assert v01.is_file()
    assert len(json.loads(v01.read_text(encoding="utf-8"))) == 130


def test_v02_offline_cluster_sizes_at_least_min_size() -> None:
    scenarios = _load_v02_scenarios()
    buckets: Counter[str] = Counter()
    for scenario in scenarios:
        cp = scenario["normalized_issue_payload"]["canonical_payload"]
        labels = tuple(str(x) for x in cp.get("labels", []))
        signals = infer_signals_from_canonical(
            str(cp.get("type")),
            labels,
            geo_normalized_label=_district_for_cluster(
                str(scenario["test_metadata"]["seed_cluster_target"])
            ),
        )
        key = (
            f"{signals['civic_domain']}|{signals['failure_pattern']}|"
            f"{signals['geographic_district']}"
        )
        buckets[key] += 1
    assert all(count >= CLUSTER_MIN_SIZE for count in buckets.values())
    assert len(buckets) == 2


def test_v02_process_all_pending_creates_issue_projections() -> None:
    repo = InMemoryStoryRepository()
    for index, scenario in enumerate(_load_v02_scenarios()):
        repo.save_story(_story_from_scenario(scenario, story_id=f"v02-story-{index:03d}"))
    orchestrator = _build_orchestrator(repo)
    issue_ids = orchestrator.process_all_pending()
    assert len(issue_ids) >= 2
    store = orchestrator.issue_create_service.issue_projection_store
    assert store is not None
    assert len(store.list_projections()) >= 2


@pytest.fixture()
def sqlite_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", str(CLUSTER_MIN_SIZE))
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", str(READINESS_THRESHOLD))
    monkeypatch_civic_knobs(monkeypatch, min_size=int(str(CLUSTER_MIN_SIZE)), readiness_threshold=int(str(READINESS_THRESHOLD)))
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'gw_seed_02.sqlite'}")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_v02_intake_and_clustering_sqlite_creates_projections(
    sqlite_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for scenario in _load_v02_scenarios():
        payload = _scenario_to_payload(scenario)
        response = post_intake_via_story_drafts(
            sqlite_client,
            json=payload,
            monkeypatch=monkeypatch,
        )
        assert response.status_code == 202, response.text
    issue_ids = get_api_dependencies().story_cluster_orchestrator.process_all_pending()
    assert len(issue_ids) >= 2
    projections = get_api_dependencies().issue_projection_read_store.list_projections()
    assert len(projections) >= 2
