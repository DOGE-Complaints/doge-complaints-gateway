"""HTTP helpers replacing legacy POST /intake/stories (GW-DRAFT-06)."""

from __future__ import annotations

import json
from copy import deepcopy
import os
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from core.identity.introspection_result import IntrospectionResult
from core.identity.me_client import IdentityMeClient
from tests.conftest import GAUTH_TEST_SERVICE_TOKEN, GAUTH_TEST_USER_TOKEN


def intake_payload_to_stash(payload: dict[str, Any]) -> dict[str, Any]:
    stash = deepcopy(payload)
    stash.pop("submitter", None)
    return stash


def submitter_external_id(payload: dict[str, Any]) -> str:
    submitter = payload.get("submitter") or {}
    if isinstance(submitter, dict):
        ext = submitter.get("external_user_id")
        if isinstance(ext, str) and ext.strip():
            return ext.strip()
    return "draft-intake-test-sub"


def patch_identity_me_verified(
    monkeypatch: pytest.MonkeyPatch,
    *,
    sub: str,
    phone_verified: bool = True,
) -> None:
    def _fetch_me(self: IdentityMeClient, bearer_token: str) -> IntrospectionResult:
        _ = bearer_token
        return IntrospectionResult(active=True, sub=sub, phone_verified=phone_verified)

    monkeypatch.setattr(IdentityMeClient, "fetch_me", _fetch_me)


def service_auth_headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    token = os.environ.get("SERVICE_API_TOKEN") or GAUTH_TEST_SERVICE_TOKEN
    headers = {"Authorization": f"Bearer {token}"}
    if extra:
        headers.update(extra)
    return headers


def browser_auth_headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    headers = {"Authorization": f"Bearer {GAUTH_TEST_USER_TOKEN}"}
    if extra:
        headers.update(extra)
    return headers


def stash_story_draft(
    client: TestClient,
    payload: dict[str, Any],
    *,
    headers: dict[str, str] | None = None,
) -> str:
    response = client.post(
        "/story-drafts",
        json=intake_payload_to_stash(payload),
        headers=service_auth_headers(headers),
    )
    if response.status_code != 201:
        raise AssertionError(response.text)
    return response.json()["data"]["draft_id"]


def submit_story_draft(
    client: TestClient,
    draft_id: str,
    *,
    headers: dict[str, str] | None = None,
) -> Any:
    return client.post(
        f"/story-drafts/{draft_id}/submit",
        headers=browser_auth_headers(headers),
    )


def _resolve_intake_body(
    *,
    json: dict[str, Any] | None,
    content: bytes | None,
) -> dict[str, Any]:
    if json is not None:
        return json
    if content is not None:
        parsed = json.loads(content.decode("utf-8"))
        if isinstance(parsed, dict):
            return parsed
    raise ValueError("post_intake_via_story_drafts requires json= or content=")


def post_intake_via_story_drafts(
    client: TestClient,
    url: str = "/story-drafts",
    *,
    json: dict[str, Any] | None = None,
    content: bytes | None = None,
    headers: dict[str, str] | None = None,
    monkeypatch: pytest.MonkeyPatch | None = None,
) -> Any:
    """Stash + browser submit; drop-in for legacy client.post('/intake/stories', ...)."""
    _ = url
    body = _resolve_intake_body(json=json, content=content)
    sub = submitter_external_id(body)

    def _fetch_me(self: IdentityMeClient, bearer_token: str) -> IntrospectionResult:
        _ = bearer_token
        return IntrospectionResult(active=True, sub=sub, phone_verified=True)

    stash_response = client.post(
        "/story-drafts",
        json=intake_payload_to_stash(body),
        headers=service_auth_headers(headers),
    )
    if stash_response.status_code != 201:
        return stash_response
    draft_id = stash_response.json()["data"]["draft_id"]

    if monkeypatch is not None:
        patch_identity_me_verified(monkeypatch, sub=sub)
        return submit_story_draft(client, draft_id, headers=headers)

    with patch.object(IdentityMeClient, "fetch_me", _fetch_me):
        return submit_story_draft(client, draft_id, headers=headers)
