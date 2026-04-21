from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Mapping, Protocol


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
class StoryGeoSnapshot:
    """Normalized geo result attached to a story (cluster lenses, audit)."""

    normalized_label: str
    latitude: float
    longitude: float
    confidence: float
    provider: str
    cluster_tags: tuple[str, ...] = ()


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
    geo: StoryGeoSnapshot | None = None
    origin_source: str | None = None
    origin_conversation_id: str | None = None
    origin_tool_call_id: str | None = None
    privacy_contains_pii: bool = False
    privacy_redaction_requested: bool = False


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


class SignalDimension(StrEnum):
    TOPIC = "topic"
    SYSTEM_FAILURE = "system_failure"
    NEED = "need"
    DESIRED_STATE = "desired_state"
    REPEATABILITY = "repeatability"
    RELEVANCE = "relevance"


@dataclass(frozen=True)
class SignalProfileRecord:
    story_id: str
    version: int
    user_asserted: Mapping[str, str]
    system_inferred: Mapping[str, str]
    created_at: datetime


class SignalProfileRepository(Protocol):
    def save_version(self, profile: SignalProfileRecord) -> SignalProfileRecord:
        """Persist profile version."""

    def get_latest(self, story_id: str) -> SignalProfileRecord | None:
        """Get latest profile version by story id."""

    def get_versions(self, story_id: str) -> list[SignalProfileRecord]:
        """Get all profile versions for a story."""

