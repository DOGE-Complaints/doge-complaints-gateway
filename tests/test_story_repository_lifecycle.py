from __future__ import annotations

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
            },
        }
    )

    saved = service.create_story(request)
    fetched = repository.get_story(saved.story_id)

    assert fetched is not None
    assert fetched.narrative_original_text == "Citizen reports repeated noise at night."
    assert fetched.submitter_external_user_id == "user-opaque-42"
    assert fetched.submitter_identity_issuer == "idp://partner"
    assert fetched.lifecycle_status == StoryLifecycleStatus.ACCEPTED
    assert fetched.created_at == fetched.updated_at

