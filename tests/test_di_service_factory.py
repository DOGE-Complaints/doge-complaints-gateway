from __future__ import annotations

from core.infrastructure import DefaultServiceFactory, InMemoryHealthRepository
from core.infrastructure.repositories import (
    InMemoryIdempotencyRepository,
    InMemorySignalProfileRepository,
    InMemoryStoryRepository,
)


def test_default_service_factory_resolves_health_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
    )
    service = factory.get_health_service()
    assert service.get_status() == "ok"


def test_default_service_factory_resolves_story_intake_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
    )
    service = factory.get_story_intake_service()
    assert service.repository is not None


def test_default_service_factory_resolves_signal_profile_service() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
    )
    service = factory.get_signal_profile_service()
    assert service.repository is not None


def test_default_service_factory_resolves_clustering_engine() -> None:
    factory = DefaultServiceFactory(
        health_repository=InMemoryHealthRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        signal_profile_repository=InMemorySignalProfileRepository(),
        story_repository=InMemoryStoryRepository(),
    )
    engine = factory.get_clustering_engine()
    assert engine is not None

