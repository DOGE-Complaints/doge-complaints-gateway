"""Pytest session defaults (STORY-M2-02-06 T05 / GAP-10): align root logging with app configure_logging."""

from __future__ import annotations

import contextvars
import logging
import os
from collections.abc import Callable
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.logging_setup import configure_logging

_SERVICE_WRITE_PATH_SUFFIXES = ("/intake/stories", "/tallinn/issues")
_ORIGINAL_TESTCLIENT_REQUEST: Callable[..., Any] | None = None
_GAUTH_RAW_CLIENT_MARKER = "gauth_raw_client"
_service_skip_auto_headers: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "service_skip_auto_headers", default=False
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """REQ-41 GAP-41-05: tag Layer 5 Supabase tests for `pytest -m live_integration`."""
    marker = pytest.mark.live_integration
    for item in items:
        path = str(item.path).replace("\\", "/")
        if "/tests/integration/supabase/" in path:
            item.add_marker(marker)


@pytest.fixture(scope="session", autouse=True)
def _pytest_session_logging() -> None:
    """Without ASGI lifespan, tests still get predictable log levels (see GAP-10 / §16)."""
    configure_logging(
        os.environ.get("LOG_LEVEL", "INFO"),
        log_format="text",
        log_debug_dir=None,
    )


@pytest.fixture(autouse=True)
def _block_dotenv_leakage(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent provide_app_config(None) from reading production .env vars into tests.

    T01 made provide_app_config() merge .env from cwd when env=None. Without this
    fixture, tests that call provide_app_config(None) or TestClient(app) would inherit
    DB_BACKEND=supabase and SUPABASE_* from the project .env, running against the real
    database. Tests that need a non-default backend override these via monkeypatch.setenv
    in their own fixtures, which run after this autouse fixture.
    """
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "60")
    monkeypatch.setenv(
        "CLUSTER_ACTIVE_LENSES",
        "civic_domain_micro,failure_pattern_micro,civic_weight_systemic,"
        "desired_outcome_local,affected_group_local,geographic_district_micro",
    )
    monkeypatch.setenv("CLUSTER_PRIMARY_LENS", "civic_domain_micro")
    monkeypatch.setenv("CLUSTER_SIGNAL_SOURCE", "canonical")
    monkeypatch.setenv("CLUSTER_TIE_BREAKER", "alpha")
    monkeypatch.setenv("SERVICE_API_TOKEN", "gauth-test-service-token")


GAUTH_TEST_SERVICE_TOKEN = "gauth-test-service-token"
GAUTH_TEST_USER_TOKEN = "gauth-test-user-token"
GAUTH_TEST_IDENTITY_URL = "https://identity.test"


def gauth_intake_headers(
    *,
    service_token: str | None = None,
    user_token: str | None = None,
    extra: dict[str, str] | None = None,
) -> dict[str, str]:
    """Service token headers for legacy POST /intake/stories and /tallinn/issues."""
    resolved_service = (
        service_token
        or os.environ.get("SERVICE_API_TOKEN")
        or GAUTH_TEST_SERVICE_TOKEN
    )
    headers = {"Authorization": f"Bearer {resolved_service}"}
    if user_token is not None:
        headers["X-User-Token"] = user_token
    if extra:
        headers.update(extra)
    return headers


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "gauth_raw_client: skip auto-injected service headers on TestClient",
    )


def _service_auto_inject_headers(method: str, url: str, kwargs: dict[str, Any]) -> dict[str, Any]:
    if method.upper() != "POST":
        return kwargs
    path = url.split("?", 1)[0]
    if not any(path.endswith(suffix) for suffix in _SERVICE_WRITE_PATH_SUFFIXES):
        return kwargs
    merged = gauth_intake_headers()
    merged.update(kwargs.pop("headers", None) or {})
    kwargs["headers"] = merged
    return kwargs


@pytest.fixture(autouse=True)
def _gauth_testclient_auto_headers(request: pytest.FixtureRequest):
    """Inject default service token on TestClient POSTs to public write paths."""
    global _ORIGINAL_TESTCLIENT_REQUEST
    skip = (
        request.node.get_closest_marker(_GAUTH_RAW_CLIENT_MARKER) is not None
        or "test_gw_gauth_01" in request.node.nodeid
    )
    token = _service_skip_auto_headers.set(skip)
    if _ORIGINAL_TESTCLIENT_REQUEST is None:
        _ORIGINAL_TESTCLIENT_REQUEST = TestClient.request

        def _patched_request(
            self: TestClient, method: str, url: str, **kwargs: Any
        ) -> Any:
            if not _service_skip_auto_headers.get():
                kwargs = _service_auto_inject_headers(method, url, kwargs)
            assert _ORIGINAL_TESTCLIENT_REQUEST is not None
            return _ORIGINAL_TESTCLIENT_REQUEST(self, method, url, **kwargs)

        TestClient.request = _patched_request  # type: ignore[method-assign]
    yield
    _service_skip_auto_headers.reset(token)


@pytest.fixture
def configured_logging() -> None:
    """REQ-39 F-04: opt-in DEBUG logging for tests that assert on log output."""
    configure_logging("DEBUG", log_format="text")
    yield
    logging.getLogger().handlers.clear()
    logging.getLogger().setLevel(logging.WARNING)
