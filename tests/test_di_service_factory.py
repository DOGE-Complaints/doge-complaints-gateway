from __future__ import annotations

from core.infrastructure import DefaultServiceFactory, InMemoryHealthRepository
from core.infrastructure.repositories import (
    InMemoryIdempotencyRepository,
    InMemoryStoryRepository,
)


def test_default_service_factory_resolves_health_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        story_repository=InMemoryStoryRepository(),
    )
    service = factory.get_health_service()
    assert service.get_status() == "ok"


def test_default_service_factory_resolves_story_intake_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        story_repository=InMemoryStoryRepository(),
    )
    service = factory.get_story_intake_service()
    assert service.repository is not None

