from __future__ import annotations

from collections.abc import Iterator

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import PROTECTED_ROUTES, PUBLIC_ROUTES, _clear_api_dependencies_cache, app


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", "transport-secret")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_route_policy_map_is_explicit() -> None:
    assert "/health" in PUBLIC_ROUTES
    assert "/ready" in PUBLIC_ROUTES
    assert "/protected/status" in PROTECTED_ROUTES
    assert "/metrics" in PROTECTED_ROUTES


def test_transport_public_smoke(client: TestClient) -> None:
    health = client.get("/health", headers={"x-trace-id": "http-health"})
    ready = client.get("/ready", headers={"x-trace-id": "http-ready"})

    assert health.status_code == 200
    assert ready.status_code == 200
    assert health.headers["content-type"].startswith("application/json")
    assert ready.headers["content-type"].startswith("application/json")
    assert health.json()["data"]["status"] == "ok"
    assert ready.json()["data"]["status"] == "ready"


def test_transport_protected_requires_auth(client: TestClient) -> None:
    protected = client.get("/protected/status")
    metrics = client.get("/metrics")

    assert protected.status_code == 401
    assert metrics.status_code == 401
    assert protected.json()["error"]["code"] == "UNAUTHORIZED"
    assert metrics.json()["error"]["code"] == "UNAUTHORIZED"


def test_transport_protected_accepts_bearer(client: TestClient) -> None:
    headers = {"Authorization": "Bearer transport-secret", "x-trace-id": "ok-auth"}
    protected = client.get("/protected/status", headers=headers)
    metrics = client.get("/metrics", headers=headers)

    assert protected.status_code == 200
    assert metrics.status_code == 200
    assert protected.json()["data"]["service"] == "authenticated"
    assert metrics.json()["data"]["metrics_requests"] >= 1
    assert metrics.headers["content-type"].startswith("application/json")
