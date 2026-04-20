from __future__ import annotations

from core.api import build_error_envelope, build_success_envelope
from core.config import ConfigError


def test_validation_error_envelope_contract_shape() -> None:
    trace_id = "trace-validation-1"
    envelope = build_error_envelope(ConfigError("invalid input"), trace_id=trace_id)
    payload = envelope.as_dict()
    assert payload == {
        "error": {
            "code": "VALIDATION_ERROR",
            "type": "validation",
            "message": "invalid input",
            "details": {},
        },
        "trace_id": trace_id,
    }


def test_domain_error_mapping() -> None:
    envelope = build_error_envelope(ValueError("domain rule failed"), trace_id="trace-domain")
    assert envelope.error.code == "DOMAIN_ERROR"
    assert envelope.error.type == "domain"
    assert envelope.trace_id == "trace-domain"


def test_infrastructure_error_mapping() -> None:
    envelope = build_error_envelope(
        ConnectionError("connection failed"), trace_id="trace-infra"
    )
    assert envelope.error.code == "INFRASTRUCTURE_ERROR"
    assert envelope.error.type == "infrastructure"
    assert envelope.trace_id == "trace-infra"


def test_internal_error_mapping_default_message() -> None:
    envelope = build_error_envelope(RuntimeError("boom"), trace_id="trace-internal")
    assert envelope.error.code == "INTERNAL_ERROR"
    assert envelope.error.type == "internal"
    assert envelope.error.message == "Unexpected internal error."
    assert envelope.trace_id == "trace-internal"


def test_success_envelope_has_trace_id() -> None:
    payload = build_success_envelope({"status": "ok"}, trace_id="trace-success").as_dict()
    assert payload == {"data": {"status": "ok"}, "trace_id": "trace-success"}

