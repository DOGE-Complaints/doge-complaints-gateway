from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol


@dataclass(frozen=True)
class HealthReport:
    status: str


class HealthRepository(Protocol):
    def get_health(self) -> HealthReport:
        """Return current health snapshot."""


class StoryLifecycleStatus(StrEnum):
    ACCEPTED = "accepted"
    PARTIAL_READY = "partial_ready"
    READY_FOR_PROFILE = "ready_for_profile"


@dataclass(frozen=True)
class StoryRecord:
    story_id: str
    schema_version: str
    narrative_original_text: str
    submitter_external_user_id: str
    submitter_identity_issuer: str | None
    lifecycle_status: StoryLifecycleStatus
    created_at: datetime
    updated_at: datetime


class StoryRepository(Protocol):
    def save_story(self, record: StoryRecord) -> StoryRecord:
        """Persist a story record."""

    def get_story(self, story_id: str) -> StoryRecord | None:
        """Fetch a story record by id."""


@dataclass(frozen=True)
class IdempotencyRecord:
    key: str
    story_id: str
    created_at: datetime


class IdempotencyRepository(Protocol):
    def get_by_key(self, key: str) -> IdempotencyRecord | None:
        """Fetch idempotency record by key."""

    def save(self, record: IdempotencyRecord) -> IdempotencyRecord:
        """Persist idempotency record."""

