from __future__ import annotations

import logging
from typing import Any

from core.api.envelope import ErrorEnvelope


LOGGER = logging.getLogger("core.api")


def log_error(envelope: ErrorEnvelope) -> None:
    LOGGER.error(
        "api_error code=%s type=%s",
        envelope.error.code,
        envelope.error.type,
        extra={"trace_id": envelope.trace_id},
    )


def log_api_event(
    level: int,
    message: str,
    *,
    trace_id: str,
    **extra_fields: Any,
) -> None:
    """Structured log line with trace_id for request-scoped observability."""
    LOGGER.log(
        level,
        message,
        extra={"trace_id": trace_id, **extra_fields},
    )

