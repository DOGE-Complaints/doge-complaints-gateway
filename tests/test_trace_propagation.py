from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import pytest  # pyright: ignore[reportMissingImports]

from core.api import HandlerDependencies, ensure_trace_id, handle_health


@dataclass(frozen=True)
class _OkService:
    def get_status(self) -> str:
        return "ok"


@dataclass(frozen=True)
class _FailService:
    def get_status(self) -> str:
        raise ConnectionError("transport unavailable")


@dataclass(frozen=True)
class _DummyIntakeService:
    pass


@dataclass(frozen=True)
class _DummyStoryClusterOrchestrator:
    pass


@dataclass(frozen=True)
class _DummyIssueCreateService:
    pass


@dataclass(frozen=True)
class _DummyIssueProjectionReadStore:
    def list_projections(self, **_kwargs: Any) -> list[dict[str, object]]:
        return []

    def get_projection(self, _issue_id: str) -> dict[str, object] | None:
        return None


def _deps_kwargs(health_service: Any) -> dict[str, Any]:
    return {
        "health_service": health_service,
        "story_intake_service": _DummyIntakeService(),
        "story_cluster_orchestrator": _DummyStoryClusterOrchestrator(),
        "issue_create_service": _DummyIssueCreateService(),
        "issue_projection_read_store": _DummyIssueProjectionReadStore(),
        "network_pulse_service": object(),
        "emerging_signals_service": object(),
    }


def test_trace_id_preserved_for_success_response() -> None:
    trace_id = "trace-success-explicit"
    payload = handle_health(HandlerDependencies(**_deps_kwargs(_OkService())), trace_id=trace_id)
    assert payload["trace_id"] == trace_id
    assert payload["data"]["status"] == "ok"


def test_trace_id_generated_when_absent() -> None:
    trace_id = ensure_trace_id(None)
    assert isinstance(trace_id, str)
    assert len(trace_id) > 10


def test_trace_id_propagates_into_error_and_logs(caplog: pytest.LogCaptureFixture) -> None:
    trace_id = "trace-error-explicit"
    with caplog.at_level(logging.ERROR, logger="core.api"):
        payload = handle_health(
            HandlerDependencies(**_deps_kwargs(_FailService())), trace_id=trace_id
        )

    assert payload["trace_id"] == trace_id
    assert payload["error"]["code"] == "INFRASTRUCTURE_ERROR"
    assert any(getattr(record, "trace_id", None) == trace_id for record in caplog.records)

