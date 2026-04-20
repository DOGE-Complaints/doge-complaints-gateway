from __future__ import annotations

from core.application import ServiceFactory
from core.domain import HealthRepository, IdempotencyRepository, StoryRepository
from core.infrastructure.repositories import (
    InMemoryHealthRepository,
    InMemoryIdempotencyRepository,
    InMemoryStoryRepository,
)
from core.infrastructure.service_factory import DefaultServiceFactory


def provide_health_repository() -> HealthRepository:
    return InMemoryHealthRepository()


def provide_story_repository() -> StoryRepository:
    return InMemoryStoryRepository()


def provide_idempotency_repository() -> IdempotencyRepository:
    return InMemoryIdempotencyRepository()


def provide_service_factory() -> ServiceFactory:
    return DefaultServiceFactory(
        health_repository=provide_health_repository(),
        story_repository=provide_story_repository(),
        idempotency_repository=provide_idempotency_repository(),
    )

