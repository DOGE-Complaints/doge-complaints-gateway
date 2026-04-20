from __future__ import annotations

from core.infrastructure import DefaultServiceFactory, InMemoryHealthRepository


def test_default_service_factory_resolves_health_service() -> None:
    factory = DefaultServiceFactory(health_repository=InMemoryHealthRepository())
    service = factory.get_health_service()
    assert service.get_status() == "ok"

