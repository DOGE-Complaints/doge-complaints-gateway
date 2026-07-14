from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class HealthReport:
    status: str


class HealthRepository(Protocol):
    def get_health(self) -> HealthReport:
        """Return current health snapshot."""
        ...


class StoryLifecycleStatus(StrEnum):
    ACCEPTED = "accepted"
    PARTIAL_READY = "partial_ready"
    READY_FOR_PROFILE = "ready_for_profile"
    CLUSTERED = "clustered"


@dataclass(frozen=True)
class StoryGeoSnapshot:
    """Normalized geo result attached to a story (cluster lenses, audit)."""

    normalized_label: str
    latitude: float
    longitude: float
    confidence: float
    provider: str
    cluster_tags: tuple[str, ...] = ()
    admin_district: str | None = None
    admin_settlement: str | None = None
    admin_region: str | None = None
    admin_country: str | None = None


@dataclass(frozen=True)
class StoryRecord:
    story_id: str
    schema_version: str
    narrative_original_text: str
    submitter_external_user_id: str
    submitter_identity_issuer: str
    lifecycle_status: StoryLifecycleStatus
    created_at: datetime
    updated_at: datetime
    narrative_language: str | None = None
    narrative_title: dict[str, str] | None = None
    narrative_description: dict[str, str] | None = None
    narrative_summary: dict[str, str] | None = None
    narrative_institution: dict[str, str] | None = None
    narrative_session_language: str | None = None
    narrative_consistency_notes: str | None = None
    narrative_canonical_type: str | None = None
    narrative_canonical_labels: tuple[str, ...] = ()
    geo: StoryGeoSnapshot | None = None
    origin_source: str | None = None
    origin_conversation_id: str | None = None
    origin_tool_call_id: str | None = None
    privacy_contains_pii: bool = False
    privacy_redaction_requested: bool = False


class StoryRepository(Protocol):
    def save_story(self, record: StoryRecord) -> StoryRecord:
        """Persist a story record."""
        ...

    def get_story(self, story_id: str) -> StoryRecord | None:
        """Fetch a story record by id."""
        ...

    def list_stories(self) -> list[StoryRecord]:
        """List all persisted stories."""
        ...

    def list_stories_by_submitter(self, submitter_external_user_id: str) -> list[StoryRecord]:
        """List stories authored by submitter_external_user_id (GW-CAB-01)."""
        ...

    def list_stories_ready_for_clustering(self) -> list[StoryRecord]:
        """Stories eligible for clustering (typically READY_FOR_PROFILE)."""
        ...

    def update_lifecycle_status(self, story_id: str, status: StoryLifecycleStatus) -> None:
        """Advance lifecycle for clustering pipeline."""
        ...


@dataclass(frozen=True)
class IdempotencyRecord:
    key: str
    story_id: str
    created_at: datetime


class IdempotencyRepository(Protocol):
    def get_by_key(self, key: str) -> IdempotencyRecord | None:
        """Fetch idempotency record by key."""
        ...

    def save(self, record: IdempotencyRecord) -> IdempotencyRecord:
        """Persist idempotency record."""
        ...


@dataclass(frozen=True)
class StoryDraftRecord:
    """Ephemeral story intake payload stashed for browser handoff (GW-DRAFT-01)."""

    draft_id: str
    payload: dict[str, Any]
    created_at: datetime
    expires_at: datetime
    updated_at: datetime


class StoryDraftRepository(Protocol):
    def save_draft(self, record: StoryDraftRecord) -> StoryDraftRecord:
        """Persist a story draft; returns the saved record."""
        ...

    def get_draft(self, draft_id: str) -> StoryDraftRecord | None:
        """Fetch draft by id; None when unknown or past expires_at (TTL)."""
        ...

    def delete_draft(self, draft_id: str) -> None:
        """Remove draft after successful submit (GW-DRAFT-02)."""
        ...


class DraftOwnerRepository(Protocol):
    def set_owner(self, draft_id: str, submitter_external_user_id: str) -> None:
        """First-wins idempotent associate: first authenticated reader owns draft (GW-CAB-02, D-CAB02-1)."""
        ...

    def get_current_draft(
        self, submitter_external_user_id: str
    ) -> StoryDraftRecord | None:
        """Latest non-expired draft for user (join draft_owner×story_drafts, D-CAB02-3)."""
        ...


class SignalDimension(StrEnum):
    """Signal axes for profiles and clustering.

    Legacy six values remain for backward compatibility; civic-oriented axes
    extend the SA cluster-engine target state (gap G1-02).
    """

    TOPIC = "topic"
    SYSTEM_FAILURE = "system_failure"
    NEED = "need"
    DESIRED_STATE = "desired_state"
    REPEATABILITY = "repeatability"
    RELEVANCE = "relevance"
    CIVIC_DOMAIN = "civic_domain"
    FAILURE_PATTERN = "failure_pattern"
    CIVIC_WEIGHT = "civic_weight"
    DESIRED_OUTCOME = "desired_outcome"
    AFFECTED_GROUP = "affected_group"
    GEOGRAPHIC_DISTRICT = "geographic_district"
    CANONICAL_TYPE = "canonical_type"


class StorySignalStore(Protocol):
    def save_signals(self, story_id: str, policy: str, signals: Mapping[str, str]) -> None:
        """Persist extracted signals for a story under a named policy."""
        ...

    def get_signals(self, story_id: str, policy: str) -> Mapping[str, str] | None:
        """Return stored signals or None if missing."""
        ...


class ClusterMembershipStore(Protocol):
    def save_membership(self, story_id: str, lens: str, cluster_id: str) -> None:
        """Record story membership in a lens-specific cluster."""
        ...

    def get_cluster_members(self, cluster_id: str, lens: str) -> list[str]:
        """List story_ids belonging to cluster_id for lens."""
        ...


class LabelTranslationMissStore(Protocol):
    def record_miss(self, label_key: str, locale: str) -> None:
        """Increment aggregate miss counter for label_key + locale."""
        ...

    def get_miss_count(self, label_key: str, locale: str) -> int:
        """Return current miss_count for label_key + locale (0 if absent)."""
        ...


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
        ...

    def get_latest(self, story_id: str) -> SignalProfileRecord | None:
        """Get latest profile version by story id."""
        ...

    def get_versions(self, story_id: str) -> list[SignalProfileRecord]:
        """Get all profile versions for a story."""
        ...

