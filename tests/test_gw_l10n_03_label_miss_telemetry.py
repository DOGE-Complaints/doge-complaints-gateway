"""GW-L10N-03 acceptance tests — label miss telemetry sink."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.api.dependencies import ApiDependencies, build_api_dependencies
from core.infrastructure.repositories import InMemoryLabelTranslationMissStore
from core.telemetry.label_miss import parse_label_miss_payload, LabelMissValidationError


def test_parse_label_miss_payload_valid() -> None:
    assert parse_label_miss_payload({"label_key": "roads", "locale": "et"}) == (
        "roads",
        "et",
    )


def test_parse_label_miss_payload_rejects_invalid() -> None:
    with pytest.raises(LabelMissValidationError):
        parse_label_miss_payload({"label_key": "", "locale": "et"})
    with pytest.raises(LabelMissValidationError):
        parse_label_miss_payload({"label_key": "roads", "locale": "de"})
    with pytest.raises(LabelMissValidationError):
        parse_label_miss_payload([])


def test_in_memory_store_aggregates_repeats() -> None:
    store = InMemoryLabelTranslationMissStore()
    store.record_miss("roads", "ru")
    store.record_miss("roads", "ru")
    assert store.get_miss_count("roads", "ru") == 2


@dataclass
class _FailingLabelMissStore:
    def record_miss(self, label_key: str, locale: str) -> None:
        raise RuntimeError("store unavailable")

    def get_miss_count(self, label_key: str, locale: str) -> int:
        return 0


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_post_label_miss_accepts_without_auth(client: TestClient) -> None:
    response = client.post(
        "/telemetry/label-misses",
        json={"label_key": "roads", "locale": "et"},
    )
    assert response.status_code == 202
    body = response.json()
    assert body["data"]["accepted"] is True
    assert "trace_id" in body

    store = get_api_dependencies().label_translation_miss_store
    assert store is not None
    assert store.get_miss_count("roads", "et") == 1


def test_post_label_miss_invalid_payload_returns_soft_400(client: TestClient) -> None:
    response = client.post(
        "/telemetry/label-misses",
        json={"label_key": "", "locale": "et"},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Invalid request"
    assert body["error"]["details"] == {}


def test_post_label_miss_store_failure_returns_202_degraded(client: TestClient) -> None:
    base = build_api_dependencies()
    failing_deps = ApiDependencies(
        health_service=base.health_service,
        story_intake_service=base.story_intake_service,
        story_cluster_orchestrator=base.story_cluster_orchestrator,
        issue_create_service=base.issue_create_service,
        issue_projection_read_store=base.issue_projection_read_store,
        network_pulse_service=base.network_pulse_service,
        config=base.config,
        service_auth=base.service_auth,
        metrics=base.metrics,
        db_backend=base.db_backend,
        db_ready=base.db_ready,
        db_checks=base.db_checks,
        label_translation_miss_store=_FailingLabelMissStore(),  # type: ignore[arg-type]
    )
    app.dependency_overrides[get_api_dependencies] = lambda: failing_deps
    try:
        response = client.post(
            "/telemetry/label-misses",
            json={"label_key": "roads", "locale": "ru"},
        )
        assert response.status_code == 202
        assert response.json()["data"]["accepted"] is False

        health = client.get("/health")
        assert health.status_code == 200
    finally:
        app.dependency_overrides.clear()
        _clear_api_dependencies_cache()
