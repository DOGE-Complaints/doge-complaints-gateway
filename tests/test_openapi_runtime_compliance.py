from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.intake import INTAKE_SCHEMA_VERSION
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict


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
    # only local component refs are expected in this contract.
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
    assert "/intake/stories" in spec["paths"]
    assert "post" in spec["paths"]["/intake/stories"]

    intake_post = spec["paths"]["/intake/stories"]["post"]
    # Current runtime exposes a lightweight OpenAPI operation without explicit requestBody.
    assert "requestBody" not in intake_post
    assert "200" in intake_post["responses"]


def test_openapi_response_contract_matches_runtime_envelope_shape(
    client: TestClient,
) -> None:
    spec = client.get("/openapi.json").json()
    intake_post = spec["paths"]["/intake/stories"]["post"]
    ok_response_schema = intake_post["responses"]["200"]["content"]["application/json"]["schema"]
    envelope_schema = _resolve_ref(spec, ok_response_schema)
    envelope_props = set(envelope_schema.get("properties", {}).keys())

    response = client.post(
        "/intake/stories",
        json={
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {"external_user_id": "openapi-runtime-user", "identity_issuer": "https://idp.example.com/eid"},
            "narrative": {
            "original_text": "OpenAPI runtime compliance check",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "OpenAPI check"},
            "description": {"et": "d", "ru": "d", "en": "OpenAPI runtime compliance check"},
            },
        },
    )
    assert response.status_code == 202
    payload = response.json()

    # If OpenAPI response schema is empty, we still enforce runtime envelope contract.
    if envelope_props:
        assert envelope_props.issubset(set(payload.keys()))
    else:
        assert {"trace_id", "data"}.issubset(set(payload.keys()))
    assert payload["data"]["schema_version"] == "m2.story_intake_response.v1"
