from __future__ import annotations

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.application import StoryIntakeService
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import valid_v2_intake_payload
from tests.story_draft_intake_helpers import (
    patch_identity_me_verified,
    stash_story_draft,
    submit_story_draft,
    submitter_external_id,
)


def test_story_intake_service_deduplicates_by_idempotency_key() -> None:
    story_repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(valid_v2_intake_payload())

    first = service.create_story(request, idempotency_key="idem-key-1")
    second = service.create_story(request, idempotency_key="idem-key-1")

    assert first.story.story_id == second.story.story_id


def test_story_intake_service_creates_new_story_for_different_idempotency_keys() -> None:
    story_repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(valid_v2_intake_payload())

    first = service.create_story(request, idempotency_key="idem-key-a")
    second = service.create_story(request, idempotency_key="idem-key-b")

    assert first.story.story_id != second.story.story_id


def test_http_draft_submit_idempotent_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    body = valid_v2_intake_payload()
    try:
        with TestClient(app) as client:
            draft_id = stash_story_draft(client, body)
            sub = submitter_external_id(body)
            patch_identity_me_verified(monkeypatch, sub=sub)
            first = submit_story_draft(client, draft_id)
            second = submit_story_draft(client, draft_id)
    finally:
        _clear_api_dependencies_cache()

    assert first.status_code == 202
    assert second.status_code == 202
    assert first.json()["data"]["story_id"] == second.json()["data"]["story_id"]
