"""GW-TAX-02: composite primary, new lenses, story_labels source, per-lens min_size."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import pytest

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine, ClusterLens, StoryProfileSignals
from core.cluster.engine import (
    cluster_key_for_lens,
    composite_primary_cluster_key,
    composite_primary_signal_pair,
    lens_dimension,
)
from core.config.schema import load_config_from_env
from core.domain import SignalDimension, StoryLabel, StoryLifecycleStatus, StoryRecord
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryLabelRepository,
    InMemoryStoryRepository,
)
from core.profile.enrichment import get_signals_for_story, infer_signals_from_canonical
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from core.taxonomy.story_labels import signals_from_story_labels
from tests.test_gw_seed_02_cluster_density import (
    CANVAS_V02,
    CLUSTER_MIN_SIZE,
    READINESS_THRESHOLD,
    _district_for_cluster,
    _load_v02_scenarios,
    _story_from_scenario,
)

CANONICAL_SIGNALS = {
    "civic_domain": "roads",
    "failure_pattern": "broken_infrastructure",
    "civic_weight": "systemic_pattern",
    "desired_outcome": "safer_space",
    "affected_group": "general_public",
    "geographic_district": "unknown",
    "service_object": "unknown",
    "need": "unknown",
    "ecosystem_signal": "unknown",
    "canonical_type": "complaint",
}


def _profile(story_id: str, **signals: str) -> StoryProfileSignals:
    merged = dict(CANONICAL_SIGNALS)
    merged.update(signals)
    return StoryProfileSignals(story_id=story_id, signals=merged)


def test_composite_primary_cluster_key_separates_domain_and_pattern() -> None:
    roads_broken = _profile("s-rb", civic_domain="roads", failure_pattern="broken_infrastructure")
    roads_maint = _profile("s-rm", civic_domain="roads", failure_pattern="maintenance_gap")
    waste_broken = _profile("s-wb", civic_domain="waste", failure_pattern="broken_infrastructure")

    key_rb = composite_primary_cluster_key(roads_broken)
    key_rm = composite_primary_cluster_key(roads_maint)
    key_wb = composite_primary_cluster_key(waste_broken)

    assert key_rb != key_rm
    assert key_rb != key_wb
    assert "roads+broken_infrastructure" in key_rb
    assert "roads+maintenance_gap" in key_rm


def test_composite_primary_memberships_group_by_domain_and_pattern() -> None:
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.COMPOSITE_PRIMARY_MICRO,),
        primary_lens=ClusterLens.COMPOSITE_PRIMARY_MICRO,
    )
    profiles = (
        _profile("s-rb", civic_domain="roads", failure_pattern="broken_infrastructure"),
        _profile("s-rb2", civic_domain="roads", failure_pattern="broken_infrastructure"),
        _profile("s-rm", civic_domain="roads", failure_pattern="maintenance_gap"),
    )
    memberships = engine.memberships(profiles)
    composite = ClusterLens.COMPOSITE_PRIMARY_MICRO.value
    assert memberships["s-rb"][composite] == memberships["s-rb2"][composite]
    assert memberships["s-rb"][composite] != memberships["s-rm"][composite]


def test_new_signal_dimensions_and_lenses_are_wired() -> None:
    assert SignalDimension.SERVICE_OBJECT.value == "service_object"
    assert SignalDimension.ECOSYSTEM_SIGNAL.value == "ecosystem_signal"
    assert lens_dimension(ClusterLens.SERVICE_OBJECT_MICRO) == SignalDimension.SERVICE_OBJECT
    assert lens_dimension(ClusterLens.DEEP_NEED_LOCAL) == SignalDimension.NEED
    assert lens_dimension(ClusterLens.ECOSYSTEM_SIGNAL_SYSTEMIC) == SignalDimension.ECOSYSTEM_SIGNAL

    profile = _profile(
        "s-rich",
        service_object="library_portal",
        need="dignity",
        ecosystem_signal="youth_program_decline",
    )
    service_key = cluster_key_for_lens(profile, ClusterLens.SERVICE_OBJECT_MICRO)
    need_key = cluster_key_for_lens(profile, ClusterLens.DEEP_NEED_LOCAL)
    eco_key = cluster_key_for_lens(profile, ClusterLens.ECOSYSTEM_SIGNAL_SYSTEMIC)
    assert "library_portal" in service_key
    assert "dignity" in need_key
    assert "youth_program_decline" in eco_key


def test_signals_from_story_labels_prefers_per_axis_values() -> None:
    labels = (
        StoryLabel(story_id="s1", axis="topic_domain", label="waste", disposition="canonical"),
        StoryLabel(story_id="s1", axis="failure_mode", label="maintenance_gap", disposition="canonical"),
        StoryLabel(story_id="s1", axis="service_object", label="courtyard_bins", disposition="canonical"),
        StoryLabel(story_id="s1", axis="deep_need", label="safety", disposition="canonical"),
        StoryLabel(
            story_id="s1",
            axis="ecosystem_signal",
            label="neighborhood_decline",
            disposition="canonical",
        ),
    )
    signals = signals_from_story_labels(canonical_type="complaint", labels=labels)
    assert signals["civic_domain"] == "waste"
    assert signals["failure_pattern"] == "maintenance_gap"
    assert signals["service_object"] == "courtyard_bins"
    assert signals["need"] == "safety"
    assert signals["ecosystem_signal"] == "neighborhood_decline"


def _minimal_story(**overrides: object) -> StoryRecord:
    now = datetime.now(UTC)
    base = dict(
        story_id="story-tax-02",
        schema_version="2.0",
        narrative_original_text="bins overflow",
        submitter_external_user_id="user-1",
        submitter_identity_issuer="https://issuer.test",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        created_at=now,
        updated_at=now,
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure"),
    )
    base.update(overrides)
    return StoryRecord(**base)  # type: ignore[arg-type]


def test_get_signals_for_story_uses_story_label_repository_when_present() -> None:
    repo = InMemoryStoryLabelRepository()
    story = _minimal_story(story_id="story-tax-02")
    repo.save_labels(
        (
            StoryLabel(story_id="story-tax-02", axis="topic_domain", label="waste", disposition="canonical"),
            StoryLabel(
                story_id="story-tax-02",
                axis="failure_mode",
                label="maintenance_gap",
                disposition="canonical",
            ),
        )
    )
    signals = get_signals_for_story(story, story_label_repository=repo)
    assert signals["civic_domain"] == "waste"
    assert signals["failure_pattern"] == "maintenance_gap"


def test_per_lens_min_size_config_parsed_from_env() -> None:
    config = load_config_from_env(
        {
            "API_BASE_URL": "https://example.test/api",
            "CLUSTER_MIN_SIZE_BY_LENS": "composite_primary_micro=8,service_object_micro=3",
        }
    )
    assert config.cluster_min_size_by_lens["composite_primary_micro"] == 8
    assert config.cluster_min_size_by_lens["service_object_micro"] == 3
    assert config.cluster_min_size == 5


def test_orchestrator_honors_per_lens_min_size_for_primary() -> None:
    repo = InMemoryStoryRepository()
    for index in range(3):
        repo.save_story(
            _minimal_story(
                story_id=f"svc-{index}",
                narrative_original_text=f"story {index}",
                submitter_external_user_id=f"user-{index}",
            )
        )
    promotion_service = IssuePromotionService(
        candidates=InMemoryIssueCandidateStore(),
        audit_log=InMemoryReviewAuditLogRepository(),
        gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=8),
    )
    issue_create = IssueCreateService(
        promotion_service=promotion_service,
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=repo),
        issue_projection_store=InMemoryIssueProjectionStore(),
        issue_story_link_store=InMemoryIssueStoryLinkStore(),
    )
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.SERVICE_OBJECT_MICRO,),
        primary_lens=ClusterLens.SERVICE_OBJECT_MICRO,
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=repo,
        clustering_engine=engine,
        issue_create_service=issue_create,
        cluster_min_size_by_lens={"service_object_micro": 3},
        default_cluster_min_size=8,
    )
    assert orchestrator._resolve_min_size_guard("service_object_micro") == 3
    assert orchestrator._resolve_min_size_guard("composite_primary_micro") == 8


def test_v02_composite_primary_density_meets_min_size() -> None:
    buckets: Counter[str] = Counter()
    for scenario in _load_v02_scenarios():
        cp = scenario["normalized_issue_payload"]["canonical_payload"]
        labels = tuple(str(x) for x in cp.get("labels", []))
        signals = infer_signals_from_canonical(
            str(cp.get("type")),
            labels,
            geo_normalized_label=_district_for_cluster(
                str(scenario["test_metadata"]["seed_cluster_target"])
            ),
        )
        domain, pattern = composite_primary_signal_pair(signals)
        key = f"{domain}|{pattern}|{signals['geographic_district']}"
        buckets[key] += 1
    assert len(buckets) == 2
    assert all(count >= CLUSTER_MIN_SIZE for count in buckets.values())


def test_v02_process_all_pending_with_composite_primary_creates_issues() -> None:
    repo = InMemoryStoryRepository()
    for index, scenario in enumerate(_load_v02_scenarios()):
        repo.save_story(_story_from_scenario(scenario, story_id=f"v02-tax02-{index:03d}"))
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
        bridge=StoryPromotionProjectionBridge(story_repository=repo),
        issue_projection_store=InMemoryIssueProjectionStore(),
        issue_story_link_store=InMemoryIssueStoryLinkStore(),
    )
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.COMPOSITE_PRIMARY_MICRO,),
        primary_lens=ClusterLens.COMPOSITE_PRIMARY_MICRO,
        geo_filter="district",
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=repo,
        clustering_engine=engine,
        issue_create_service=issue_create,
        cluster_min_size_by_lens={"composite_primary_micro": CLUSTER_MIN_SIZE},
        default_cluster_min_size=CLUSTER_MIN_SIZE,
    )
    issue_ids = orchestrator.process_all_pending()
    assert len(issue_ids) >= 2


def test_v02_canvas_file_exists() -> None:
    assert CANVAS_V02.is_file()
    assert len(json.loads(CANVAS_V02.read_text(encoding="utf-8"))) == 18
