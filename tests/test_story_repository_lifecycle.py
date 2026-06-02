from __future__ import annotations

from datetime import UTC, datetime

import pytest

from core.application import StoryIntakeService
from core.domain import StoryLifecycleStatus
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteStoryRepository
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import make_story_record, narrative_dict, valid_v2_intake_payload


def test_story_intake_service_persists_immutable_narrative_and_authorship() -> None:
    repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(
        valid_v2_intake_payload(
            submitter={
                "external_user_id": "user-opaque-42",
                "identity_issuer": "idp://partner",
            },
            narrative={
                "original_text": "Citizen reports repeated noise at night.",
                "title": narrative_dict(en="Night noise"),
            },
            origin={
                "source": "openai_gpt_action",
                "conversation_id": "conv-1",
                "tool_call_id": "call-1",
            },
            privacy={"contains_pii": True, "redaction_requested": True},
        )
    )

    saved = service.create_story(request).story
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
    accepted = repository.save_story(
        make_story_record(
            lifecycle_status=StoryLifecycleStatus.ACCEPTED,
            narrative_title={"et": "", "ru": "", "en": "Needs clarification"},
        )
    )
    assert accepted.lifecycle_status == StoryLifecycleStatus.ACCEPTED

    partial = service.advance_story_readiness(
        story_id=accepted.story_id, narrative_complete=False
    )
    assert partial.lifecycle_status == StoryLifecycleStatus.PARTIAL_READY

    advanced = service.advance_story_readiness(
        story_id=accepted.story_id, narrative_complete=True
    )
    assert advanced.lifecycle_status == StoryLifecycleStatus.READY_FOR_PROFILE


def test_story_intake_service_rejects_readiness_regression() -> None:
    repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(valid_v2_intake_payload())

    saved = service.create_story(request).story
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
    story = make_story_record(
        story_id="sqlite-story-1",
        narrative_original_text="SQLite direct story roundtrip",
        submitter_external_user_id="sqlite-user",
        narrative_title=narrative_dict(en="SQLite roundtrip"),
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
    assert fetched.narrative_title is not None
    assert fetched.narrative_title["en"] == "SQLite roundtrip"
    assert len(all_rows) == 1
    assert missing is None
