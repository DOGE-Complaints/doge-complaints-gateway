from __future__ import annotations

from datetime import UTC, datetime

import pytest

from core.application import StoryIntakeService
from core.domain import StoryLifecycleStatus, StoryRecord
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteStoryRepository
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION, parse_story_intake_request


def test_story_intake_service_persists_immutable_narrative_and_authorship() -> None:
    repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(
        {
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {
                "external_user_id": "user-opaque-42",
                "identity_issuer": "idp://partner",
            },
            "narrative": {
                "original_text": "Citizen reports repeated noise at night.",
                "language": "en",
                "title_hint": "Night noise",
            },
            "origin": {
                "source": "openai_gpt_action",
                "conversation_id": "conv-1",
                "tool_call_id": "call-1",
            },
            "privacy": {
                "contains_pii": True,
                "redaction_requested": True,
            },
        }
    )

    saved = service.create_story(request)
    fetched = repository.get_story(saved.story_id)

    assert fetched is not None
    assert fetched.narrative_original_text == "Citizen reports repeated noise at night."
    assert fetched.submitter_external_user_id == "user-opaque-42"
    assert fetched.submitter_identity_issuer == "idp://partner"
    assert fetched.lifecycle_status == StoryLifecycleStatus.READY_FOR_PROFILE
    assert fetched.origin_source == "openai_gpt_action"
    assert fetched.origin_conversation_id == "conv-1"
    assert fetched.origin_tool_call_id == "call-1"
    assert fetched.privacy_contains_pii is True
    assert fetched.privacy_redaction_requested is True
    assert fetched.updated_at >= fetched.created_at


def test_story_intake_service_supports_readiness_transitions() -> None:
    repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(
        {
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {"external_user_id": "user-opaque-42"},
            "narrative": {
                "original_text": "Needs clarification later.",
                "language": "en",
                "title_hint": "Needs clarification",
            },
        }
    )

    saved = service.create_story(request)
    assert saved.lifecycle_status == StoryLifecycleStatus.READY_FOR_PROFILE

    advanced = service.advance_story_readiness(
        story_id=saved.story_id, narrative_complete=True
    )
    assert advanced.lifecycle_status == StoryLifecycleStatus.READY_FOR_PROFILE


def test_story_intake_service_rejects_readiness_regression() -> None:
    repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(
        {
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {"external_user_id": "user-opaque-42"},
            "narrative": {
                "original_text": "Complete story.",
                "language": "en",
                "title_hint": "complete",
            },
        }
    )

    saved = service.create_story(request)
    assert saved.lifecycle_status == StoryLifecycleStatus.READY_FOR_PROFILE

    with pytest.raises(ValueError, match="Cannot regress"):
        service.advance_story_readiness(
            story_id=saved.story_id, narrative_complete=False
        )


def test_story_intake_service_raises_for_unknown_story_id() -> None:
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    with pytest.raises(ValueError, match="Unknown story_id"):
        service.advance_story_readiness(story_id="missing-story", narrative_complete=True)


def test_sqlite_story_repository_roundtrip_and_get_missing() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    repo = SqliteStoryRepository(db)
    now = datetime.now(UTC)
    story = StoryRecord(
        story_id="sqlite-story-1",
        schema_version="m2.story_intake_envelope.v1",
        narrative_original_text="SQLite direct story roundtrip",
        submitter_external_user_id="sqlite-user",
        submitter_identity_issuer=None,
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        created_at=now,
        updated_at=now,
        narrative_language="en",
        narrative_title_hint="SQLite roundtrip",
        narrative_canonical_type="infrastructure",
        narrative_canonical_labels=("lighting",),
    )

    repo.save_story(story)
    fetched = repo.get_story("sqlite-story-1")
    all_rows = repo.list_stories()
    missing = repo.get_story("missing-story")

    assert fetched is not None
    assert fetched.story_id == "sqlite-story-1"
    assert fetched.narrative_canonical_labels == ("lighting",)
    assert len(all_rows) == 1
    assert all_rows[0].story_id == "sqlite-story-1"
    assert missing is None

