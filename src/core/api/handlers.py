from __future__ import annotations

import logging
import secrets
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any, Mapping

from core.api.dependencies import ApiDependencies
from core.api.envelope import (
    DatabaseNotReadyError,
    build_error_envelope,
    build_success_envelope,
    ensure_trace_id,
)
from core.api.logging import log_api_event, log_error
from core.logging_setup import clear_log_context, log_runtime_exception, set_log_context
from core.api.security import UnauthorizedError
from core.domain import StoryDraftRecord
from core.config import schema as config_schema
from core.geo.intake_merge import enforce_geo_intake_mode
from core.geo.scope import GeoScopeMismatchError, assert_geo_in_scope
from core.identity.authoritative_submitter import (
    authoritative_submitter_from_introspection,
    payload_submitter_mismatches_introspection,
)
from core.application.story_activity import StoryActivityService
from core.application.services import GPT_CLASSIFIER_POLICY_VERSION
from core.identity.introspection_result import IntrospectionResult
from core.intake import (
    IntakeValidationError,
    Submitter,
    build_story_intake_response,
    intake_request_from_stash_and_submitter,
    parse_story_draft_stash_request,
    parse_story_intake_request,
    parse_stored_draft_stash_request,
)
from core.telemetry.label_miss import LabelMissValidationError, parse_label_miss_payload


def handle_network_pulse(
    dependencies: ApiDependencies,
    *,
    trace_id: str | None = None,
) -> dict[str, Any]:
    """GW-ES-02 / REQ-49: public Network Pulse L1 aggregates."""
    resolved_trace_id = ensure_trace_id(trace_id)
    pulse = dependencies.network_pulse_service.build_pulse()
    return build_success_envelope(data=pulse, trace_id=resolved_trace_id).as_dict()


def handle_emerging_signals(
    dependencies: ApiDependencies,
    *,
    top_n: int = 10,
    trace_id: str | None = None,
) -> dict[str, Any]:
    """GW-ES-03 / REQ-50: public Emerging L2 (≠ Issues projections)."""
    resolved_trace_id = ensure_trace_id(trace_id)
    emerging = dependencies.emerging_signals_service.build_emerging(top_n=top_n)
    return build_success_envelope(data=emerging, trace_id=resolved_trace_id).as_dict()


def _require_service_auth(
    dependencies: ApiDependencies,
    *,
    headers: Mapping[str, str] | None,
    trace_id: str,
) -> dict[str, Any] | None:
    try:
        dependencies.service_auth.require(headers or {}, mandatory=False)
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
    user_introspection: IntrospectionResult | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    set_log_context(trace_id=resolved_trace_id)
    if dependencies.db_backend == "supabase" and not dependencies.db_ready:
        envelope = build_error_envelope(
            DatabaseNotReadyError(
                "Persistence backend is not ready; fix schema drift or configuration."
            ),
            trace_id=resolved_trace_id,
            details={
                "db": {
                    "backend": dependencies.db_backend,
                    "ready": dependencies.db_ready,
                    "checks": dict(dependencies.db_checks),
                }
            },
        )
        log_error(envelope)
        log_api_event(
            logging.WARNING,
            "story_intake_rejected_db_not_ready",
            trace_id=resolved_trace_id,
            backend=dependencies.db_backend,
            checks=dict(dependencies.db_checks),
            outcome="error",
        )
        return envelope.as_dict(), 503
    try:
        request = parse_story_intake_request(payload)
        if user_introspection is not None:
            claimed_submitter = request.submitter
            if payload_submitter_mismatches_introspection(
                claimed_submitter, user_introspection
            ):
                log_api_event(
                    logging.INFO,
                    "story_intake_submitter_mismatch",
                    trace_id=resolved_trace_id,
                    claimed_external_user_id=claimed_submitter.external_user_id,
                    authoritative_sub=user_introspection.sub,
                    outcome="resolved_to_introspection",
                )
            request = replace(
                request,
                submitter=authoritative_submitter_from_introspection(
                    payload_submitter=claimed_submitter,
                    introspection=user_introspection,
                    identity_introspect_url=dependencies.config.identity_base_url,
                ),
            )
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
        geo_scope = config_schema.civic_clustering_from_active_node(
            schema_id=dependencies.config.node_schema_id,
            schema_version=dependencies.config.node_schema_version,
        ).geo_scope
        geo_service = dependencies.story_intake_service.geo_service
        if geo_scope is not None and geo_service is None:
            raise IntakeValidationError("geo unavailable")
        location_query = (request.narrative.location_query or "").strip()
        enforce_geo_intake_mode(
            geo_intake=config_schema.geo_intake_from_active_node(
                schema_id=dependencies.config.node_schema_id,
                schema_version=dependencies.config.node_schema_version,
            ),
            location_query=location_query,
            detail=request.geo_detail,
        )
        if geo_scope is not None and location_query:
            scope_level, scope_value = geo_scope
            resolved_geo = geo_service.resolve_for_story(location_query)
            assert_geo_in_scope(
                resolved_geo,
                level=scope_level,
                expected_value=scope_value,
            )
        intake_result = dependencies.story_intake_service.create_story(
            request,
            idempotency_key=idempotency_key,
        )
        story = intake_result.story
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
                geo_resolved=intake_result.geo_resolved,
                gpt_signals_persisted=intake_result.gpt_signals_persisted,
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


