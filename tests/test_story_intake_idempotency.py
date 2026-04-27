from __future__ import annotations

from core.application import StoryIntakeService
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION, parse_story_intake_request


def _request() -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": "opaque-abc"},
        "narrative": {
            "original_text": "Water leakage observed near public square.",
            "language": "en",
            "title_hint": "Water leakage report",
        },
    }


def test_story_intake_service_deduplicates_by_idempotency_key() -> None:
    story_repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(_request())

    first = service.create_story(request, idempotency_key="idem-key-1")
    second = service.create_story(request, idempotency_key="idem-key-1")

    assert first.story_id == second.story_id


def test_story_intake_service_creates_new_story_for_different_idempotency_keys() -> None:
    story_repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(_request())

    first = service.create_story(request, idempotency_key="idem-key-a")
    second = service.create_story(request, idempotency_key="idem-key-b")

    assert first.story_id != second.story_id

