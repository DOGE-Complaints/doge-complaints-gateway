from __future__ import annotations

import logging

import pytest

from core.intake import (
    IntakeErrorType,
    IntakeTelemetry,
    build_intake_error_payload,
    classify_intake_error,
    log_intake_error,
)


def test_classify_intake_error_validation() -> None:
    info = classify_intake_error(ValueError("invalid payload"))
    assert info.error_type == IntakeErrorType.VALIDATION_ERROR
    assert info.code == "INTAKE_VALIDATION_ERROR"


def test_classify_intake_error_infrastructure() -> None:
    info = classify_intake_error(ConnectionError("db down"))
    assert info.error_type == IntakeErrorType.INFRASTRUCTURE_ERROR
    assert info.code == "INTAKE_INFRASTRUCTURE_ERROR"


def test_build_intake_error_payload_contains_trace_id() -> None:
    payload = build_intake_error_payload(ValueError("bad"), trace_id="trace-intake-1")
    assert payload["trace_id"] == "trace-intake-1"
    assert payload["error_type"] == "validation_error"


def test_log_intake_error_emits_structured_fields(
    caplog: pytest.LogCaptureFixture,
) -> None:
    logger = logging.getLogger("intake-observability-tests")
    with caplog.at_level(logging.ERROR):
        log_intake_error(
            logger=logger,
            error=RuntimeError("boom"),
            trace_id="trace-intake-2",
            event="story_intake",
        )
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.trace_id == "trace-intake-2"
    assert record.error_type == "internal_error"
    assert record.error_code == "INTAKE_INTERNAL_ERROR"


def test_intake_telemetry_counters() -> None:
    telemetry = IntakeTelemetry()
    telemetry.record_accepted()
    telemetry.record_accepted()
    telemetry.record_rejected()
    telemetry.record_failed()
    assert telemetry.as_dict() == {
        "accepted_count": 2,
        "rejected_count": 1,
        "failed_count": 1,
    }

