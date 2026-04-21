from __future__ import annotations

import pytest

from core.application import StoryIntakeService
from core.domain import StoryLifecycleStatus
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
            },
        }
    )

    saved = service.create_story(request)
    assert saved.lifecycle_status == StoryLifecycleStatus.PARTIAL_READY

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

