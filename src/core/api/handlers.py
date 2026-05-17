from __future__ import annotations

import logging
from typing import Any, Mapping

from core.api.dependencies import ApiDependencies
from core.api.envelope import build_error_envelope, build_success_envelope, ensure_trace_id
from core.api.logging import log_api_event, log_error
from core.logging_setup import clear_log_context, log_runtime_exception, set_log_context
from core.api.security import UnauthorizedError
from core.geo.scope import GeoScopeMismatchError, assert_geo_in_scope
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
    set_log_context(trace_id=resolved_trace_id)
    try:
        request = parse_story_intake_request(payload)
        log_api_event(
            logging.DEBUG,
            "story_intake_received",
            trace_id=resolved_trace_id,
            schema_version=request.schema_version,
            submitter=request.submitter.external_user_id,
            lang=request.narrative.language,
            session_language=request.narrative.session_language,
            has_multilingual_title=all(
                request.narrative.title[lang].strip() for lang in ("et", "ru", "en")
            ),
            has_location_query=bool((request.narrative.location_query or "").strip()),
            canonical_labels_count=len(request.narrative.canonical_labels),
            canonical_type=request.narrative.canonical_type,
        )
        log_api_event(
            logging.INFO,
            f"story.persistence_backend_selected backend={dependencies.db_backend}",
            trace_id=resolved_trace_id,
            backend=dependencies.db_backend,
            repository_class=dependencies.story_intake_service.repository.__class__.__name__,
            stage="api.intake",
            outcome="selected",
        )
        geo_scope = dependencies.config.cluster_geo_scope
        location_query = (request.narrative.location_query or "").strip()
        if geo_scope is not None and location_query:
            geo_service = dependencies.story_intake_service.geo_service
            if geo_service is not None:
                scope_level, scope_value = geo_scope
                resolved_geo = geo_service.resolve_for_story(location_query)
                assert_geo_in_scope(
                    resolved_geo,
                    level=scope_level,
                    expected_value=scope_value,
                )
        story = dependencies.story_intake_service.create_story(
            request,
            idempotency_key=idempotency_key,
        )
        set_log_context(story_id=story.story_id)
        log_api_event(
            logging.INFO,
            "story.persistence_commit_ack "
            f"backend={dependencies.db_backend} "
            f"lifecycle_status={story.lifecycle_status.value}",
            trace_id=resolved_trace_id,
            story_id=story.story_id,
            backend=dependencies.db_backend,
            repository_class=dependencies.story_intake_service.repository.__class__.__name__,
            stage="api.intake",
            outcome="success",
        )
        log_api_event(
            logging.INFO,
            "story_intake_created",
            trace_id=resolved_trace_id,
            outcome="success",
            story_id=story.story_id,
        )
        # Intake path no longer clusters synchronously; emit explicit pending signal.
        log_api_event(
            logging.INFO,
            "story_cluster_issue_pending",
            trace_id=resolved_trace_id,
            story_id=story.story_id,
            reason="cron_deferred",
            outcome="not_clustered",
        )
        log_api_event(
            logging.INFO,
            "story.pipeline_outcome",
            trace_id=resolved_trace_id,
            story_id=story.story_id,
            lifecycle_status=story.lifecycle_status.value,
            cluster_outcome="deferred",
            error_code="none",
            outcome="success",
        )
        return (
            build_story_intake_response(
                story_id=story.story_id,
                status=story.lifecycle_status.value,
                trace_id=resolved_trace_id,
            ),
            202,
        )
    except GeoScopeMismatchError as exc:
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        log_api_event(
            logging.INFO,
            "story.pipeline_outcome",
            trace_id=resolved_trace_id,
            story_id="-",
            lifecycle_status="rejected",
            cluster_outcome="not_started",
            error_code=envelope.error.code,
            outcome="error",
        )
        return envelope.as_dict(), 422
    except IntakeValidationError as exc:
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        log_api_event(
            logging.DEBUG,
            "story.pipeline_outcome",
            trace_id=resolved_trace_id,
            story_id="-",
            lifecycle_status="rejected",
            cluster_outcome="not_started",
            error_code=envelope.error.code,
            outcome="error",
        )
        return envelope.as_dict(), 400
    except ValueError as exc:
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        log_api_event(
            logging.INFO,
            "story.pipeline_outcome",
            trace_id=resolved_trace_id,
            story_id="-",
            lifecycle_status="rejected",
            cluster_outcome="not_started",
            error_code=envelope.error.code,
            outcome="error",
        )
        return envelope.as_dict(), 400
    except Exception as exc:  # noqa: BLE001
        log_runtime_exception(
            logging.getLogger("core.api"),
            exc,
            stage="api.intake",
            trace_id=resolved_trace_id,
        )
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        log_api_event(
            logging.INFO,
            "story.pipeline_outcome",
            trace_id=resolved_trace_id,
            story_id="-",
            lifecycle_status="failed",
            cluster_outcome="not_started",
            error_code=envelope.error.code,
            outcome="error",
        )
        return envelope.as_dict(), 500
    finally:
        clear_log_context()


