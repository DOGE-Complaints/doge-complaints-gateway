from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from core.api.envelope import build_error_envelope, build_success_envelope, ensure_trace_id
from core.api.logging import log_error


class HealthServiceLike(Protocol):
    def get_status(self) -> str:
        """Return current runtime status."""


@dataclass(frozen=True)
class HandlerDependencies:
    health_service: HealthServiceLike


def handle_health(
    dependencies: HandlerDependencies, trace_id: str | None = None
) -> dict[str, Any]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        status = dependencies.health_service.get_status()
        return build_success_envelope(
            data={"status": status}, trace_id=resolved_trace_id
        ).as_dict()
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict()

