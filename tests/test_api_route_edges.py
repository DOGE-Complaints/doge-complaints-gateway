from __future__ import annotations

from collections.abc import Iterator

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api import asgi_app
from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.config import ConfigError


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    _clear_api_dependencies_cache()


def test_ready_route_degraded_payload_path(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        asgi_app,
        "handle_readiness",
        lambda deps, trace_id: {"trace_id": trace_id, "data": {"status": "degraded"}},
    )
    response = client.get("/ready", headers={"x-trace-id": "ready-degraded"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["trace_id"] == "ready-degraded"
    assert payload["data"]["status"] == "degraded"


def test_demo_auth_page_routes_are_served(client: TestClient) -> None:
    page = client.get("/demo/auth-page")
    page_slash = client.get("/demo/auth-page/")
    styles = client.get("/demo/auth-page/styles.css")

    assert page.status_code == 200
    assert page_slash.status_code == 200
    assert styles.status_code == 200
    assert page.headers["content-type"].startswith("text/html")
    assert styles.headers["content-type"].startswith("text/css")


def test_config_error_handler_returns_http_500_envelope(client: TestClient) -> None:
    def _raise_config_error() -> object:
        raise ConfigError("forced config failure")

    app.dependency_overrides[get_api_dependencies] = _raise_config_error
    response = client.get("/health", headers={"x-trace-id": "cfg-error-trace"})

    assert response.status_code == 500
    payload = response.json()
    assert payload["trace_id"] == "cfg-error-trace"
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert "forced config failure" in payload["error"]["message"]
