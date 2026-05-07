from __future__ import annotations

import os
from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path
from typing import Any

import uvicorn  # pyright: ignore[reportMissingImports]
from fastapi import Depends, FastAPI, Request  # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse, JSONResponse  # pyright: ignore[reportMissingImports]

from core.api.dependencies import ApiDependencies, build_api_dependencies
from core.api.envelope import build_error_envelope, ensure_trace_id
from core.api.handlers import (
    handle_health,
    handle_metrics,
    handle_protected_status,
    handle_readiness,
    handle_story_intake,
)
from core.api.security import UnauthorizedError
from core.config import ConfigError
from core.scheduler import ClusterCronJob

PUBLIC_ROUTES: tuple[str, ...] = (
    "/health",
    "/ready",
    "/demo/auth-page",
    "/intake/stories",
)
PROTECTED_ROUTES: tuple[str, ...] = ("/protected/status", "/metrics")
_DEMO_DIR = Path(__file__).resolve().parents[3] / "demo" / "auth-page"

@asynccontextmanager
async def _lifespan(_: FastAPI):
    deps = get_api_dependencies()
    cron_job: ClusterCronJob | None = None
    if deps.config.cluster_cron_enabled:
        cron_job = ClusterCronJob(
            orchestrator=deps.story_cluster_orchestrator,
            interval_s=deps.config.cluster_cron_interval_s,
            min_size_guard=deps.config.cluster_min_size,
        )
        cron_job.start()
    try:
        yield
    finally:
        if cron_job is not None:
            cron_job.stop()


app = FastAPI(title="doge-complaints-gateway", version="0.1.0", lifespan=_lifespan)


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
    deps.service_auth.require(dict(request.headers.items()))


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


@app.post("/intake/stories")
async def intake_stories(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = await request.json()
    envelope, status_code = handle_story_intake(
        deps,
        payload=payload,
        idempotency_key=request.headers.get("idempotency-key"),
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=envelope, status_code=status_code)


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
