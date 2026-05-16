from __future__ import annotations

from datetime import UTC, datetime, timedelta

from core.cluster.alpha import alpha_score
from core.domain import StoryGeoSnapshot, StoryLifecycleStatus
from core.projection import select_dominant_story
from tests.intake_v2_fixtures import make_story_record, narrative_dict


def _long_text(chars: int = 300) -> str:
    return "x" * chars


def test_alpha_score_rich_story_above_sixty() -> None:
    story = make_story_record(
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure", "safety"),
        narrative_original_text=_long_text(300),
        narrative_summary=narrative_dict(en="Summary"),
        narrative_consistency_notes="Follow-up notes",
        geo=StoryGeoSnapshot(
            normalized_label="Tallinn",
            latitude=59.4,
            longitude=24.7,
            confidence=0.88,
            provider="stub",
        ),
    )
    score = alpha_score(story)
    assert 0.0 <= score <= 100.0
    assert score > 60.0


def test_alpha_score_sparse_story_below_twenty() -> None:
    story = make_story_record(
        narrative_canonical_type=None,
        narrative_canonical_labels=(),
        narrative_original_text="short",
        narrative_summary=None,
        narrative_consistency_notes=None,
        geo=None,
    )
    assert alpha_score(story) < 20.0


def test_alpha_score_geo_none_skips_geo_dimension() -> None:
    base = dict(
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads",),
        narrative_original_text="Enough text for narrative points here.",
        narrative_summary=None,
        narrative_consistency_notes=None,
    )
    without_geo = make_story_record(**base, geo=None)
    with_geo = make_story_record(
        **base,
        geo=StoryGeoSnapshot(
            normalized_label="Tallinn",
            latitude=59.4,
            longitude=24.7,
            confidence=0.5,
            provider="stub",
        ),
    )
    assert alpha_score(without_geo) + 20.0 == alpha_score(with_geo)


def test_select_dominant_story_picks_higher_alpha() -> None:
    low = make_story_record(
        story_id="low",
        narrative_canonical_type="observation",
        narrative_canonical_labels=("roads",),
        narrative_original_text="Brief.",
    )
    high = make_story_record(
        story_id="high",
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure", "safety"),
        narrative_original_text=_long_text(300),
        narrative_summary=narrative_dict(en="Summary"),
    )
    dominant = select_dominant_story((low, high))
    assert dominant.story_id == "high"


def test_select_dominant_story_tie_breaks_oldest_created_at() -> None:
    older = datetime(2026, 1, 1, tzinfo=UTC)
    newer = older + timedelta(days=1)
    a = make_story_record(
        story_id="older",
        created_at=older,
        updated_at=older,
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads",),
        narrative_original_text="Same quality baseline text for tie.",
    )
    b = make_story_record(
        story_id="newer",
        created_at=newer,
        updated_at=newer,
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads",),
        narrative_original_text="Same quality baseline text for tie.",
    )
    assert alpha_score(a) == alpha_score(b)
    dominant = select_dominant_story((b, a))
    assert dominant.story_id == "older"
