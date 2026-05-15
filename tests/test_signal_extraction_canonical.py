from __future__ import annotations

from datetime import UTC, datetime

from core.domain import StoryLifecycleStatus, StoryRecord
from core.profile import get_signals_for_story
from tests.intake_v2_fixtures import narrative_dict


def _story(
    *,
    story_id: str = "s1",
    text: str = "",
    language: str = "en",
    canonical_type: str | None = "infrastructure",
    canonical_labels: tuple[str, ...] = (),
) -> StoryRecord:
    now = datetime.now(UTC)
    return StoryRecord(
        story_id=story_id,
        schema_version="v1",
        narrative_original_text=text,
        submitter_external_user_id="u1",
        submitter_identity_issuer="https://idp.example.com/eid",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        created_at=now,
        updated_at=now,
        narrative_language=language,
        narrative_title=narrative_dict(en="t"),
        narrative_canonical_type=canonical_type,
        narrative_canonical_labels=canonical_labels,
    )


def test_canonical_signals_language_neutral_et() -> None:
    story = _story(
        text="Teed on katki ja ohtlikud.",
        language="et",
        canonical_type="complaint",
        canonical_labels=("roads", "broken_infrastructure"),
    )
    signals = get_signals_for_story(story)
    assert signals["civic_domain"] == "roads"
    assert signals["failure_pattern"] == "broken_infrastructure"
    assert signals["canonical_type"] == "complaint"


def test_canonical_signals_language_neutral_ru() -> None:
    story = _story(
        text="Двор не убирают уже месяц.",
        language="ru",
        canonical_type="complaint",
        canonical_labels=("waste", "recurring_issue"),
    )
    signals = get_signals_for_story(story)
    assert signals["civic_domain"] == "waste"
    assert signals["civic_weight"] == "recurring_issue"
    assert signals["canonical_type"] == "complaint"


def test_civic_weight_priority_order() -> None:
    story = _story(
        canonical_labels=("recurring_issue", "systemic_pattern", "roads"),
    )
    signals = get_signals_for_story(story)
    assert signals["civic_weight"] == "systemic_pattern"


def test_civic_weight_default_isolated() -> None:
    story = _story(canonical_labels=("roads",))
    signals = get_signals_for_story(story)
    assert signals["civic_weight"] == "isolated"


def test_canonical_type_unknown_when_missing() -> None:
    story = _story(canonical_type=None, canonical_labels=("roads",))
    signals = get_signals_for_story(story)
    assert signals["canonical_type"] == "unknown"
