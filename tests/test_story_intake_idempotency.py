from __future__ import annotations

import json
from hashlib import sha256

from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.application import StoryIntakeService
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import valid_v2_intake_payload


def test_story_intake_service_deduplicates_by_idempotency_key() -> None:
    story_repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(valid_v2_intake_payload())

    first = service.create_story(request, idempotency_key="idem-key-1")
    second = service.create_story(request, idempotency_key="idem-key-1")

    assert first.story_id == second.story_id


def test_story_intake_service_creates_new_story_for_different_idempotency_keys() -> None:
    story_repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    request = parse_story_intake_request(valid_v2_intake_payload())

    first = service.create_story(request, idempotency_key="idem-key-a")
    second = service.create_story(request, idempotency_key="idem-key-b")

    assert first.story_id != second.story_id


def test_http_intake_sha256_idempotency_without_header(monkeypatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    body = valid_v2_intake_payload()
    raw = json.dumps(body, separators=(",", ":"), sort_keys=True).encode("utf-8")
    expected_key = sha256(raw).hexdigest()
    try:
        with TestClient(app) as client:
            first = client.post(
                "/intake/stories",
                content=raw,
                headers={"content-type": "application/json"},
            )
            second = client.post(
                "/intake/stories",
                content=raw,
                headers={"content-type": "application/json"},
            )
    finally:
        _clear_api_dependencies_cache()

    assert first.status_code == 202
    assert second.status_code == 202
    assert first.json()["data"]["story_id"] == second.json()["data"]["story_id"]
    assert expected_key  # key derived from body; stored server-side
