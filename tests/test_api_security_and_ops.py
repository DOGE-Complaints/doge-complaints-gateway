from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, cast

import pytest  # pyright: ignore[reportMissingImports]

from core.api import (
    ApiDependencies,
    ApiMetrics,
    handle_health,
    handle_metrics,
    handle_protected_status,
    handle_readiness,
)
from core.api.security import (
    ServiceTokenAuth,
    UnauthorizedError,
    build_service_auth_from_env,
    extract_service_token,
)
from core.application import HealthService


@dataclass(frozen=True)
class _OkService:
    def get_status(self) -> str:
        return "ok"


def _ok_health_service() -> HealthService:
    return cast(HealthService, _OkService())


@dataclass(frozen=True)
class _DummyIntakeService:
    pass


@dataclass(frozen=True)
class _DummyStoryClusterOrchestrator:
    pass


def _deps_base() -> dict[str, Any]:
    return {
        "health_service": _ok_health_service(),
        "story_intake_service": cast(Any, _DummyIntakeService()),
        "story_cluster_orchestrator": cast(Any, _DummyStoryClusterOrchestrator()),
        "issue_create_service": cast(Any, object()),
        "issue_projection_read_store": cast(Any, object()),
        "network_pulse_service": cast(Any, object()),
        "metrics": ApiMetrics(),
    }


def test_extract_service_token_bearer() -> None:
    assert (
        extract_service_token({"Authorization": "Bearer secret-token"})
        == "secret-token"
    )


def test_extract_service_token_x_header() -> None:
    assert extract_service_token({"X-Service-Token": " abc "}) == "abc"


def test_protected_route_rejects_without_token_when_auth_enabled() -> None:
    deps = ApiDependencies(
        **_deps_base(),
        service_auth=ServiceTokenAuth.from_secret("expected-secret"),
    )
    out = handle_protected_status(deps, headers={}, trace_id="t1")
    assert out["error"]["code"] == "UNAUTHORIZED"
    assert out["trace_id"] == "t1"
    assert deps.metrics.auth_failures == 1


def test_protected_route_accepts_bearer_token() -> None:
    deps = ApiDependencies(
        **_deps_base(),
        service_auth=ServiceTokenAuth.from_secret("expected-secret"),
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
        **_deps_base(),
        service_auth=ServiceTokenAuth.disabled(),
    )
    out = handle_protected_status(deps, headers={}, trace_id="t3")
    assert out["data"]["service"] == "authenticated"


def test_build_service_auth_from_env() -> None:
    unset = build_service_auth_from_env({})
    assert unset.is_enabled() is False
    assert unset.mandatory is True
    with pytest.raises(UnauthorizedError):
        unset.require({}, mandatory=True)
    enabled = build_service_auth_from_env({"SERVICE_API_TOKEN": "x"})
    assert enabled.is_enabled() is True
    assert enabled.mandatory is True


def test_extract_user_token_reads_x_user_token() -> None:
    from core.api.security import extract_user_token

    assert extract_user_token({"X-User-Token": "  user-tok  "}) == "user-tok"
    assert extract_user_token({}) is None


def test_readiness_and_metrics_increment_counters() -> None:
    deps = ApiDependencies(**_deps_base())
    readiness = handle_readiness(deps, trace_id="r1")
    handle_metrics(deps, headers={}, trace_id="m1")
    assert deps.metrics.readiness_requests == 1
    assert deps.metrics.metrics_requests == 1
    assert readiness["data"]["db"]["checks"] == {}
    m = handle_metrics(deps, headers={}, trace_id="m2")
    assert m["data"]["health_requests"] == 0
    assert m["data"]["metrics_requests"] == 2


def test_metrics_alert_contract_shape() -> None:
    metrics = ApiMetrics()
    metrics.record_auth_failure()
    alert = metrics.alert_contract()
    assert alert["auth_failures"] == 1
    assert alert["auth_failures_threshold"] == 1
    assert alert["auth_failure_alert"] is True


def test_health_logs_structured_trace(caplog: Any) -> None:
    deps = ApiDependencies(**_deps_base())
    with caplog.at_level(logging.INFO, logger="core.api"):
        handle_health(deps, trace_id="trace-structured")
    assert any(
        getattr(rec, "trace_id", None) == "trace-structured" for rec in caplog.records
    )


def test_metrics_rejects_without_token_when_auth_enabled() -> None:
    deps = ApiDependencies(
        **_deps_base(),
        service_auth=ServiceTokenAuth.from_secret("expected-secret"),
    )
    out = handle_metrics(deps, headers={}, trace_id="m-auth-err")
    assert out["error"]["code"] == "UNAUTHORIZED"
    assert out["trace_id"] == "m-auth-err"
    assert deps.metrics.auth_failures == 1


def test_metrics_accepts_bearer_token_when_auth_enabled() -> None:
    deps = ApiDependencies(
        **_deps_base(),
        service_auth=ServiceTokenAuth.from_secret("expected-secret"),
    )
    out = handle_metrics(
        deps,
        headers={"Authorization": "Bearer expected-secret"},
        trace_id="m-auth-ok",
    )
    assert out["data"]["metrics_requests"] == 1
    assert out["trace_id"] == "m-auth-ok"
