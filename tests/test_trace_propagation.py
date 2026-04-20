from __future__ import annotations

import logging
from dataclasses import dataclass

import pytest

from core.api import HandlerDependencies, ensure_trace_id, handle_health


@dataclass(frozen=True)
class _OkService:
    def get_status(self) -> str:
        return "ok"


@dataclass(frozen=True)
class _FailService:
    def get_status(self) -> str:
        raise ConnectionError("transport unavailable")


def test_trace_id_preserved_for_success_response() -> None:
    trace_id = "trace-success-explicit"
    payload = handle_health(HandlerDependencies(health_service=_OkService()), trace_id=trace_id)
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
            HandlerDependencies(health_service=_FailService()), trace_id=trace_id
        )

    assert payload["trace_id"] == trace_id
    assert payload["error"]["code"] == "INFRASTRUCTURE_ERROR"
    assert any(getattr(record, "trace_id", None) == trace_id for record in caplog.records)

