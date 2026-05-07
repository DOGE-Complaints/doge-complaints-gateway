from __future__ import annotations

import logging
from collections.abc import Iterator
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.intake import INTAKE_SCHEMA_VERSION


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _valid_intake_payload() -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": "opaque-user-001"},
        "narrative": {
            "original_text": "Street lights are off for two nights.",
            "language": "en",
            "title_hint": "Street lights outage",
        },
        "origin": {"source": "spa_dashboard"},
    }


def test_intake_stories_endpoint_returns_success_envelope(client: TestClient) -> None:
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers={"x-trace-id": "trace-intake-200", "idempotency-key": "idem-1"},
    )

    assert response.status_code == 200
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
    monkeypatch.setenv("CLUSTER_SIGNAL_SOURCE", "narrative")
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
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    caplog.set_level(logging.DEBUG, logger="core.api")
    try:
        with TestClient(app) as client:
            response = client.post(
                "/intake/stories",
                json=_valid_intake_payload(),
                headers={"x-trace-id": "trace-cluster-pending", "idempotency-key": "idem-pending"},
            )
            assert response.status_code == 200
    finally:
        _clear_api_dependencies_cache()

    pending = [r for r in caplog.records if r.getMessage() == "story_cluster_issue_pending"]
    assert pending
    record = pending[-1]
    assert getattr(record, "story_id", None)
    assert getattr(record, "reason", None) == "cron_deferred"
    assert getattr(record, "outcome", None) == "not_clustered"


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
