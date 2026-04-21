from __future__ import annotations

import logging
from dataclasses import dataclass

import pytest

from core.api import (
    ApiDependencies,
    ApiMetrics,
    ServiceTokenAuth,
    build_service_auth_from_env,
    extract_service_token,
    handle_health,
    handle_metrics,
    handle_protected_status,
    handle_readiness,
)


@dataclass(frozen=True)
class _OkService:
    def get_status(self) -> str:
        return "ok"


def test_extract_service_token_bearer() -> None:
    assert (
        extract_service_token({"Authorization": "Bearer secret-token"})
        == "secret-token"
    )


def test_extract_service_token_x_header() -> None:
    assert extract_service_token({"X-Service-Token": " abc "}) == "abc"


def test_protected_route_rejects_without_token_when_auth_enabled() -> None:
    deps = ApiDependencies(
        health_service=_OkService(),
        service_auth=ServiceTokenAuth.from_secret("expected-secret"),
        metrics=ApiMetrics(),
    )
    out = handle_protected_status(deps, headers={}, trace_id="t1")
    assert out["error"]["code"] == "UNAUTHORIZED"
    assert out["trace_id"] == "t1"
    assert deps.metrics.auth_failures == 1


def test_protected_route_accepts_bearer_token() -> None:
    deps = ApiDependencies(
        health_service=_OkService(),
        service_auth=ServiceTokenAuth.from_secret("expected-secret"),
        metrics=ApiMetrics(),
    )
    out = handle_protected_status(
        deps,
        headers={"Authorization": "Bearer expected-secret"},
        trace_id="t2",
    )
    assert out["data"]["service"] == "authenticated"
    assert out["trace_id"] == "t2"
    assert deps.metrics.protected_requests == 1


def test_service_auth_disabled_allows_protected_without_header() -> None:
    deps = ApiDependencies(
        health_service=_OkService(),
        service_auth=ServiceTokenAuth.disabled(),
        metrics=ApiMetrics(),
    )
    out = handle_protected_status(deps, headers={}, trace_id="t3")
    assert out["data"]["service"] == "authenticated"


def test_build_service_auth_from_env() -> None:
    assert build_service_auth_from_env({}).is_enabled() is False
    assert build_service_auth_from_env({"SERVICE_API_TOKEN": "x"}).is_enabled() is True


def test_readiness_and_metrics_increment_counters() -> None:
    deps = ApiDependencies(health_service=_OkService(), metrics=ApiMetrics())
    handle_readiness(deps, trace_id="r1")
    handle_metrics(deps, trace_id="m1")
    assert deps.metrics.readiness_requests == 1
    assert deps.metrics.metrics_requests == 1
    m = handle_metrics(deps, trace_id="m2")
    assert m["data"]["health_requests"] == 0
    assert m["data"]["metrics_requests"] == 2


def test_metrics_alert_contract_shape() -> None:
    metrics = ApiMetrics()
    metrics.record_auth_failure()
    alert = metrics.alert_contract()
    assert alert["auth_failures"] == 1
    assert alert["auth_failures_threshold"] == 1
    assert alert["auth_failure_alert"] is True


def test_health_logs_structured_trace(caplog: pytest.LogCaptureFixture) -> None:
    deps = ApiDependencies(health_service=_OkService(), metrics=ApiMetrics())
    with caplog.at_level(logging.INFO, logger="core.api"):
        handle_health(deps, trace_id="trace-structured")
    assert any(
        getattr(rec, "trace_id", None) == "trace-structured" for rec in caplog.records
    )
