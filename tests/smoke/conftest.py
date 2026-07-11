"""Shared fixtures for local real-HTTP smoke tests (REQ-41 GAP-41-01 / GAP-41-06)."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import httpx
import pytest

_SMOKE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SMOKE_DIR.parent.parent
_CANVAS_PATH = _SMOKE_DIR.parent / "sandbox" / "dogestonia_simulation_canvas_v0_1.json"
SCENARIO_GROUPS = ("infrastructure", "environment", "digital", "conflict")
_ENV_TEST_LOADED = False


def _load_env_file(path: Path, *, overwrite: bool) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and (overwrite or key not in os.environ):
            os.environ[key] = value


def _load_dotenv_test() -> None:
    global _ENV_TEST_LOADED
    if _ENV_TEST_LOADED:
        return
    _load_env_file(_REPO_ROOT / ".env.test", overwrite=True)
    _load_env_file(_REPO_ROOT / ".env", overwrite=False)
    _ENV_TEST_LOADED = True


def resolve_local_server_url() -> tuple[str, str]:
    """Resolve smoke target URL with product-approved gateway-only policy."""
    _load_dotenv_test()
    gateway = os.environ.get("GATEWAY_URL", "").strip()
    if gateway:
        return gateway.rstrip("/"), "GATEWAY_URL"
    return "", "UNSET"


def intake_auth_token() -> str | None:
    """Bearer token from .env.test — GATEWAY_API_TOKEN or SERVICE_API_TOKEN."""
    _load_dotenv_test()
    for name in ("GATEWAY_API_TOKEN", "SERVICE_API_TOKEN"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return None


def build_intake_headers(
    *,
    idempotency_key: str,
    trace_id: str | None = None,
    bearer_token: str | None = None,
) -> dict[str, str]:
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "idempotency-key": idempotency_key,
    }
    if trace_id is not None:
        headers["x-trace-id"] = trace_id
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    return headers


def smoke_browser_bearer_token() -> str | None:
    _load_dotenv_test()
    for name in ("GATEWAY_USER_TOKEN", "SMOKE_USER_BEARER_TOKEN"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return None


def post_intake_via_story_drafts_http(
    client: httpx.Client,
    *,
    json: dict[str, Any],
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Live HTTP: stash then browser submit (requires service + user bearer tokens)."""
    from tests.story_draft_intake_helpers import intake_payload_to_stash

    service_token = intake_auth_token()
    if not service_token:
        pytest.skip("GATEWAY_API_TOKEN or SERVICE_API_TOKEN required for smoke stash")
    user_token = smoke_browser_bearer_token()
    if not user_token:
        pytest.skip("GATEWAY_USER_TOKEN or SMOKE_USER_BEARER_TOKEN required for smoke submit")

    stash_headers = dict(headers or {})
    stash_headers.setdefault("Authorization", f"Bearer {service_token}")
    stash_headers.setdefault("Content-Type", "application/json")
    stash_payload = intake_payload_to_stash(json)
    stash_response = client.post("/story-drafts", json=stash_payload, headers=stash_headers)
    if stash_response.status_code != 201:
        return stash_response
    draft_id = stash_response.json()["data"]["draft_id"]
    submit_headers = {
        "Authorization": f"Bearer {user_token}",
        "Accept": "application/json",
    }
    if headers and headers.get("x-trace-id"):
        submit_headers["x-trace-id"] = headers["x-trace-id"]
    return client.post(f"/story-drafts/{draft_id}/submit", headers=submit_headers)


def post_story_draft_stash_http(
    client: httpx.Client,
    *,
    json: dict[str, Any],
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Live HTTP stash-only (GW-DRAFT-06 simulation_runner parity)."""
    from tests.story_draft_intake_helpers import intake_payload_to_stash

    service_token = intake_auth_token()
    if not service_token:
        pytest.skip("GATEWAY_API_TOKEN or SERVICE_API_TOKEN required for smoke stash")
    stash_headers = dict(headers or {})
    stash_headers.setdefault("Authorization", f"Bearer {service_token}")
    stash_headers.setdefault("Content-Type", "application/json")
    return client.post(
        "/story-drafts",
        json=intake_payload_to_stash(json),
        headers=stash_headers,
    )


def load_simulation_canvas() -> list[dict[str, Any]]:
    raw = json.loads(_CANVAS_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise TypeError(f"expected canvas list in {_CANVAS_PATH}")
    return raw


def first_scenario_for_group(group: str) -> dict[str, Any]:
    for scenario in load_simulation_canvas():
        if scenario.get("scenario_group") == group:
            return scenario
    raise LookupError(f"no scenario for group {group!r} in {_CANVAS_PATH}")


@pytest.fixture(scope="module")
def local_server_url() -> str:
    configured, _ = resolve_local_server_url()
    if not configured:
        pytest.fail("GATEWAY_URL must be set for smoke target resolution")
    base = configured.rstrip("/")
    try:
        health = httpx.get(f"{base}/health", timeout=3.0)
    except httpx.HTTPError as exc:
        pytest.skip(f"server not reachable: {exc}")
    if health.status_code != 200:
        pytest.skip(f"server not reachable: /health returned {health.status_code}")
    return base


@pytest.fixture(scope="module")
def local_server_url_source() -> str:
    _, source = resolve_local_server_url()
    return source


@pytest.fixture(scope="module")
def http_client(local_server_url: str) -> Iterator[httpx.Client]:
    with httpx.Client(base_url=local_server_url, timeout=30.0) as client:
        yield client
