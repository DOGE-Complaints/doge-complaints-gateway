"""REQ-39 Zone K: geo propagation StoryRecord.geo → doge_issues payload."""

from __future__ import annotations

from core.application.issue_create import StoryPromotionProjectionBridge
from core.domain import StoryGeoSnapshot
from core.infrastructure.repositories import InMemoryStoryRepository
from core.projection import project_distinct_issue
from tests.geo_propagation_fixtures import (
    build_orchestrator,
    geo_kalamaja,
    issue_payload,
    story_record,
)


def test_k01_story_with_geo_produces_issue_with_geo() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        story_record(
            "k1a",
            text="street light broken near Kalamaja district center",
            title_hint="Kalamaja light",
            geo=geo_kalamaja(),
        )
    )
    stories.save_story(
        story_record(
            "k1b",
            text="street light still broken Kalamaja same area",
            title_hint="Kalamaja issue",
            geo=geo_kalamaja(),
        )
    )
    orchestrator, projection_store = build_orchestrator(stories)
    issue_id = orchestrator.process_story("k1a")
    assert issue_id is not None
    payload = issue_payload(projection_store, issue_id)
    geo = payload.get("geo")
    assert isinstance(geo, dict)
    assert "lat" in geo or "district" in geo


def test_k02_story_without_geo_produces_issue_with_null_geo() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        story_record(
            "k2a",
            text="generic complaint without location roads broken alpha",
            title_hint="No geo a",
            geo=None,
        )
    )
    stories.save_story(
        story_record(
            "k2b",
            text="generic complaint without location roads broken beta",
            title_hint="No geo b",
            geo=None,
        )
    )
    orchestrator, projection_store = build_orchestrator(stories)
    issue_id = orchestrator.process_story("k2a")
    assert issue_id is not None
    payload = issue_payload(projection_store, issue_id)
    assert "geo" not in payload or payload.get("geo") is None


def test_k03_geo_district_normalized_in_issue_payload() -> None:
    from core.geo.scope import normalize_geo_token

    stories = InMemoryStoryRepository()
    geo = StoryGeoSnapshot(
        normalized_label="Põhja-Tallinn, Tallinn",
        latitude=59.44,
        longitude=24.75,
        confidence=0.9,
        provider="stub",
        admin_district="Põhja-Tallinn",
        admin_settlement="Tallinn",
        admin_region="Harju maakond",
        admin_country="EE",
    )
    stories.save_story(
        story_record(
            "k3a",
            text="district normalization Põhja-Tallinn alpha roads",
            title_hint="District norm a",
            geo=geo,
        )
    )
    stories.save_story(
        story_record(
            "k3b",
            text="district normalization Põhja-Tallinn beta roads",
            title_hint="District norm b",
            geo=geo,
        )
    )
    orchestrator, projection_store = build_orchestrator(stories)
    issue_id = orchestrator.process_story("k3a")
    assert issue_id is not None
    payload = issue_payload(projection_store, issue_id)
    issue_geo = payload.get("geo")
    assert isinstance(issue_geo, dict)
    district = str(issue_geo.get("district", ""))
    assert normalize_geo_token(district) == normalize_geo_token("Põhja-Tallinn")


def test_k04_cluster_dominant_geo_from_mixed_stories() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        story_record(
            "k4a",
            text="first story with geo Kalamaja crossing lights broken",
            title_hint="Geo story",
            geo=geo_kalamaja(),
        )
    )
    stories.save_story(
        story_record(
            "k4b",
            text="second story no geo same cluster theme lights crossing broken",
            title_hint="No geo story",
            geo=None,
        )
    )
    bridge = StoryPromotionProjectionBridge(story_repository=stories)
    projection_input = bridge.build_projection_input(
        issue_id="issue-k4-mixed",
        promoted_title="Mixed cluster",
        story_ids=("k4a", "k4b"),
    )
    payload = project_distinct_issue(projection_input).to_public_dict()
    assert payload.get("geo") is not None
