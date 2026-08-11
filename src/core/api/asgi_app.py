from __future__ import annotations

import os
import logging
import signal
from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path
from typing import Any

import uvicorn  # pyright: ignore[reportMissingImports]
from fastapi import Depends, FastAPI, Query, Request  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from fastapi.responses import (  # pyright: ignore[reportMissingImports]
    FileResponse,
    JSONResponse,
    Response,
)

from core.api.dependencies import ApiDependencies, build_api_dependencies
from core.api.envelope import build_error_envelope, ensure_trace_id
from core.api.handlers import (
    handle_health,
    handle_label_miss_telemetry,
    handle_metrics,
    handle_network_pulse,
    handle_emerging_signals,
    handle_protected_status,
    handle_readiness,
    handle_story_draft_create,
    handle_story_draft_current,
    handle_story_draft_get,
    handle_story_draft_submit,
    handle_story_activity,
    handle_tallinn_issue_create,
    handle_tallinn_issue_get,
    handle_tallinn_issues_list,
)
from core.api.security import (
    UnauthorizedError,
    UserTokenIntrospectionError,
    UserTokenIntrospectionUnavailableError,
    UserTokenMissingError,
    VerificationRequiredError,
    extract_authorization_bearer,
)
from core.identity import IdentityMeError
from core.identity.verification_gate import (
    DEFAULT_VERIFICATION_REQUIRED_REASON,
    VerificationGateOutcome,
    evaluate_verification_gate,
)
from core.identity.verify_url import build_verify_url
from core.config import ConfigError
from core.logging_setup import log_runtime_exception
from core.scheduler import ClusterCronJob
from core.logging_setup import configure_logging

PUBLIC_ROUTES: tuple[str, ...] = (
    "/health",
    "/ready",
    "/demo/auth-page",
    "/story-drafts",
    "/telemetry/label-misses",
    "/tallinn/issues",
    "/tallinn/network-pulse",
    "/tallinn/emerging-signals",
)
PROTECTED_ROUTES: tuple[str, ...] = ("/protected/status", "/metrics")
_DEMO_DIR = Path(__file__).resolve().parents[3] / "demo" / "auth-page"
_shutdown_reason = "unknown"


def _install_signal_reason_hooks() -> dict[signal.Signals, Any]:
    previous: dict[signal.Signals, Any] = {}

    def _mark_reason(sig: signal.Signals) -> None:
        global _shutdown_reason
        if sig is signal.SIGINT:
            _shutdown_reason = "sigint"
        elif sig is signal.SIGTERM:
            _shutdown_reason = "sigterm"
        else:
            _shutdown_reason = f"signal_{int(sig)}"

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            prev = signal.getsignal(sig)
            previous[sig] = prev

            def _handler(signum: int, frame: Any, *, _prev: Any = prev) -> None:
                _mark_reason(signal.Signals(signum))
                if callable(_prev):
                    _prev(signum, frame)

            signal.signal(sig, _handler)
        except (ValueError, OSError):
            continue
    return previous


def _restore_signal_reason_hooks(previous: dict[signal.Signals, Any]) -> None:
    for sig, handler in previous.items():
        try:
            signal.signal(sig, handler)
        except (ValueError, OSError):
            continue

