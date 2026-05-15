from __future__ import annotations

from core.projection import (
    DeterministicStoryToProjectionPolicy,
    canonical_issue_type_from_story,
    canonical_labels_from_cluster,
    select_dominant_story,
)
from tests.intake_v2_fixtures import make_story_record


def test_canonical_labels_union_preserves_order() -> None:
    stories = (
        make_story_record(
            story_id="a",
            narrative_canonical_labels=("roads", "safety"),
        ),
        make_story_record(
            story_id="b",
            narrative_canonical_labels=("waste", "roads"),
        ),
    )
    assert canonical_labels_from_cluster(stories) == ("roads", "safety", "waste")


def test_dominant_story_prefers_richer_labels() -> None:
    sparse = make_story_record(
        story_id="sparse",
        narrative_canonical_type="observation",
        narrative_canonical_labels=("roads",),
    )
    rich = make_story_record(
        story_id="rich",
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure", "safety"),
    )
    dominant = select_dominant_story((sparse, rich))
    assert dominant.story_id == "rich"
    assert canonical_issue_type_from_story(dominant) == "INCIDENT"


def test_projection_policy_uses_canonical_fields_not_keywords() -> None:
    stories = (
        make_story_record(
            story_id="et-only",
            narrative_original_text="Tänav on katki.",
            narrative_canonical_type="complaint",
            narrative_canonical_labels=("roads",),
        ),
    )
    dominant = select_dominant_story(stories)
    draft = DeterministicStoryToProjectionPolicy().build_draft(
        promoted_title="ET title",
        aggregate_text="Tänav on katki.",
        dominant_story=dominant,
        cluster_stories=stories,
    )
    assert draft.issue_type == "INCIDENT"
    assert draft.labels == ("infrastructure",)
