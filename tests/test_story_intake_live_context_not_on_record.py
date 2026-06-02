from __future__ import annotations

from dataclasses import fields

from core.application.services import StoryIntakeService
from core.domain.contracts import StoryRecord
from core.infrastructure.repositories import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import narrative_dict, valid_v2_intake_payload


def test_story_record_has_narrative_consistency_notes_field() -> None:
    """STORY-M2-02-06 T04: GAP-06 closed — consistency notes persist on StoryRecord."""
    names = {f.name for f in fields(StoryRecord)}
    assert "narrative_consistency_notes" in names


def test_intake_persists_live_story_context_consistency_notes() -> None:
    """GAP-06: live_story_context.consistency_notes → StoryRecord.narrative_consistency_notes."""
    repo = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )
    saved = service.create_story(
        parse_story_intake_request(
            valid_v2_intake_payload(
                live_story_context={"consistency_notes": "User clarified scope."},
            )
        )
    ).story
    assert saved.narrative_consistency_notes == "User clarified scope."


def test_intake_optional_summary_dict() -> None:
    req = parse_story_intake_request(
        valid_v2_intake_payload(
            narrative={
                "summary": {"et": "S et", "ru": "S ru", "en": "S en"},
            }
        )
    )
    assert req.narrative.summary == {"et": "S et", "ru": "S ru", "en": "S en"}


def test_intake_service_persists_multilingual_fields() -> None:
    repo = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )
    saved = service.create_story(
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={
                    "title": narrative_dict(ru="RU title"),
                    "summary": {"ru": "Sum ru", "et": "Sum et", "en": "Sum en"},
                }
            )
        )
    ).story
    assert saved.narrative_title is not None
    assert saved.narrative_title["ru"] == "RU title"
    assert saved.narrative_summary == {"ru": "Sum ru", "et": "Sum et", "en": "Sum en"}