@asynccontextmanager
async def _lifespan(_: FastAPI):
    global _shutdown_reason
    _shutdown_reason = "unknown"
    signal_hooks = _install_signal_reason_hooks()
    deps = get_api_dependencies()
    configure_logging(
        deps.config.log_level,
        log_format=deps.config.log_format,
        log_debug_dir=deps.config.log_debug_dir,
    )
    logging.getLogger(__name__).info(
        "startup.config db_backend=%s cluster_primary_lens=%s cluster_min_size=%s cron_enabled=%s cron_interval_s=%s",
        deps.config.db_backend,
        deps.config.cluster_primary_lens,
        deps.config.cluster_min_size,
        deps.config.cluster_cron_enabled,
        deps.config.cluster_cron_interval_s,
        extra={
            "db_backend": deps.config.db_backend,
            "cluster_active_lenses": ",".join(deps.config.cluster_active_lenses),
            "cluster_primary_lens": deps.config.cluster_primary_lens,
            "cluster_min_size": deps.config.cluster_min_size,
            "cluster_readiness_threshold": deps.config.cluster_readiness_threshold,
            "log_level": deps.config.log_level,
            "cron_enabled": deps.config.cluster_cron_enabled,
            "cron_interval_s": deps.config.cluster_cron_interval_s,
        },
    )
    logging.getLogger(__name__).info(
        "startup.persistence_backend backend=%s db_ready=%s checks=%s",
        deps.config.db_backend,
        getattr(deps, "db_ready", False),
        ",".join(
            f"{key}:{'ok' if value else 'fail'}"
            for key, value in sorted(getattr(deps, "db_checks", {}).items())
        )
        or "none",
        extra={
            "backend": deps.config.db_backend,
            "db_ready": getattr(deps, "db_ready", False),
            "db_checks": dict(getattr(deps, "db_checks", {})),
            "stage": "api.startup",
            "outcome": "success",
        },
    )
    if deps.config.db_backend == "in_memory":
        logging.getLogger(__name__).warning(
            "startup.db_backend_in_memory",
            extra={"hint": "set DB_BACKEND=supabase for persistent remote writes"},
        )
    cron_job: ClusterCronJob | None = None
    if deps.config.cluster_cron_enabled:
        if deps.config.db_backend == "supabase" and not deps.db_ready:
            logging.getLogger(__name__).warning(
                "startup.cluster_cron_skipped db_ready=False checks=%s",
                ",".join(
                    f"{k}:{'ok' if v else 'fail'}"
                    for k, v in sorted(deps.db_checks.items())
                ),
                extra={
                    "stage": "api.startup",
                    "db_ready": False,
                    "db_checks": dict(deps.db_checks),
                    "hint": "fix SUPABASE_URL/secrets or apply migrations; or CLUSTER_CRON_ENABLED=false",
                },
            )
        else:
            cron_job = ClusterCronJob(
                orchestrator=deps.story_cluster_orchestrator,
                interval_s=deps.config.cluster_cron_interval_s,
                min_size_guard=deps.config.cluster_min_size,
            )
            cron_job.start()
    try:
        yield
        if _shutdown_reason == "unknown":
            _shutdown_reason = "graceful"
    except Exception as exc:
        log_runtime_exception(
            logging.getLogger(__name__),
            exc,
            stage="api.lifespan",
            shutdown_reason=_shutdown_reason,
        )
        raise
    finally:
        if cron_job is not None:
            cron_job.stop()
        logging.getLogger(__name__).info(
            "shutdown.lifecycle",
            extra={"shutdown_reason": _shutdown_reason},
        )
        _restore_signal_reason_hooks(signal_hooks)


app = FastAPI(title="doge-complaints-gateway", version="0.1.0", lifespan=_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["x-trace-id", "authorization"],
)


@app.middleware("http")
async def runtime_exception_diagnostics(request: Request, call_next: Any) -> Any:
    trace_id = _read_trace_id(request)
    try:
        return await call_next(request)
    except Exception as exc:
        log_runtime_exception(
            logging.getLogger("core.api"),
            exc,
            stage="api.http",
            trace_id=trace_id,
            path=request.url.path,
            method=request.method,
        )
        raise


@lru_cache(maxsize=1)
def _cached_dependencies() -> ApiDependencies:
    return build_api_dependencies()


def _clear_api_dependencies_cache() -> None:
    _cached_dependencies.cache_clear()


def get_api_dependencies() -> ApiDependencies:
    return _cached_dependencies()


def _json_http_status(payload: dict[str, Any]) -> int:
    return 401 if "error" in payload and payload["error"]["code"] == "UNAUTHORIZED" else 200


def _read_trace_id(request: Request) -> str:
    incoming = request.headers.get("x-trace-id")
    return ensure_trace_id(incoming)


def _unauthorized_response(exc: Exception, *, trace_id: str) -> JSONResponse:
    envelope = build_error_envelope(exc, trace_id=trace_id).as_dict()
    return JSONResponse(content=envelope, status_code=401)


@app.exception_handler(VerificationRequiredError)
async def verification_required_handler(
    request: Request, exc: VerificationRequiredError
) -> JSONResponse:
    trace_id = _read_trace_id(request)
    envelope = build_error_envelope(exc, trace_id=trace_id).as_dict()
    return JSONResponse(content=envelope, status_code=403)


@app.exception_handler(UserTokenIntrospectionUnavailableError)
async def user_token_introspection_unavailable_handler(
    request: Request, exc: UserTokenIntrospectionUnavailableError
) -> JSONResponse:
    trace_id = _read_trace_id(request)
    envelope = build_error_envelope(exc, trace_id=trace_id).as_dict()
    return JSONResponse(content=envelope, status_code=503)


@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    trace_id = _read_trace_id(request)
    return _unauthorized_response(exc, trace_id=trace_id)


