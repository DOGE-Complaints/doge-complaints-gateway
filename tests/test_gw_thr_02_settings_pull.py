"""GW-THR-02: service-auth active pack shell settings pull."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.config import ConfigError
from core.schema import SchemaRef
from core.schema.resolver import resolve_pack
from core.schema.shell_capabilities import (
    CAP_VERIFICATION_VALIDATION_TYPE,
    SHELL_CAPABILITIES_FILENAME,
    write_shell_capabilities,
)
from core.schema.shell_settings import (
    PACK_SHELL_SETTINGS_KEY,
    assert_no_story_narrative,
    build_active_pack_shell_settings,
    shell_capabilities_to_settings_dict,
)
from tests.conftest import GAUTH_TEST_SERVICE_TOKEN, gauth_intake_headers
from tests.test_gw_thr_01_pack_shell_required import _write_fixture_pack

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("NODE_SCHEMA_ID", "tallinn_civic")
    monkeypatch.setenv("NODE_SCHEMA_VERSION", "v1")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


@pytest.mark.gauth_raw_client
def test_shell_settings_requires_service_auth(client: TestClient) -> None:
    response = client.get("/node/shell-settings")
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["code"] == "UNAUTHORIZED"


def test_shell_settings_happy_path_returns_capabilities(client: TestClient) -> None:
    response = client.get(
        "/node/shell-settings",
        headers=gauth_intake_headers(),
    )
    assert response.status_code == 200
    data = response.json()["data"]
    settings = data[PACK_SHELL_SETTINGS_KEY]
    assert settings["active_schema"]["schema_id"] == "tallinn_civic"
    assert settings["verification"]["validation_type"] == "phone"
    assert settings["verification"]["integration_name"] == "tallinn_phone_sms"
    assert settings["threads"]["tree"]["max_depth"] >= 1
    assert "enable" in settings["threads"]["reactions"]
    assert "image/jpeg" in settings["threads"]["media"]["allowed_types"]
    assert_no_story_narrative(data)
    # No Story narrative / ThreadContext composition keys.
    blob = json.dumps(data)
    for banned in ("story_body", "original_text", "thread_context", "ThreadContext"):
        assert banned not in blob


def test_shell_settings_not_in_public_routes() -> None:
    from core.api.asgi_app import PUBLIC_ROUTES

    assert "/node/shell-settings" not in PUBLIC_ROUTES
    assert not any(r.endswith("ThreadContext") or "thread-context" in r for r in PUBLIC_ROUTES)


def test_public_issue_get_remains_civic_projection(client: TestClient) -> None:
    """AC-GW-THR02-05: knobs not required inside Issue get."""
    response = client.get("/node/issues/nonexistent-issue-id")
    # 404 or 200 depending on store; shape must stay issue-centric when success.
    body = response.json()
    if response.status_code == 200:
        assert "issue" in body["data"]
        assert PACK_SHELL_SETTINGS_KEY not in body["data"]
        assert "thread_context" not in body["data"]
    else:
        assert "error" in body


def test_build_settings_from_warehouse_pack() -> None:
    ctx = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    payload = shell_capabilities_to_settings_dict(
        ctx.shell_capabilities,
        schema_id="tallinn_civic",
        schema_version="v1",
    )
    assert payload[PACK_SHELL_SETTINGS_KEY]["verification"]["validation_type"] == "phone"


def test_incomplete_pack_fail_closed(tmp_path: Path) -> None:
    pack_dir = _write_fixture_pack(tmp_path)
    path = pack_dir / SHELL_CAPABILITIES_FILENAME
    body = json.loads(path.read_text(encoding="utf-8"))
    body["entries"] = [
        e for e in body["entries"] if e["id"] != CAP_VERIFICATION_VALIDATION_TYPE
    ]
    path.write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(ConfigError, match="shell capabilities|missing mandatory"):
        build_active_pack_shell_settings(
            schema_id="fixture_shell",
            schema_version="v1",
            environ={"SCHEMA_PACKS_ROOT": str(tmp_path)},
        )


def test_missing_sidecar_fail_closed(tmp_path: Path) -> None:
    _write_fixture_pack(tmp_path, with_shell=False)
    with pytest.raises(ConfigError, match="shell capabilities"):
        build_active_pack_shell_settings(
            schema_id="fixture_shell",
            schema_version="v1",
            environ={"SCHEMA_PACKS_ROOT": str(tmp_path)},
        )


def test_no_client_chosen_pack_id_in_builder(tmp_path: Path) -> None:
    """Active pair only — builder takes schema_id/version from caller (config), not body."""
    _write_fixture_pack(tmp_path, schema_id="fixture_shell")
    write_shell_capabilities(
        tmp_path / "fixture_shell" / "v1",
        validation_type="phone",
        integration_name="fixture_phone_sms",
    )
    payload = build_active_pack_shell_settings(
        schema_id="fixture_shell",
        schema_version="v1",
        environ={"SCHEMA_PACKS_ROOT": str(tmp_path)},
    )
    assert payload[PACK_SHELL_SETTINGS_KEY]["active_schema"]["schema_id"] == "fixture_shell"


@pytest.mark.gauth_raw_client
def test_shell_settings_wrong_token_denied(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("NODE_SCHEMA_ID", "tallinn_civic")
    monkeypatch.setenv("NODE_SCHEMA_VERSION", "v1")
    _clear_api_dependencies_cache()
    with TestClient(app) as client:
        response = client.get(
            "/node/shell-settings",
            headers={"Authorization": "Bearer wrong-token"},
        )
    _clear_api_dependencies_cache()
    assert response.status_code == 401
