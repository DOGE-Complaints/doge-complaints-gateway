"""Pytest session defaults (STORY-M2-02-06 T05 / GAP-10): align root logging with app configure_logging."""

from __future__ import annotations

import logging
import os

import pytest

from core.logging_setup import configure_logging


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


@pytest.fixture
def configured_logging() -> None:
    """REQ-39 F-04: opt-in DEBUG logging for tests that assert on log output."""
    configure_logging("DEBUG", log_format="text")
    yield
    logging.getLogger().handlers.clear()
    logging.getLogger().setLevel(logging.WARNING)
