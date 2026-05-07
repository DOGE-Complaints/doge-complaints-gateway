"""TC-24: GET /ready response shape when DB_BACKEND=supabase (skip-safe without live env)."""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app


def _require_live_http_env() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_TEST_URL", "").strip()
    key = os.environ.get("SUPABASE_TEST_SERVICE_ROLE", "").strip()
    if not url or not key:
        pytest.skip("SUPABASE_TEST_URL/SUPABASE_TEST_SERVICE_ROLE are not configured.")
    return url, key


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    supabase_url, service_role_key = _require_live_http_env()
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "20")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    monkeypatch.setenv("DB_BACKEND", "supabase")
    monkeypatch.setenv("SUPABASE_URL", supabase_url)
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", service_role_key)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_supabase_ready_endpoint_reports_expected_db_checks(client: TestClient) -> None:
    response = client.get("/ready", headers={"x-trace-id": "tcr-p2-03-ready"})
    assert response.status_code == 200
    data = response.json()["data"]
    db = data["db"]
    assert db["backend"] == "supabase"
    assert db["ready"] is True
    checks = db["checks"]
    assert "connectivity" in checks
    assert "schema" in checks
    assert "columns" in checks
    assert "policy_probe" in checks
