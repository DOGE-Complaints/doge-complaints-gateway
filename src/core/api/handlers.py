from __future__ import annotations

import logging
from typing import Any, Mapping

from core.api.dependencies import ApiDependencies
from core.api.envelope import build_error_envelope, build_success_envelope, ensure_trace_id
from core.api.logging import log_api_event, log_error
from core.api.security import UnauthorizedError
from core.application import IssueCreateCommand
from core.intake import IntakeValidationError, build_story_intake_response, parse_story_intake_request


def _require_service_auth(
    dependencies: ApiDependencies,
    *,
    headers: Mapping[str, str] | None,
    trace_id: str,
) -> dict[str, Any] | None:
    try:
        dependencies.service_auth.require(headers or {})
        return None
    except UnauthorizedError as exc:
        dependencies.metrics.record_auth_failure()
        envelope = build_error_envelope(exc, trace_id=trace_id)
        log_error(envelope)
        return envelope.as_dict()


def handle_health(
    dependencies: ApiDependencies, trace_id: str | None = None
) -> dict[str, Any]:
    resolved_trace_id = ensure_trace_id(trace_id)
    dependencies.metrics.record_health()
    try:
        status = dependencies.health_service.get_status()
        log_api_event(
            logging.INFO,
            "health_check_ok",
            trace_id=resolved_trace_id,
            outcome="success",
        )
        return build_success_envelope(
            data={"status": status}, trace_id=resolved_trace_id
        ).as_dict()
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict()


def handle_readiness(
    dependencies: ApiDependencies, trace_id: str | None = None
) -> dict[str, Any]:
    resolved_trace_id = ensure_trace_id(trace_id)
    dependencies.metrics.record_readiness()
    status = "ready" if dependencies.db_ready else "degraded"
    log_api_event(
        logging.INFO,
        "readiness_check",
        trace_id=resolved_trace_id,
        outcome=status,
    )
    return build_success_envelope(
        data={
            "status": status,
            "db": {
                "backend": dependencies.db_backend,
                "ready": dependencies.db_ready,
                "checks": dict(dependencies.db_checks),
            },
        },
        trace_id=resolved_trace_id,
    ).as_dict()


def handle_protected_status(
    dependencies: ApiDependencies,
    headers: Mapping[str, str] | None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    resolved_trace_id = ensure_trace_id(trace_id)
    unauthorized = _require_service_auth(
        dependencies, headers=headers, trace_id=resolved_trace_id
    )
    if unauthorized is not None:
        return unauthorized
    dependencies.metrics.record_protected()
    log_api_event(
        logging.INFO,
        "protected_status_ok",
        trace_id=resolved_trace_id,
        outcome="success",
    )
    return build_success_envelope(
        data={"service": "authenticated"}, trace_id=resolved_trace_id
    ).as_dict()


def handle_metrics(
    dependencies: ApiDependencies,
    headers: Mapping[str, str] | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    resolved_trace_id = ensure_trace_id(trace_id)
    unauthorized = _require_service_auth(
        dependencies, headers=headers, trace_id=resolved_trace_id
    )
    if unauthorized is not None:
        return unauthorized
    dependencies.metrics.record_metrics_endpoint()
    log_api_event(
        logging.INFO,
        "metrics_scrape",
        trace_id=resolved_trace_id,
        outcome="success",
    )
    return build_success_envelope(
        data=dependencies.metrics.as_dict(), trace_id=resolved_trace_id
    ).as_dict()


def handle_story_intake(
    dependencies: ApiDependencies,
    *,
    payload: Mapping[str, Any],
    idempotency_key: str | None = None,
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        request = parse_story_intake_request(payload)
        story = dependencies.story_intake_service.create_story(
            request,
            idempotency_key=idempotency_key,
        )
        log_api_event(
            logging.INFO,
            "story_intake_created",
            trace_id=resolved_trace_id,
            outcome="success",
            story_id=story.story_id,
        )
        return (
            build_story_intake_response(
                story_id=story.story_id,
                status=story.lifecycle_status.value,
                trace_id=resolved_trace_id,
            ),
            200,
        )
    except IntakeValidationError as exc:
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 400
    except ValueError as exc:
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 400
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500


def handle_issue_create(
    dependencies: ApiDependencies,
    *,
    payload: Mapping[str, Any],
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        cluster_id_raw = payload.get("cluster_id")
        story_ids_raw = payload.get("story_ids")
        readiness_score_raw = payload.get("readiness_score")
        title_raw = payload.get("title")

        if not isinstance(cluster_id_raw, str) or not cluster_id_raw.strip():
            raise ValueError("Missing or invalid cluster_id.")
        if not isinstance(story_ids_raw, list) or not story_ids_raw:
            raise ValueError("Missing or invalid story_ids. Expected non-empty array.")
        if any(not isinstance(story_id, str) or not story_id.strip() for story_id in story_ids_raw):
            raise ValueError("Missing or invalid story_ids entries.")
        if not isinstance(readiness_score_raw, int):
            raise ValueError("Missing or invalid readiness_score. Expected integer.")
        if not isinstance(title_raw, str) or not title_raw.strip():
            raise ValueError("Missing or invalid title.")

        result = dependencies.issue_create_service.create_issue(
            IssueCreateCommand(
                cluster_id=cluster_id_raw.strip(),
                story_ids=tuple(story_id.strip() for story_id in story_ids_raw),
                readiness_score=readiness_score_raw,
                title=title_raw.strip(),
            )
        )
        log_api_event(
            logging.INFO,
            "issue_created",
            trace_id=resolved_trace_id,
            outcome="success",
            issue_id=result.issue_id,
        )
        return (
            build_success_envelope(data=result.as_dict(), trace_id=resolved_trace_id).as_dict(),
            200,
        )
    except ValueError as exc:
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 400
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500
