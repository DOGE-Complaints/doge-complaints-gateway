from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.intake import INTAKE_SCHEMA_VERSION
from tests.story_draft_intake_helpers import post_intake_via_story_drafts


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _resolve_ref(spec: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    ref = schema.get("$ref")
    if not isinstance(ref, str):
        return schema
    path = ref.removeprefix("#/").split("/")
    cursor: Any = spec
    for segment in path:
        cursor = cursor[segment]
    return cursor


def test_openapi_contains_required_runtime_paths_and_request_contract(
    client: TestClient,
) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    spec = response.json()
    assert str(spec.get("openapi", "")).startswith("3.")

    assert "/health" in spec["paths"]
    assert "get" in spec["paths"]["/health"]
    assert "/story-drafts" in spec["paths"]
    assert "post" in spec["paths"]["/story-drafts"]
    assert "/intake/stories" not in spec["paths"]

    stash_post = spec["paths"]["/story-drafts"]["post"]
    assert "post" in spec["paths"]["/story-drafts"]
    assert "201" in stash_post["responses"] or "200" in stash_post["responses"]


def test_openapi_response_contract_matches_runtime_envelope_shape(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spec = client.get("/openapi.json").json()
    submit_post = spec["paths"]["/story-drafts/{draft_id}/submit"]["post"]
    success_code = "202" if "202" in submit_post["responses"] else "200"
    ok_response_schema = submit_post["responses"][success_code]["content"]["application/json"]["schema"]
    envelope_schema = _resolve_ref(spec, ok_response_schema)
    envelope_props = set(envelope_schema.get("properties", {}).keys())

    response = post_intake_via_story_drafts(
        client,
        json={
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {
                "external_user_id": "openapi-runtime-user",
                "identity_issuer": "https://idp.example.com/eid",
            },
            "narrative": {
                "original_text": "OpenAPI runtime compliance check",
                "language": "en",
                "session_language": "en",
                "title": {"et": "t", "ru": "t", "en": "OpenAPI check"},
                "description": {"et": "d", "ru": "d", "en": "OpenAPI runtime compliance check"},
            },
        },
        monkeypatch=monkeypatch,
    )
    assert response.status_code == 202
    payload = response.json()

    if envelope_props:
        assert envelope_props.issubset(set(payload.keys()))
    else:
        assert {"trace_id", "data"}.issubset(set(payload.keys()))
    assert payload["data"]["schema_version"] == "m2.story_intake_response.v1"
