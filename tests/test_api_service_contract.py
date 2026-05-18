from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.infrastructure.providers import provide_app_config, provide_service_factory
from core.infrastructure.repositories import InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION, IntakeValidationError, parse_story_intake_request
from tests.intake_v2_fixtures import valid_v2_intake_payload


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _minimal_valid_payload() -> dict[str, Any]:
    return valid_v2_intake_payload(
        submitter={
            "external_user_id": "u-001",
            "identity_issuer": "https://idp.example.com/eid",
        },
        narrative={
            "original_text": "Katki sillal on auk",
            "language": "et",
            "session_language": "et",
            "title": {"et": "Katki sild", "ru": "Мост", "en": "Broken bridge"},
            "description": {"et": "Kirjeldus", "ru": "Описание", "en": "Description"},
        },
    )


def test_parse_minimal_valid_payload() -> None:
    """REQ-39 E-01: parse_story_intake_request accepts minimal v2 payload."""
    result = parse_story_intake_request(_minimal_valid_payload())
    assert result.schema_version == INTAKE_SCHEMA_VERSION
    assert result.submitter.external_user_id == "u-001"
    assert result.narrative.language == "et"
    assert result.narrative.location_query is None
    assert result.narrative.canonical_type is None
    assert result.narrative.canonical_labels == ()


def test_wrong_schema_version_raises_intake_validation_error() -> None:
    """REQ-39 E-02: bad schema_version → IntakeValidationError."""
    payload = _minimal_valid_payload()
    payload["schema_version"] = "v99.wrong"
    with pytest.raises(IntakeValidationError):
        parse_story_intake_request(payload)


@pytest.mark.parametrize("lang", ["fr", "ee", "", "EST", "english"])
def test_invalid_language_raises_intake_validation_error(lang: str) -> None:
    """REQ-39 E-03: unsupported narrative.language rejected at parse."""
    payload = _minimal_valid_payload()
    payload["narrative"]["language"] = lang
    with pytest.raises(IntakeValidationError):
        parse_story_intake_request(payload)


def test_invalid_payload_returns_422_not_500(client: TestClient) -> None:
    """REQ-39 E-04: handler maps validation errors to 4xx, not 500."""
    resp = client.post("/intake/stories", json={"schema_version": "wrong"})
    assert resp.status_code != 500
    assert resp.status_code in (400, 422)
    body = resp.json()
    assert "error" in body or "detail" in body


def test_idempotency_key_deduplicates_story(client: TestClient) -> None:
    """REQ-39 E-05: same idempotency-key returns same story_id."""
    payload = _minimal_valid_payload()
    headers = {"idempotency-key": "test-key-001"}
    resp1 = client.post("/intake/stories", json=payload, headers=headers)
    resp2 = client.post("/intake/stories", json=payload, headers=headers)
    assert resp1.status_code == 202
    assert resp2.status_code == 202
    assert resp1.json()["data"]["story_id"] == resp2.json()["data"]["story_id"]


def test_api_dependencies_wires_correct_repo_for_in_memory() -> None:
    """REQ-39 E-06: in_memory backend → InMemoryStoryRepository."""
    config = provide_app_config(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "https://demo.example/api",
            "DB_BACKEND": "in_memory",
        }
    )
    factory = provide_service_factory(config)
    svc = factory.get_story_intake_service()
    assert isinstance(svc.repository, InMemoryStoryRepository)


def test_payload_with_consistency_notes_parses_without_error() -> None:
    """REQ-39 E-07: GAP-06 consistency_notes accepted by parser."""
    result = parse_story_intake_request(
        valid_v2_intake_payload(
            live_story_context={"consistency_notes": "duplicate of #123"},
        )
    )
    assert result.live_story_context is not None
    assert result.live_story_context.consistency_notes == "duplicate of #123"


def test_canonical_labels_parsed_as_tuple() -> None:
    """REQ-39 E-08: canonical_labels normalized to tuple."""
    result = parse_story_intake_request(
        valid_v2_intake_payload(
            narrative={
                "canonical_labels": ["infrastructure", "transport"],
            },
        )
    )
    assert result.narrative.canonical_labels == ("infrastructure", "transport")
    assert isinstance(result.narrative.canonical_labels, tuple)