def handle_issues_list(
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


def handle_issue_get(
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


def handle_issue_create(
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


def handle_label_miss_telemetry(
    dependencies: ApiDependencies,
    *,
    body: dict[str, Any],
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        label_key, locale = parse_label_miss_payload(body)
    except LabelMissValidationError as exc:
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 400

    store = dependencies.label_translation_miss_store
    accepted = False
    if store is not None:
        try:
            store.record_miss(label_key, locale)
            accepted = True
        except Exception as exc:  # noqa: BLE001
            log_api_event(
                logging.WARNING,
                "label_miss_store_failed",
                trace_id=resolved_trace_id,
                label_key=label_key,
                locale=locale,
                outcome="degraded",
            )
            log_runtime_exception(
                logging.getLogger("core.api"),
                exc,
                stage="api.telemetry.label_miss",
                trace_id=resolved_trace_id,
            )

    return (
        build_success_envelope(
            data={"accepted": accepted}, trace_id=resolved_trace_id
        ).as_dict(),
        202,
    )


def handle_story_draft_create(
    dependencies: ApiDependencies,
    *,
    payload: Mapping[str, Any],
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    repository = dependencies.story_draft_repository
    if repository is None:
        envelope = build_error_envelope(
            RuntimeError("Story draft repository is not configured."),
            trace_id=resolved_trace_id,
        )
        log_error(envelope)
        return envelope.as_dict(), 500
    try:
        stash = parse_story_draft_stash_request(payload)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=dependencies.config.story_draft_ttl_seconds)
        draft_id = secrets.token_urlsafe(16)
        record = StoryDraftRecord(
            draft_id=draft_id,
            payload=stash.as_dict(),
            created_at=now,
            expires_at=expires_at,
            updated_at=now,
        )
        repository.save_draft(record)
        log_api_event(
            logging.INFO,
            "story_draft_stashed",
            trace_id=resolved_trace_id,
            draft_id=draft_id,
            outcome="success",
        )
        return (
            build_success_envelope(
                data={"draft_id": draft_id}, trace_id=resolved_trace_id
            ).as_dict(),
            201,
        )
    except IntakeValidationError as exc:
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 400
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500


def handle_story_draft_get(
    dependencies: ApiDependencies,
    *,
    draft_id: str,
    submitter_external_user_id: str | None = None,
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    repository = dependencies.story_draft_repository
    if repository is None:
        envelope = build_error_envelope(
            RuntimeError("Story draft repository is not configured."),
            trace_id=resolved_trace_id,
        )
        log_error(envelope)
        return envelope.as_dict(), 500
    try:
        record = repository.get_draft(draft_id)
        if record is None:
            return (
                build_error_envelope(
                    ValueError(f"Draft not found: {draft_id}"),
                    trace_id=resolved_trace_id,
                ).as_dict(),
                404,
            )
        if submitter_external_user_id and dependencies.draft_owner_repository is not None:
            try:
                dependencies.draft_owner_repository.set_owner(
                    draft_id, submitter_external_user_id
                )
            except Exception as exc:  # noqa: BLE001
                log_api_event(
                    logging.WARNING,
                    "draft_owner_set_failed",
                    trace_id=resolved_trace_id,
                    draft_id=draft_id,
                    outcome="best_effort_ignored",
                    error_type=type(exc).__name__,
                )
        return (
            build_success_envelope(data=record.payload, trace_id=resolved_trace_id).as_dict(),
            200,
        )
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500


def handle_story_draft_current(
    dependencies: ApiDependencies,
    *,
    submitter_external_user_id: str,
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    owner_repository = dependencies.draft_owner_repository
    if owner_repository is None:
        envelope = build_error_envelope(
            RuntimeError("Draft owner repository is not configured."),
            trace_id=resolved_trace_id,
        )
        log_error(envelope)
        return envelope.as_dict(), 500
    try:
        record = owner_repository.get_current_draft(submitter_external_user_id)
        if record is None:
            return (
                build_success_envelope(data=None, trace_id=resolved_trace_id).as_dict(),
                200,
            )
        return (
            build_success_envelope(
                data={
                    "draft_id": record.draft_id,
                    "last_edited_at": record.updated_at.isoformat(),
                },
                trace_id=resolved_trace_id,
            ).as_dict(),
            200,
        )
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500


def _story_intake_replay_from_idempotency(
    dependencies: ApiDependencies,
    *,
    draft_id: str,
    trace_id: str,
) -> tuple[dict[str, Any], int] | None:
    """Return 202 intake envelope when draft_id already submitted (GW-DRAFT-02 T04)."""
    idem_repo = dependencies.story_intake_service.idempotency_repository
    existing_key = idem_repo.get_by_key(draft_id)
    if existing_key is None:
        return None
    existing_story = dependencies.story_intake_service.repository.get_story(
        existing_key.story_id
    )
    if existing_story is None:
        return None
    signal_store = dependencies.story_intake_service.story_signal_store
    gpt_signals_persisted = (
        signal_store is not None
        and signal_store.get_signals(
            existing_story.story_id, GPT_CLASSIFIER_POLICY_VERSION
        )
        is not None
    )
    return (
        build_story_intake_response(
            story_id=existing_story.story_id,
            status=existing_story.lifecycle_status.value,
            trace_id=trace_id,
            geo_resolved=existing_story.geo is not None,
            gpt_signals_persisted=gpt_signals_persisted,
        ),
        202,
    )


def handle_story_draft_submit(
    dependencies: ApiDependencies,
    *,
    draft_id: str,
    user_introspection: IntrospectionResult,
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    """Submit stashed draft via browser Bearer + identity /me gate (GW-DRAFT-02)."""
    resolved_trace_id = ensure_trace_id(trace_id)
    set_log_context(trace_id=resolved_trace_id)
    replay = _story_intake_replay_from_idempotency(
        dependencies, draft_id=draft_id, trace_id=resolved_trace_id
    )
    if replay is not None:
        log_api_event(
            logging.INFO,
            "story_draft_submit_idempotent_replay",
            trace_id=resolved_trace_id,
            draft_id=draft_id,
            outcome="success",
        )
        return replay

    repository = dependencies.story_draft_repository
    if repository is None:
        envelope = build_error_envelope(
            RuntimeError("Story draft repository is not configured."),
            trace_id=resolved_trace_id,
        )
        log_error(envelope)
        return envelope.as_dict(), 500

    record = repository.get_draft(draft_id)
    if record is None:
        return (
            build_error_envelope(
                ValueError(f"Draft not found: {draft_id}"),
                trace_id=resolved_trace_id,
            ).as_dict(),
            404,
        )

    stash = parse_stored_draft_stash_request(record.payload)
    authoritative = authoritative_submitter_from_introspection(
        payload_submitter=Submitter(external_user_id="", identity_issuer=""),
        introspection=user_introspection,
        identity_introspect_url=dependencies.config.identity_base_url,
    )
    intake_request = intake_request_from_stash_and_submitter(
        stash, submitter=authoritative
    )
    envelope, status_code = handle_story_intake(
        dependencies,
        payload=intake_request.as_dict(),
        idempotency_key=draft_id,
        trace_id=resolved_trace_id,
        user_introspection=None,
    )
    if status_code == 202:
        repository.delete_draft(draft_id)
        log_api_event(
            logging.INFO,
            "story_draft_submitted",
            trace_id=resolved_trace_id,
            draft_id=draft_id,
            story_id=envelope.get("data", {}).get("story_id"),
            outcome="success",
        )
    return envelope, status_code


def handle_story_activity(
    dependencies: ApiDependencies,
    *,
    submitter_external_user_id: str,
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    """GW-CAB-01: user-scoped story list + metrics for cabinet."""
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        service = StoryActivityService(
            story_repository=dependencies.story_intake_service.repository,
            issue_story_link_store=dependencies.issue_create_service.issue_story_link_store,
            issue_projection_read_store=dependencies.issue_projection_read_store,
        )
        data = service.build_activity(submitter_external_user_id=submitter_external_user_id)
        return (
            build_success_envelope(data=data, trace_id=resolved_trace_id).as_dict(),
            200,
        )
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500

