from __future__ import annotations

from dataclasses import dataclass, field

from core.api.metrics import ApiMetrics
from core.api.security import ServiceTokenAuth, build_service_auth_from_env
from core.application import HealthService
from core.infrastructure import provide_service_factory


@dataclass(frozen=True)
class ApiDependencies:
    health_service: HealthService
    service_auth: ServiceTokenAuth = field(default_factory=ServiceTokenAuth.disabled)
    metrics: ApiMetrics = field(default_factory=ApiMetrics)


# Backward-compatible name used in tests and story docs
HandlerDependencies = ApiDependencies


def build_api_dependencies() -> ApiDependencies:
    service_factory = provide_service_factory()
    return ApiDependencies(
        health_service=service_factory.get_health_service(),
        service_auth=build_service_auth_from_env(),
        metrics=ApiMetrics(),
    )
