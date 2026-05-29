from __future__ import annotations

import logging
from collections.abc import Iterator
from copy import deepcopy
from typing import Any

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
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


def _valid_intake_payload() -> dict[str, Any]:
    return valid_v2_intake_payload(
        submitter={
            "external_user_id": "opaque-user-001",
            "identity_issuer": "https://idp.example.com/eid",
        },
        narrative={
            "original_text": "Street lights are off for two nights.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "Tuled väljas", "ru": "Свет выключен", "en": "Street lights outage"},
            "description": {
                "et": "Kirjeldus",
                "ru": "Описание",
                "en": "Lights off for two nights.",
            },
        },
        origin={"source": "spa_dashboard"},
    )


def test_intake_stories_endpoint_returns_success_envelope(client: TestClient) -> None:
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers={"x-trace-id": "trace-intake-200", "idempotency-key": "idem-1"},
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["trace_id"] == "trace-intake-200"
    assert payload["data"]["schema_version"] == "m2.story_intake_response.v1"
    assert payload["data"]["story_id"]
    assert payload["data"]["status"] == "ready_for_profile"


def test_intake_does_not_trigger_sync_clustering_logs(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    monkeypatch.setenv("CLUSTER_SIGNAL_SOURCE", "canonical")
    _clear_api_dependencies_cache()
    caplog.set_level(logging.INFO, logger="core.api")
    base = _valid_intake_payload()
    base["narrative"]["original_text"] = "Road damage and broken street surface near district center."
    first = deepcopy(base)
    first["submitter"] = {"external_user_id": "cluster-log-user-a"}
    second = deepcopy(base)
    second["submitter"] = {"external_user_id": "cluster-log-user-b"}
    try:
        with TestClient(app) as client:
            client.post(
                "/intake/stories",
                json=first,
                headers={"x-trace-id": "trace-cluster-a", "idempotency-key": "idem-cluster-a"},
            )
            client.post(
                "/intake/stories",
                json=second,
                headers={"x-trace-id": "trace-cluster-b", "idempotency-key": "idem-cluster-b"},
            )
    finally:
        _clear_api_dependencies_cache()

    triggered = [
        r
        for r in caplog.records
        if r.getMessage() in {"story_intake_cluster_triggered_issue", "story_intake_cluster_no_issue"}
    ]
    assert triggered == []


def test_intake_emits_cluster_pending_observability_event(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    try:
        with TestClient(app) as client:
            response = client.post(
                "/intake/stories",
                json=_valid_intake_payload(),
                headers={"x-trace-id": "trace-cluster-pending", "idempotency-key": "idem-pending"},
            )
            assert response.status_code == 202
    finally:
        _clear_api_dependencies_cache()

    captured = capsys.readouterr()
    assert "story.persistence_backend_selected backend=in_memory" in captured.out
    assert "story.persistence_commit_ack backend=in_memory lifecycle_status=ready_for_profile" in captured.out
    assert "story_cluster_issue_pending" in captured.out
    assert "trace-cluster-pending" in captured.out
    assert "story.pipeline_outcome" in captured.out


def test_intake_stories_endpoint_returns_400_for_unsupported_session_language(
    client: TestClient,
) -> None:
    invalid_payload = _valid_intake_payload()
    invalid_payload["narrative"]["session_language"] = "de"

    response = client.post(
        "/intake/stories",
        json=invalid_payload,
        headers={"x-trace-id": "trace-intake-session-lang-400"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["trace_id"] == "trace-intake-session-lang-400"
    assert payload["error"]["code"] == "DOMAIN_ERROR"
    assert "Supported values: et, ru, en" in payload["error"]["message"]


def test_intake_stories_endpoint_returns_400_for_validation_error(
    client: TestClient,
) -> None:
    invalid_payload = _valid_intake_payload()
    invalid_payload.pop("narrative")

    response = client.post(
        "/intake/stories",
        json=invalid_payload,
        headers={"x-trace-id": "trace-intake-400"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["trace_id"] == "trace-intake-400"
    assert payload["error"]["code"] == "DOMAIN_ERROR"
    assert payload["error"]["type"] == "domain"
    assert "narrative" in payload["error"]["message"]
