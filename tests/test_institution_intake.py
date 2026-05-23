from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.application import StoryPromotionProjectionBridge
from core.application.services import StoryIntakeService
from core.infrastructure.repositories import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import IntakeValidationError, parse_story_intake_request
from core.projection import project_distinct_issue
from tests.intake_v2_fixtures import valid_v2_intake_payload

_INSTITUTION = {
    "et": "Tallinna Linnavalitsus",
    "ru": "Таллинская городская управа",
    "en": "Tallinn City Government",
}


@pytest.fixture()
def sqlite_client(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'institution.sqlite'}")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _payload_with_institution(**institution_overrides: str) -> dict[str, Any]:
    return valid_v2_intake_payload(
        narrative={"institution": {**_INSTITUTION, **institution_overrides}}
    )


def test_parse_institution_valid_i18n_dict() -> None:
    request = parse_story_intake_request(_payload_with_institution())
    assert request.narrative.institution == _INSTITUTION


def test_parse_omits_institution_when_key_absent() -> None:
    payload = valid_v2_intake_payload()
    assert "institution" not in payload["narrative"]
    request = parse_story_intake_request(payload)
    assert request.narrative.institution is None


def test_parse_incomplete_institution_raises() -> None:
    with pytest.raises(IntakeValidationError, match="institution"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={"institution": {"et": "only-et", "ru": "", "en": "en"}}
            )
        )


def test_intake_with_institution_returns_202_and_persists_sqlite(
    sqlite_client: TestClient,
) -> None:
    response = sqlite_client.post(
        "/intake/stories",
        json=_payload_with_institution(),
        headers={"x-trace-id": "trace-inst-1", "idempotency-key": "idem-inst-1"},
    )
    assert response.status_code == 202
    story_id = response.json()["data"]["story_id"]

    record = get_api_dependencies().story_intake_service.repository.get_story(story_id)
    assert record is not None
    assert record.narrative_institution == _INSTITUTION


def test_intake_without_institution_leaves_column_null(
    sqlite_client: TestClient,
) -> None:
    response = sqlite_client.post(
        "/intake/stories",
        json=valid_v2_intake_payload(),
        headers={"x-trace-id": "trace-inst-none", "idempotency-key": "idem-inst-none"},
    )
    assert response.status_code == 202
    story_id = response.json()["data"]["story_id"]

    record = get_api_dependencies().story_intake_service.repository.get_story(story_id)
    assert record is not None
    assert record.narrative_institution is None


def test_intake_invalid_institution_returns_400(sqlite_client: TestClient) -> None:
    response = sqlite_client.post(
        "/intake/stories",
        json=valid_v2_intake_payload(
            narrative={"institution": {"et": "x", "ru": "y"}}
        ),
        headers={"x-trace-id": "trace-inst-bad", "idempotency-key": "idem-inst-bad"},
    )
    assert response.status_code == 400


def test_bridge_projection_institution_roundtrip_from_dominant_story() -> None:
    story_repository = InMemoryStoryRepository()
    intake_service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )
    story = intake_service.create_story(parse_story_intake_request(_payload_with_institution()))
    bridge = StoryPromotionProjectionBridge(story_repository=story_repository)
    projection_input = bridge.build_projection_input(
        issue_id="issue-inst-1",
        promoted_title="Institution propagation",
        story_ids=(story.story_id,),
    )
    assert projection_input.institution == _INSTITUTION

    issue = project_distinct_issue(projection_input)
    assert issue.to_public_dict()["institution"] == _INSTITUTION
