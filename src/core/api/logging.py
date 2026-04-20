from __future__ import annotations

import logging

from core.api.envelope import ErrorEnvelope


LOGGER = logging.getLogger("core.api")


def log_error(envelope: ErrorEnvelope) -> None:
    LOGGER.error(
        "api_error code=%s type=%s",
        envelope.error.code,
        envelope.error.type,
        extra={"trace_id": envelope.trace_id},
    )

