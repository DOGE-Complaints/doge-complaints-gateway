from __future__ import annotations

from core.application import ServiceFactory
from core.domain import HealthRepository
from core.infrastructure.repositories import InMemoryHealthRepository
from core.infrastructure.service_factory import DefaultServiceFactory


def provide_health_repository() -> HealthRepository:
    return InMemoryHealthRepository()


def provide_service_factory() -> ServiceFactory:
    return DefaultServiceFactory(health_repository=provide_health_repository())

