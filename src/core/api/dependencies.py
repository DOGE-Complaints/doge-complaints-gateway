from __future__ import annotations

from dataclasses import dataclass

from core.application import HealthService
from core.infrastructure import provide_service_factory


@dataclass(frozen=True)
class ApiDependencies:
    health_service: HealthService


def build_api_dependencies() -> ApiDependencies:
    service_factory = provide_service_factory()
    return ApiDependencies(health_service=service_factory.get_health_service())

