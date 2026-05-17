from __future__ import annotations

from typing import Any

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine
from core.domain import StoryGeoSnapshot, StoryRecord
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryRepository,
)
from core.projection import IssueProjectionService, ProjectionInput, project_distinct_issue
from core.projection.enums import DOGEIssueStatus, DOGEIssueType, DOGEIssueLabel
from core.projection.i18n import I18nText
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from tests.intake_v2_fixtures import make_story_record, narrative_dict


def _geo_kalamaja() -> StoryGeoSnapshot:
    return StoryGeoSnapshot(
        normalized_label="Kalamaja, Tallinn",
        latitude=59.4372,
        longitude=24.7453,
        confidence=0.9,
        provider="stub",
        admin_district="Põhja-Tallinn",
        admin_settlement="Tallinn",
        admin_region="Harju maakond",
        admin_country="EE",
    )


def _geo_mustamae() -> StoryGeoSnapshot:
    return StoryGeoSnapshot(
        normalized_label="Mustamäe, Tallinn",
        latitude=59.408,
        longitude=24.698,
        confidence=0.85,
        provider="stub",
        admin_district="Mustamäe",
        admin_settlement="Tallinn",
        admin_region="Harju maakond",
        admin_country="EE",
    )


def _story(
    story_id: str,
    *,
    text: str,
    title_hint: str,
    geo: StoryGeoSnapshot | None = None,
    labels: tuple[str, ...] = ("roads", "broken_infrastructure"),
    **extra: Any,
) -> StoryRecord:
    return make_story_record(
        story_id=story_id,
        narrative_original_text=text,
        submitter_external_user_id=f"user-{story_id}",
        narrative_title=narrative_dict(en=title_hint),
        narrative_canonical_type="complaint",
        narrative_canonical_labels=labels,
        geo=geo,
        **extra,
    )


def _build_orchestrator(
    stories: InMemoryStoryRepository,
) -> tuple[StoryClusterOrchestrator, InMemoryIssueProjectionStore]:
    projection_store = InMemoryIssueProjectionStore()
    promotion_service = IssuePromotionService(
        candidates=InMemoryIssueCandidateStore(),
        audit_log=InMemoryReviewAuditLogRepository(),
        gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
    )
    issue_create = IssueCreateService(
        promotion_service=promotion_service,
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
        issue_projection_store=projection_store,
        issue_story_link_store=InMemoryIssueStoryLinkStore(),
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=issue_create,
    )
    return orchestrator, projection_store


def _issue_payload(
    projection_store: InMemoryIssueProjectionStore,
    issue_id: str,
) -> dict[str, object]:
    rows = projection_store._rows
    assert rows is not None
    payload = rows[issue_id]["payload"]
    assert isinstance(payload, dict)
    return payload


def test_req40_ac1_geo_present_in_issue_payload_when_dominant_has_geo() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        _story(
            "s1",
            text="street light broken near Kalamaja district center",
            title_hint="Kalamaja light",
            geo=_geo_kalamaja(),
        )
    )
    stories.save_story(
        _story(
            "s2",
            text="street light still broken Kalamaja same area",
            title_hint="Kalamaja issue",
            geo=_geo_kalamaja(),
        )
    )
    orchestrator, projection_store = _build_orchestrator(stories)
    issue_id = orchestrator.process_story("s1")
    assert issue_id is not None

    payload = _issue_payload(projection_store, issue_id)
    assert "geo" in payload
    geo = payload["geo"]
    assert isinstance(geo, dict)
    assert geo["lat"] == 59.4372
    assert geo["lon"] == 24.7453
    assert geo["district"] == "Põhja-Tallinn"
    assert geo["settlement"] == "Tallinn"


def test_req40_ac2_issue_payload_omits_geo_key_when_stories_have_no_geo() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        _story(
            "s1",
            text="street light broken near district center no location",
            title_hint="Broken light",
            geo=None,
        )
    )
    stories.save_story(
        _story(
            "s2",
            text="street light still broken same district no location",
            title_hint="Street light issue",
            geo=None,
        )
    )
    orchestrator, projection_store = _build_orchestrator(stories)
    issue_id = orchestrator.process_story("s1")
    assert issue_id is not None

    payload = _issue_payload(projection_store, issue_id)
    assert "geo" not in payload


def test_req40_ac3_payload_geo_matches_dominant_story_alpha_score() -> None:
    stories = InMemoryStoryRepository()
    sparse = _story(
        "sparse",
        text="Brief.",
        title_hint="Mustamäe brief",
        geo=_geo_mustamae(),
        labels=("roads",),
    )
    rich = _story(
        "rich",
        text="x" * 300,
        title_hint="Kalamaja rich narrative",
        geo=_geo_kalamaja(),
        labels=("roads", "broken_infrastructure", "safety"),
        narrative_summary=narrative_dict(en="Summary"),
        narrative_consistency_notes="notes",
    )
    stories.save_story(sparse)
    stories.save_story(rich)

    bridge = StoryPromotionProjectionBridge(story_repository=stories)
    projection_input = bridge.build_projection_input(
        issue_id="issue-geo-dominant",
        promoted_title="Cluster title",
        story_ids=("sparse", "rich"),
    )
    out = project_distinct_issue(projection_input)
    d = out.to_public_dict()
    assert d["geo"]["district"] == "Põhja-Tallinn"
    assert d["geo"]["settlement"] == "Tallinn"


def test_req40_ac4_backward_compat_projection_without_geo_fields() -> None:
    legacy = ProjectionInput(
        issue_id="legacy-issue-1",
        status=DOGEIssueStatus.PUBLISHED.value,
        issue_type=DOGEIssueType.INCIDENT.value,
        labels=(DOGEIssueLabel.INFRASTRUCTURE.value,),
        title=I18nText(et="t", ru="t", en="Title"),
        summary=I18nText(et="s", ru="s", en="Summary"),
        description=I18nText(et="d", ru="d", en="Description"),
    )
    out = project_distinct_issue(legacy)
    d = out.to_public_dict()
    assert "geo" not in d
    assert d["id"] == "legacy-issue-1"

    store = InMemoryIssueProjectionStore()
    store.save_projection(
        issue_id="legacy-issue-1",
        status="PUBLISHED",
        payload=d,
        policy_version="test.v1",
    )
    rows = store._rows
    assert rows is not None
    row_payload = rows["legacy-issue-1"]["payload"]
    assert isinstance(row_payload, dict)
    assert "geo" not in row_payload


def test_bridge_passes_geo_snapshot_to_projection_input() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        _story(
            "g1",
            text="geo story text enough for clustering baseline",
            title_hint="Geo story",
            geo=_geo_kalamaja(),
        )
    )
    bridge = StoryPromotionProjectionBridge(story_repository=stories)
    inp = bridge.build_projection_input(
        issue_id="issue-1",
        promoted_title="Title",
        story_ids=("g1",),
    )
    assert inp.geo_lat == 59.4372
    assert inp.geo_lon == 24.7453
    assert inp.geo_admin_district == "Põhja-Tallinn"