def handle_tallinn_issues_list(
    dependencies: ApiDependencies,
    *,
    status: list[str] | None = None,
    issue_type: str | None = None,
    labels: list[str] | None = None,
    institution: str | None = None,
    created_after: str | None = None,
    created_before: str | None = None,
    geo_lat_min: float | None = None,
    geo_lat_max: float | None = None,
    geo_lon_min: float | None = None,
    geo_lon_max: float | None = None,
    geo_district: list[str] | None = None,
    geo_settlement: list[str] | None = None,
    geo_region: list[str] | None = None,
    geo_country: list[str] | None = None,
    geo_postal_code: list[str] | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        issues = dependencies.issue_projection_read_store.list_projections(
            status=status,
            issue_type=issue_type,
            labels=labels,
            institution=institution,
            created_after=created_after,
            created_before=created_before,
            geo_lat_min=geo_lat_min,
            geo_lat_max=geo_lat_max,
            geo_lon_min=geo_lon_min,
            geo_lon_max=geo_lon_max,
            geo_district=geo_district,
            geo_settlement=geo_settlement,
            geo_region=geo_region,
            geo_country=geo_country,
            geo_postal_code=geo_postal_code,
        )
        return build_success_envelope(
            data={"issues": issues}, trace_id=resolved_trace_id
        ).as_dict()
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict()


def handle_tallinn_issue_get(
    dependencies: ApiDependencies,
    *,
    issue_id: str,
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        projection = dependencies.issue_projection_read_store.get_projection(issue_id)
        if projection is None:
            return (
                build_error_envelope(
                    ValueError(f"Issue not found: {issue_id}"),
                    trace_id=resolved_trace_id,
                ).as_dict(),
                404,
            )
        return (
            build_success_envelope(
                data={"issue": projection}, trace_id=resolved_trace_id
            ).as_dict(),
            200,
        )
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500


def handle_tallinn_issue_create(
    dependencies: ApiDependencies,
    *,
    body: dict[str, Any],
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        story_ids = body.get("story_ids", [])
        if not isinstance(story_ids, list):
            raise ValueError("story_ids must be a list.")
        title = body.get("title", {})
        if not isinstance(title, dict):
            raise ValueError("title must be an object.")
        issue_id = dependencies.issue_create_service.create_manual_issue(
            cluster_id=str(body.get("cluster_id", "")),
            story_ids=story_ids,
            title=title,
            issue_type=str(body.get("type", "complaint")),
        )
        return (
            build_success_envelope(
                data={"issue_id": issue_id}, trace_id=resolved_trace_id
            ).as_dict(),
            201,
        )
    except (KeyError, ValueError) as exc:
        return build_error_envelope(exc, trace_id=resolved_trace_id).as_dict(), 400
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500


