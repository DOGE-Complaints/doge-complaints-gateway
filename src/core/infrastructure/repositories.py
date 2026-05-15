from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
import logging
from typing import Mapping

from core.domain import (
    HealthReport,
    IdempotencyRecord,
    SignalProfileRecord,
    StoryLifecycleStatus,
    StoryRecord,
)

logger = logging.getLogger(__name__)


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
        logger.info(
            "repo.in_memory.save_story_done story_id=%s",
            record.story_id,
            extra={
                "story_id": record.story_id,
                "backend": "in_memory",
                "repository_class": self.__class__.__name__,
                "stage": "repository.in_memory.save_story",
                "outcome": "success",
            },
        )
        return record

    def get_story(self, story_id: str) -> StoryRecord | None:
        assert self._records is not None
        return self._records.get(story_id)

    def list_stories(self) -> list[StoryRecord]:
        assert self._records is not None
        return list(self._records.values())

    def list_stories_ready_for_clustering(self) -> list[StoryRecord]:
        return [
            s
            for s in self.list_stories()
            if s.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
        ]

    def update_lifecycle_status(self, story_id: str, status: StoryLifecycleStatus) -> None:
        current = self.get_story(story_id)
        if current is None:
            raise ValueError(f"Unknown story_id={story_id!r}")
        self.save_story(
            replace(current, lifecycle_status=status, updated_at=datetime.now(UTC))
        )


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
        self._rows = [row for row in self._rows if row.get("issue_id") != issue_id]
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
        existing = self._rows.get(issue_id)
        existing_story_ids = existing[1] if existing is not None else ()
        merged_story_ids = tuple(sorted(set(existing_story_ids).union(set(story_ids))))
        self._rows[issue_id] = (cluster_id, merged_story_ids)


@dataclass
class InMemoryStorySignalStore:
    _rows: dict[tuple[str, str], dict[str, str]] | None = None

    def __post_init__(self) -> None:
        if self._rows is None:
            self._rows = {}

    def save_signals(self, story_id: str, policy: str, signals: Mapping[str, str]) -> None:
        assert self._rows is not None
        self._rows[(story_id, policy)] = dict(signals)

    def get_signals(self, story_id: str, policy: str) -> Mapping[str, str] | None:
        assert self._rows is not None
        row = self._rows.get((story_id, policy))
        return dict(row) if row is not None else None


@dataclass
class InMemoryClusterMembershipStore:
    _story_lens_to_cluster: dict[tuple[str, str], str] | None = None

    def __post_init__(self) -> None:
        if self._story_lens_to_cluster is None:
            self._story_lens_to_cluster = {}

    def save_membership(self, story_id: str, lens: str, cluster_id: str) -> None:
        assert self._story_lens_to_cluster is not None
        self._story_lens_to_cluster[(story_id, lens)] = cluster_id

    def get_cluster_members(self, cluster_id: str, lens: str) -> list[str]:
        assert self._story_lens_to_cluster is not None
        return sorted(
            sid
            for (sid, ln), cid in self._story_lens_to_cluster.items()
            if ln == lens and cid == cluster_id
        )

