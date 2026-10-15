"""GW-REQ57-04: manual regenerate service-auth (HTTP double, no live aibridge)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.application.sense_brief_nudge import (
    ACCEPT_PATH,
    SenseBriefNudgeService,
    SenseBriefNudgeSettings,
)
from core.application.sense_brief_regenerate import (
    SenseBriefRegenerateService,
    bump_generation_version,
    mark_regenerate_pending,
)
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from tests.civic_pack_overrides import monkeypatch_civic_knobs

_TOKEN = "req57-04-service-token"
_S2S = "req57-04-worker-s2s-token"
_CITIZEN = "citizen-oauth-bearer-not-service"


class _RecordingTransport:
    def __init__(self, *, status_code: int = 200) -> None:
        self.status_code = status_code
        self.calls: list[dict[str, Any]] = []

    def post_json(
        self,
        *,
        url: str,
        headers: dict[str, str],
        body: dict[str, Any],
        timeout_s: float,
    ) -> httpx.Response:
        self.calls.append(
            {"url": url, "headers": dict(headers), "body": dict(body), "timeout_s": timeout_s}
        )
        return httpx.Response(self.status_code, json={"ok": True, "idempotent": False})


def test_req57_04_bump_generation_version_distinct() -> None:
    assert bump_generation_version("v1") == "v2"
    assert bump_generation_version("v2") == "v3"
    assert bump_generation_version("custom") == "custom.regen2"
    assert bump_generation_version("custom.regen2") == "custom.regen3"
    assert bump_generation_version("v1") != "v1"


def test_req57_04_mark_regenerate_keeps_brief_title() -> None:
    pending = mark_regenerate_pending(
        {
            "id": "issue-x",
            "generation_status": "ready",
            "generation_version": "v1",
            "poster_url": "https://cdn.example/p.png",
            "title": {"en": "Brief title", "et": "Brief title", "ru": "Brief title"},
            "summary": {"en": "Brief summary"},
        },
        generation_version="v2",
    )
    assert pending["generation_status"] == "pending"
    assert pending["generation_version"] == "v2"
    assert pending["title"]["en"] == "Brief title"
    assert "poster_url" not in pending  # public omit while not ready


def test_req57_04_unit_regenerate_bumps_pending_and_nudges() -> None:
    store = InMemoryIssueProjectionStore()
    store.save_projection(
        issue_id="issue-req57-04-unit",
        status="PUBLISHED",
        payload={
            "id": "issue-req57-04-unit",
            "status": "PUBLISHED",
            "type": "INCIDENT",
            "labels": ["infrastructure"],
            "title": {"et": "t", "ru": "t", "en": "Ready brief"},
            "summary": {"et": "s", "ru": "s", "en": "Ready brief summary"},
            "description": {"et": "d", "ru": "d", "en": "d"},
            "generation_status": "ready",
            "generation_version": "v1",
            "poster_url": "https://cdn.example/poster.png",
        },
        policy_version="m3.doge_issue_derivation.v1",
    )
    transport = _RecordingTransport()
    nudge = SenseBriefNudgeService(
        settings=SenseBriefNudgeSettings(
            enabled=True,
            base_url="https://aibridge.test",
            s2s_token=_S2S,
            timeout_s=5.0,
        ),
        transport=transport,
    )
    service = SenseBriefRegenerateService(store=store, nudge_service=nudge)
    result = service.regenerate(issue_id="issue-req57-04-unit")
    assert result.generation_version == "v2"
    assert result.projection["generation_status"] == "pending"
    assert result.projection["generation_version"] == "v2"
    assert result.projection["title"]["en"] == "Ready brief"
    assert len(transport.calls) == 1
    call = transport.calls[0]
    assert call["url"] == f"https://aibridge.test{ACCEPT_PATH}"
    assert call["headers"]["Authorization"] == f"Bearer {_S2S}"
    assert call["body"]["issue_id"] == "issue-req57-04-unit"
    assert call["body"]["generation_version"] == "v2"
    assert call["body"]["generation_version"] != "v1"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch_civic_knobs(monkeypatch, min_size=1, readiness_threshold=1)
    monkeypatch.setenv("SERVICE_API_TOKEN", _TOKEN)
    monkeypatch.setenv("AIBRIDGE_BASE_URL", "https://aibridge.test")
    monkeypatch.setenv("AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN", _S2S)
    monkeypatch.setenv("AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED", "true")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _service_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {_TOKEN}"}


def _seed_ready_issue(issue_id: str = "issue-req57-04") -> None:
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    store.save_projection(
        issue_id=issue_id,
        status="PUBLISHED",
        payload={
            "id": issue_id,
            "status": "PUBLISHED",
            "type": "INCIDENT",
            "labels": ["infrastructure"],
            "title": {"et": "Brief", "ru": "Brief", "en": "Brief"},
            "summary": {"et": "s", "ru": "s", "en": "Brief summary"},
            "description": {"et": "d", "ru": "d", "en": "d"},
            "generation_status": "ready",
            "generation_version": "v1",
            "poster_url": "https://cdn.example/poster.png",
        },
        policy_version="m3.doge_issue_derivation.v1",
    )


def _inject_recording_nudge(transport: _RecordingTransport) -> None:
    deps = get_api_dependencies()
    object.__setattr__(
        deps.issue_create_service,
        "sense_brief_nudge_service",
        SenseBriefNudgeService(
            settings=SenseBriefNudgeSettings(
                enabled=True,
                base_url="https://aibridge.test",
                s2s_token=_S2S,
                timeout_s=5.0,
            ),
            transport=transport,
        ),
    )


def test_req57_04_asgi_service_token_bumps_pending_and_nudges(
    client: TestClient,
) -> None:
    """AC-01 + AC-04: service token → bump + pending + nudge with distinct version."""
    _seed_ready_issue()
    transport = _RecordingTransport()
    _inject_recording_nudge(transport)

    response = client.post(
        "/v1/issue-sense-brief/regenerate",
        headers=_service_headers(),
        json={"issue_id": "issue-req57-04"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["generation_version"] == "v2"
    assert data["issue"]["generation_status"] == "pending"
    assert data["issue"]["generation_version"] == "v2"
    assert data["issue"]["title"]["en"] == "Brief"
    assert len(transport.calls) == 1
    assert transport.calls[0]["body"]["generation_version"] == "v2"
    assert transport.calls[0]["body"]["generation_version"] != "v1"


def test_req57_04_asgi_missing_auth_rejected(client: TestClient) -> None:
    """AC-02: without service auth → rejected."""
    _seed_ready_issue("issue-req57-04-noauth")
    response = client.post(
        "/v1/issue-sense-brief/regenerate",
        json={"issue_id": "issue-req57-04-noauth"},
    )
    assert response.status_code == 401


def test_req57_04_asgi_citizen_bearer_rejected(client: TestClient) -> None:
    """AC-03: citizen Bearer cannot regenerate."""
    _seed_ready_issue("issue-req57-04-citizen")
    response = client.post(
        "/v1/issue-sense-brief/regenerate",
        headers={"Authorization": f"Bearer {_CITIZEN}"},
        json={"issue_id": "issue-req57-04-citizen"},
    )
    assert response.status_code == 401


def test_req57_04_asgi_empty_issue_id_rejected(client: TestClient) -> None:
    """G4: empty issue_id + service token → 400."""
    transport = _RecordingTransport()
    _inject_recording_nudge(transport)
    response = client.post(
        "/v1/issue-sense-brief/regenerate",
        headers=_service_headers(),
        json={"issue_id": ""},
    )
    assert response.status_code == 400
    assert transport.calls == []


def test_req57_04_asgi_unknown_issue_id_rejected(client: TestClient) -> None:
    """G4: unknown issue_id + service token → 400."""
    transport = _RecordingTransport()
    _inject_recording_nudge(transport)
    response = client.post(
        "/v1/issue-sense-brief/regenerate",
        headers=_service_headers(),
        json={"issue_id": "issue-req57-04-does-not-exist"},
    )
    assert response.status_code == 400
    assert transport.calls == []
