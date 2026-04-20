from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class IntakeErrorType(StrEnum):
    VALIDATION_ERROR = "validation_error"
    DOMAIN_ERROR = "domain_error"
    INFRASTRUCTURE_ERROR = "infrastructure_error"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True)
class IntakeErrorInfo:
    error_type: IntakeErrorType
    code: str
    message: str


def classify_intake_error(error: Exception) -> IntakeErrorInfo:
    if isinstance(error, ValueError):
        return IntakeErrorInfo(
            error_type=IntakeErrorType.VALIDATION_ERROR,
            code="INTAKE_VALIDATION_ERROR",
            message=str(error),
        )
    if isinstance(error, (ConnectionError, TimeoutError, OSError)):
        return IntakeErrorInfo(
            error_type=IntakeErrorType.INFRASTRUCTURE_ERROR,
            code="INTAKE_INFRASTRUCTURE_ERROR",
            message="Intake infrastructure dependency failed.",
        )
    return IntakeErrorInfo(
        error_type=IntakeErrorType.INTERNAL_ERROR,
        code="INTAKE_INTERNAL_ERROR",
        message="Unexpected intake failure.",
    )


def build_intake_error_payload(error: Exception, *, trace_id: str) -> dict[str, str]:
    info = classify_intake_error(error)
    return {
        "trace_id": trace_id,
        "error_type": info.error_type.value,
        "code": info.code,
        "message": info.message,
    }


def log_intake_error(
    *, logger: logging.Logger, error: Exception, trace_id: str, event: str
) -> None:
    payload = build_intake_error_payload(error, trace_id=trace_id)
    logger.error(
        "intake_event_failed",
        extra={
            "event": event,
            "trace_id": payload["trace_id"],
            "error_type": payload["error_type"],
            "error_code": payload["code"],
        },
    )


@dataclass
class IntakeTelemetry:
    accepted_count: int = 0
    rejected_count: int = 0
    failed_count: int = 0

    def record_accepted(self) -> None:
        self.accepted_count += 1

    def record_rejected(self) -> None:
        self.rejected_count += 1

    def record_failed(self) -> None:
        self.failed_count += 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "accepted_count": self.accepted_count,
            "rejected_count": self.rejected_count,
            "failed_count": self.failed_count,
        }