@app.exception_handler(ConfigError)
async def config_error_handler(request: Request, exc: ConfigError) -> JSONResponse:
    trace_id = _read_trace_id(request)
    envelope = build_error_envelope(exc, trace_id=trace_id).as_dict()
    return JSONResponse(content=envelope, status_code=500)


def require_service_auth(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> None:
    deps.service_auth.require(dict(request.headers.items()), mandatory=False)


def require_public_content_service_auth(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> None:
    deps.service_auth.require(dict(request.headers.items()), mandatory=True)


_STORY_DRAFT_WRITE_DEPS = [Depends(require_public_content_service_auth)]


def require_story_draft_read_user(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> None:
    """GW-DRAFT-02 audit G1: browser Bearer → identity /me; active session only (no phone_verified gate)."""
    bearer = extract_authorization_bearer(dict(request.headers.items()))
    if bearer is None:
        raise UserTokenMissingError("Missing user token.")
    client = deps.identity_me
    if client is None:
        raise UserTokenIntrospectionUnavailableError("Identity /me is not configured.")
    try:
        result = client.fetch_me(bearer)
    except IdentityMeError as exc:
        raise UserTokenIntrospectionUnavailableError(
            "Identity /me request failed."
        ) from exc
    if not result.active:
        raise UserTokenIntrospectionError("User token is not active.")
    assert result.sub is not None
    request.state.user_introspection = result


def require_story_draft_submit_user(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> None:
    """GW-DRAFT-02: browser Supabase Bearer → identity /me + phone_verified gate."""
    bearer = extract_authorization_bearer(dict(request.headers.items()))
    if bearer is None:
        raise UserTokenMissingError("Missing user token.")
    client = deps.identity_me
    if client is None:
        raise UserTokenIntrospectionUnavailableError("Identity /me is not configured.")
    try:
        result = client.fetch_me(bearer)
    except IdentityMeError as exc:
        raise UserTokenIntrospectionUnavailableError(
            "Identity /me request failed."
        ) from exc

    gate = evaluate_verification_gate(result)
    if gate is VerificationGateOutcome.UNAUTHORIZED:
        raise UserTokenIntrospectionError("User token is not active.")
    if gate is VerificationGateOutcome.VERIFICATION_REQUIRED:
        raise VerificationRequiredError(
            DEFAULT_VERIFICATION_REQUIRED_REASON,
            verify_url=build_verify_url(deps.config),
            reason=DEFAULT_VERIFICATION_REQUIRED_REASON,
        )

    assert result.sub is not None
    request.state.user_introspection = result


_STORY_DRAFT_READ_DEPS = [Depends(require_story_draft_read_user)]
_STORY_DRAFT_SUBMIT_DEPS = [Depends(require_story_draft_submit_user)]


@app.get("/health")
async def health(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_health(deps, trace_id=_read_trace_id(request))
    return JSONResponse(content=payload, status_code=_json_http_status(payload))


@app.get("/ready")
async def readiness(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_readiness(deps, trace_id=_read_trace_id(request))
    return JSONResponse(content=payload, status_code=_json_http_status(payload))


@app.get("/protected/status", dependencies=[Depends(require_service_auth)])
async def protected_status(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_protected_status(
        deps,
        headers=dict(request.headers.items()),
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=_json_http_status(payload))


@app.get("/metrics", dependencies=[Depends(require_service_auth)])
async def metrics(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_metrics(
        deps,
        headers=dict(request.headers.items()),
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=_json_http_status(payload))


@app.get("/demo/auth-page")
@app.get("/demo/auth-page/")
async def demo_auth_page() -> FileResponse:
    return FileResponse(_DEMO_DIR / "index.html", media_type="text/html")


@app.get("/demo/auth-page/styles.css")
async def demo_auth_styles() -> FileResponse:
    return FileResponse(_DEMO_DIR / "styles.css", media_type="text/css")


@app.options("/tallinn/issues")
async def tallinn_issues_options() -> Response:
    return Response(status_code=200)


@app.options("/tallinn/issues/{issue_id}")
async def tallinn_issue_options() -> Response:
    return Response(status_code=200)


@app.options("/tallinn/network-pulse")
async def tallinn_network_pulse_options() -> Response:
    return Response(status_code=200)


@app.get("/tallinn/network-pulse")
async def tallinn_network_pulse(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_network_pulse(deps, trace_id=_read_trace_id(request))
    return JSONResponse(content=payload, status_code=_json_http_status(payload))


@app.options("/tallinn/emerging-signals")
async def tallinn_emerging_signals_options() -> Response:
    return Response(status_code=200)


@app.get("/tallinn/emerging-signals")
async def tallinn_emerging_signals(
    request: Request,
    top_n: int = Query(default=10, ge=1, le=50),
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_emerging_signals(
        deps, top_n=top_n, trace_id=_read_trace_id(request)
    )
    return JSONResponse(content=payload, status_code=_json_http_status(payload))


@app.get("/tallinn/issues")
async def tallinn_issues_list(
    request: Request,
    status: list[str] | None = Query(default=None),
    type: str | None = Query(default=None),
    labels: list[str] | None = Query(default=None),
    institution: str | None = Query(default=None),
    created_after: str | None = Query(default=None),
    created_before: str | None = Query(default=None),
    geo_lat_min: float | None = Query(default=None),
    geo_lat_max: float | None = Query(default=None),
    geo_lon_min: float | None = Query(default=None),
    geo_lon_max: float | None = Query(default=None),
    geo_district: list[str] | None = Query(default=None),
    geo_settlement: list[str] | None = Query(default=None),
    geo_region: list[str] | None = Query(default=None),
    geo_country: list[str] | None = Query(default=None),
    geo_postal_code: list[str] | None = Query(default=None),
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_tallinn_issues_list(
        deps,
        status=status,
        issue_type=type,
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
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=_json_http_status(payload))


@app.get("/tallinn/issues/{issue_id}")
async def tallinn_issue_get(
    issue_id: str,
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_tallinn_issue_get(
        deps,
        issue_id=issue_id,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.post("/tallinn/issues", dependencies=[Depends(require_public_content_service_auth)])
async def tallinn_issue_create(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    body = await request.json()
    if not isinstance(body, dict):
        body = {}
    payload, status_code = handle_tallinn_issue_create(
        deps,
        body=body,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.post("/story-drafts", dependencies=_STORY_DRAFT_WRITE_DEPS)
async def story_draft_create(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    body = await request.json()
    if not isinstance(body, dict):
        body = {}
    payload, status_code = handle_story_draft_create(
        deps,
        payload=body,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.get("/story-drafts/current", dependencies=_STORY_DRAFT_READ_DEPS)
async def story_draft_current(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    user_introspection = getattr(request.state, "user_introspection", None)
    assert user_introspection is not None
    assert user_introspection.sub is not None
    payload, status_code = handle_story_draft_current(
        deps,
        submitter_external_user_id=user_introspection.sub,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.get("/story-drafts/{draft_id}", dependencies=_STORY_DRAFT_READ_DEPS)
async def story_draft_get(
    request: Request,
    draft_id: str,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    user_introspection = getattr(request.state, "user_introspection", None)
    assert user_introspection is not None
    payload, status_code = handle_story_draft_get(
        deps,
        draft_id=draft_id,
        submitter_external_user_id=user_introspection.sub,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.post(
    "/story-drafts/{draft_id}/submit",
    dependencies=_STORY_DRAFT_SUBMIT_DEPS,
)
async def story_draft_submit(
    request: Request,
    draft_id: str,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    user_introspection = getattr(request.state, "user_introspection", None)
    assert user_introspection is not None
    payload, status_code = handle_story_draft_submit(
        deps,
        draft_id=draft_id,
        user_introspection=user_introspection,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.get("/story-activity", dependencies=_STORY_DRAFT_READ_DEPS)
async def story_activity(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    user_introspection = getattr(request.state, "user_introspection", None)
    assert user_introspection is not None
    assert user_introspection.sub is not None
    payload, status_code = handle_story_activity(
        deps,
        submitter_external_user_id=user_introspection.sub,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.post("/telemetry/label-misses")
async def telemetry_label_misses(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    body = await request.json()
    if not isinstance(body, dict):
        body = {}
    payload, status_code = handle_label_miss_telemetry(
        deps,
        body=body,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)


def _parse_port(raw: str | None) -> int:
    if raw is None or not raw.strip():
        return 8000
    try:
        parsed = int(raw)
    except ValueError as exc:
        raise ValueError(f"Invalid PORT={raw!r}. Expected integer.") from exc
    if not (1 <= parsed <= 65535):
        raise ValueError(f"Invalid PORT={parsed}. Expected range 1..65535.")
    return parsed


def run_asgi_server(*, host: str | None = None, port: int | None = None) -> None:
    resolved_host = host or os.getenv("HOST", "127.0.0.1")
    resolved_port = port if port is not None else _parse_port(os.getenv("PORT"))
    uvicorn.run("core.api.asgi_app:app", host=resolved_host, port=resolved_port)


if __name__ == "__main__":
    run_asgi_server()
