from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from core.domain import (
    HealthReport,
    IdempotencyRecord,
    SignalProfileRecord,
    StoryRecord,
)


@dataclass(frozen=True)
class InMemoryHealthRepository:
    default_status: str = "ok"

    def get_health(self) -> HealthReport:
        return HealthReport(status=self.default_status)


@dataclass
class InMemoryStoryRepository:
    _records: dict[str, StoryRecord] | None = None

    def __post_init__(self) -> None:
        if self._records is None:
            self._records = {}

    def save_story(self, record: StoryRecord) -> StoryRecord:
        assert self._records is not None
        self._records[record.story_id] = record
        return record

    def get_story(self, story_id: str) -> StoryRecord | None:
        assert self._records is not None
        return self._records.get(story_id)

    def list_stories(self) -> list[StoryRecord]:
        assert self._records is not None
        return list(self._records.values())


@dataclass
class InMemoryIdempotencyRepository:
    _records: dict[str, IdempotencyRecord] | None = None

    def __post_init__(self) -> None:
        if self._records is None:
            self._records = {}

    def get_by_key(self, key: str) -> IdempotencyRecord | None:
        assert self._records is not None
        return self._records.get(key)

    def save(self, record: IdempotencyRecord) -> IdempotencyRecord:
        assert self._records is not None
        self._records[record.key] = record
        return record


@dataclass
class InMemorySignalProfileRepository:
    _versions: dict[str, list[SignalProfileRecord]] | None = None

    def __post_init__(self) -> None:
        if self._versions is None:
            self._versions = {}

    def save_version(self, profile: SignalProfileRecord) -> SignalProfileRecord:
        assert self._versions is not None
        versions = self._versions.setdefault(profile.story_id, [])
        versions.append(profile)
        return profile

    def get_latest(self, story_id: str) -> SignalProfileRecord | None:
        assert self._versions is not None
        versions = self._versions.get(story_id, [])
        if not versions:
            return None
        return versions[-1]

    def get_versions(self, story_id: str) -> list[SignalProfileRecord]:
        assert self._versions is not None
        return list(self._versions.get(story_id, []))


@dataclass
class InMemoryStoryEmbeddingStore:
    _rows: list[dict[str, object]] | None = None

    def __post_init__(self) -> None:
        if self._rows is None:
            self._rows = []

    def save_story_embedding(
        self,
        *,
        story_id: str,
        model_name: str,
        embedding_vector: tuple[float, ...],
        source_checksum: str,
        embedding_policy_version: str,
    ) -> None:
        assert self._rows is not None
        self._rows.append(
            {
                "story_id": story_id,
                "model_name": model_name,
                "embedding_vector": tuple(embedding_vector),
                "source_checksum": source_checksum,
                "embedding_policy_version": embedding_policy_version,
                "created_at": datetime.now(UTC),
            }
        )


@dataclass
class InMemoryIssueProjectionStore:
    _rows: dict[str, dict[str, object]] | None = None

    def __post_init__(self) -> None:
        if self._rows is None:
            self._rows = {}

    def save_projection(
        self,
        *,
        issue_id: str,
        status: str,
        payload: dict[str, object],
        policy_version: str,
    ) -> None:
        assert self._rows is not None
        self._rows[issue_id] = {
            "issue_id": issue_id,
            "status": status,
            "payload": dict(payload),
            "policy_version": policy_version,
            "updated_at": datetime.now(UTC),
        }


@dataclass
class InMemoryIssueProjectionEmbeddingStore:
    _rows: list[dict[str, object]] | None = None

    def __post_init__(self) -> None:
        if self._rows is None:
            self._rows = []

    def save_projection_embedding(
        self,
        *,
        issue_id: str,
        model_name: str,
        embedding_vector: tuple[float, ...],
        source_checksum: str,
        embedding_policy_version: str,
    ) -> None:
        assert self._rows is not None
        self._rows.append(
            {
                "issue_id": issue_id,
                "model_name": model_name,
                "embedding_vector": tuple(embedding_vector),
                "source_checksum": source_checksum,
                "embedding_policy_version": embedding_policy_version,
                "created_at": datetime.now(UTC),
            }
        )


@dataclass
class InMemoryIssueStoryLinkStore:
    _rows: dict[str, tuple[str, tuple[str, ...]]] | None = None

    def __post_init__(self) -> None:
        if self._rows is None:
            self._rows = {}

    def save_issue_story_links(
        self,
        *,
        issue_id: str,
        cluster_id: str,
        story_ids: tuple[str, ...],
    ) -> None:
        assert self._rows is not None
        self._rows[issue_id] = (cluster_id, tuple(story_ids))

