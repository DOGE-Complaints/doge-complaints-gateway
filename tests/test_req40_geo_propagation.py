from __future__ import annotations

from core.application.issue_create import StoryPromotionProjectionBridge
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryStoryRepository,
)
from core.projection import ProjectionInput, project_distinct_issue
from core.projection.enums import DOGEIssueStatus, DOGEIssueType, DOGEIssueLabel
from core.projection.i18n import I18nText
from tests.geo_propagation_fixtures import (
    build_orchestrator,
    geo_kalamaja,
    geo_mustamae,
    issue_payload,
    story_record,
)
from tests.intake_v2_fixtures import narrative_dict


def test_req40_ac1_geo_present_in_issue_payload_when_dominant_has_geo() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        story_record(
            "s1",
            text="street light broken near Kalamaja district center",
            title_hint="Kalamaja light",
            geo=geo_kalamaja(),
        )
    )
    stories.save_story(
        story_record(
            "s2",
            text="street light still broken Kalamaja same area",
            title_hint="Kalamaja issue",
            geo=geo_kalamaja(),
        )
    )
    orchestrator, projection_store = build_orchestrator(stories)
    issue_id = orchestrator.process_story("s1")
    assert issue_id is not None

    payload = issue_payload(projection_store, issue_id)
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
        story_record(
            "s1",
            text="street light broken near district center no location",
            title_hint="Broken light",
            geo=None,
        )
    )
    stories.save_story(
        story_record(
            "s2",
            text="street light still broken same district no location",
            title_hint="Street light issue",
            geo=None,
        )
    )
    orchestrator, projection_store = build_orchestrator(stories)
    issue_id = orchestrator.process_story("s1")
    assert issue_id is not None

    payload = issue_payload(projection_store, issue_id)
    assert "geo" not in payload


def test_req40_ac3_payload_geo_matches_dominant_story_alpha_score() -> None:
    stories = InMemoryStoryRepository()
    sparse = story_record(
        "sparse",
        text="Brief.",
        title_hint="Mustamäe brief",
        geo=geo_mustamae(),
        labels=("roads",),
    )
    rich = story_record(
        "rich",
        text="x" * 300,
        title_hint="Kalamaja rich narrative",
        geo=geo_kalamaja(),
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
    row_payload = store.get_projection("legacy-issue-1")
    assert row_payload is not None
    assert "geo" not in row_payload


def test_bridge_passes_geo_snapshot_to_projection_input() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        story_record(
            "g1",
            text="geo story text enough for clustering baseline",
            title_hint="Geo story",
            geo=geo_kalamaja(),
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
