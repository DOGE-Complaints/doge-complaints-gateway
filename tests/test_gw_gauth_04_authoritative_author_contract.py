"""GW-GAUTH-04: authoritative author from introspection `sub`."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.identity.authoritative_submitter import (
    authoritative_submitter_from_introspection,
    payload_submitter_mismatches_introspection,
    resolve_identity_issuer_from_introspect_url,
)
from core.identity.introspection_client import (
    IdentityIntrospectionClient,
    IntrospectionResult,
)
from core.intake.contracts import Submitter
from tests.conftest import (
    GAUTH_TEST_IDENTITY_SERVICE_TOKEN,
    GAUTH_TEST_IDENTITY_URL,
    GAUTH_TEST_SERVICE_TOKEN,
    gauth_intake_headers,
)
from tests.intake_v2_fixtures import valid_v2_intake_payload

GAUTH_TEST_SPA_VERIFY_BASE = "https://spa.test"
INTROSPECTION_SUB = "introspected-author-sub-99"
CLAIMED_PAYLOAD_SUB = "claimed-payload-sub-wrong"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("IDENTITY_INTROSPECT_URL", GAUTH_TEST_IDENTITY_URL)
    monkeypatch.setenv("IDENTITY_SERVICE_TOKEN", GAUTH_TEST_IDENTITY_SERVICE_TOKEN)
    monkeypatch.setenv("SPA_VERIFY_BASE_URL", GAUTH_TEST_SPA_VERIFY_BASE)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _valid_intake_payload(*, external_user_id: str = CLAIMED_PAYLOAD_SUB) -> dict[str, Any]:
    return valid_v2_intake_payload(
        submitter={
            "external_user_id": external_user_id,
            "identity_issuer": "https://idp.example.com/eid",
        },
        narrative={
            "original_text": "Pothole on main street.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Pothole"},
            "description": {"et": "d", "ru": "d", "en": "Pothole on main street."},
        },
    )


def _patch_introspect(
    monkeypatch: pytest.MonkeyPatch,
    *,
    result: IntrospectionResult,
) -> None:
    def _introspect(self: IdentityIntrospectionClient, user_token: str) -> IntrospectionResult:
        _ = user_token
        return result

    monkeypatch.setattr(IdentityIntrospectionClient, "introspect", _introspect)


def _latest_story_submitter_external_id() -> str:
    repo = get_api_dependencies().story_intake_service.repository
    stories = repo.list_stories()
    assert stories
    return stories[-1].submitter_external_user_id


def test_resolve_identity_issuer_from_introspect_url() -> None:
    assert (
        resolve_identity_issuer_from_introspect_url(GAUTH_TEST_IDENTITY_URL)
        == "https://identity.test"
    )
    assert resolve_identity_issuer_from_introspect_url(None) == "identity://gateway"


def test_authoritative_submitter_mapping_unit() -> None:
    payload = Submitter(
        external_user_id=CLAIMED_PAYLOAD_SUB,
        identity_issuer="https://idp.example.com/eid",
    )
    intro = IntrospectionResult(active=True, sub=INTROSPECTION_SUB, phone_verified=True)
    assert payload_submitter_mismatches_introspection(payload, intro) is True
    resolved = authoritative_submitter_from_introspection(
        payload_submitter=payload,
        introspection=intro,
        identity_introspect_url=GAUTH_TEST_IDENTITY_URL,
    )
    assert resolved.external_user_id == INTROSPECTION_SUB
    assert resolved.identity_issuer == "https://identity.test"


def test_verified_introspection_persists_sub_not_payload(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_introspect(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub=INTROSPECTION_SUB, phone_verified=True
        ),
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(extra={"idempotency-key": "gauth04-author-sub"}),
    )
    assert response.status_code == 202
    assert _latest_story_submitter_external_id() == INTROSPECTION_SUB
    assert _latest_story_submitter_external_id() != CLAIMED_PAYLOAD_SUB


def test_mismatch_payload_submitter_sub_wins(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_introspect(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub="authoritative-on-mismatch", phone_verified=True
        ),
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(external_user_id="different-claimed-id"),
        headers=gauth_intake_headers(extra={"idempotency-key": "gauth04-mismatch"}),
    )
    assert response.status_code == 202
    assert _latest_story_submitter_external_id() == "authoritative-on-mismatch"


def test_inactive_introspection_does_not_persist_payload_author(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = len(get_api_dependencies().story_intake_service.repository.list_stories())
    _patch_introspect(
        monkeypatch,
        result=IntrospectionResult(active=False, sub=INTROSPECTION_SUB),
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(extra={"idempotency-key": "gauth04-inactive"}),
    )
    assert response.status_code == 401
    assert len(get_api_dependencies().story_intake_service.repository.list_stories()) == before


def test_unverified_introspection_does_not_persist_payload_author(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = len(get_api_dependencies().story_intake_service.repository.list_stories())
    _patch_introspect(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub=INTROSPECTION_SUB, phone_verified=False
        ),
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(extra={"idempotency-key": "gauth04-unverified"}),
    )
    assert response.status_code == 403
    assert len(get_api_dependencies().story_intake_service.repository.list_stories()) == before
