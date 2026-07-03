from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime

from core.projection.columnar_storage import (
    assemble_public_issue_from_storage_row,
    payload_to_storage_fields,
    storage_fields_to_sqlite_values,
)
from core.projection.read_filters import filter_projection_rows
import logging
from typing import Mapping

from core.domain import (
    HealthReport,
    IdempotencyRecord,
    SignalProfileRecord,
    StoryDraftRecord,
    StoryLifecycleStatus,
    StoryRecord,
)

logger = logging.getLogger(__name__)


def _row_created_at_text(row: dict[str, object]) -> str:
    created_at = row.get("created_at")
    if isinstance(created_at, datetime):
        return created_at.isoformat()
    if created_at:
        return str(created_at)
    updated_at = row.get("updated_at")
    if isinstance(updated_at, datetime):
        return updated_at.isoformat()
    return str(updated_at or "")


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
class InMemoryStoryDraftRepository:
    _records: dict[str, StoryDraftRecord] | None = None

    def __post_init__(self) -> None:
        if self._records is None:
            self._records = {}

    def save_draft(self, record: StoryDraftRecord) -> StoryDraftRecord:
        assert self._records is not None
        self._records[record.draft_id] = record
        return record

    def get_draft(self, draft_id: str) -> StoryDraftRecord | None:
        assert self._records is not None
        record = self._records.get(draft_id)
        if record is None:
            return None
        if record.expires_at <= datetime.now(UTC):
            self._records.pop(draft_id, None)
            return None
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
        now = datetime.now(UTC)
        storage_fields = storage_fields_to_sqlite_values(payload_to_storage_fields(payload))
        self._rows[issue_id] = {
            "issue_id": issue_id,
            "status": status,
            "policy_version": policy_version,
            "created_at": now,
            "updated_at": now,
            **storage_fields,
        }

    def list_projections(
        self,
        *,
        status: list[str] | None = None,
        issue_type: str | None = None,
        labels: list[str] | None = None,
        institution: str | None = None,
        created_after: str | None = None,
        created_before: str | None = None,
        geo_lat_min: float | None = None,
        geo_lat_max: float | None = None,
        geo_lon_min: float | None = None,
        geo_lon_max: float | None = None,
        geo_district: list[str] | None = None,
        geo_settlement: list[str] | None = None,
        geo_region: list[str] | None = None,
        geo_country: list[str] | None = None,
        geo_postal_code: list[str] | None = None,
    ) -> list[dict[str, object]]:
        assert self._rows is not None
        rows: list[tuple[str, str, dict[str, object], str]] = []
        for issue_id, row in self._rows.items():
            created_at_text = _row_created_at_text(row)
            row_dict = {
                "issue_id": issue_id,
                "status": str(row["status"]),
                "created_at": created_at_text,
                "issue_type": row.get("issue_type"),
                "labels_json": row.get("labels_json"),
                "title_json": row.get("title_json"),
                "summary_json": row.get("summary_json"),
                "description_json": row.get("description_json"),
                "institution_json": row.get("institution_json"),
                "geo_json": row.get("geo_json"),
                "original_locale_json": row.get("original_locale_json"),
                "arweave_txid": row.get("arweave_txid"),
                "image_txid": row.get("image_txid"),
                "image_hash": row.get("image_hash"),
            }
            legacy_payload = row.get("payload")
            assembled = assemble_public_issue_from_storage_row(
                row_dict,
                legacy_payload_json=legacy_payload if isinstance(legacy_payload, dict) else None,
            )
            rows.append((issue_id, str(row["status"]), assembled, created_at_text))
        ordered = sorted(rows, key=lambda item: item[3], reverse=True)
        return filter_projection_rows(
            ordered,
            status=status,
            issue_type=issue_type,
            labels=labels,
            institution=institution,
            created_after=created_after,
            created_before=created_before,
            geo_lat_min=geo_lat_min,
            geo_lat_max=geo_lat_max,
            geo_lon_min=geo_lon_min,
            geo_lon_max=geo_lon_max,
            geo_district=geo_district,
            geo_settlement=geo_settlement,
            geo_region=geo_region,
            geo_country=geo_country,
            geo_postal_code=geo_postal_code,
        )

    def get_projection(self, issue_id: str) -> dict[str, object] | None:
        assert self._rows is not None
        row = self._rows.get(issue_id)
        if row is None:
            return None
        created_at_text = _row_created_at_text(row)
        row_dict = {
            "issue_id": issue_id,
            "status": str(row["status"]),
            "created_at": created_at_text,
            "issue_type": row.get("issue_type"),
            "labels_json": row.get("labels_json"),
            "title_json": row.get("title_json"),
            "summary_json": row.get("summary_json"),
            "description_json": row.get("description_json"),
            "institution_json": row.get("institution_json"),
            "geo_json": row.get("geo_json"),
            "original_locale_json": row.get("original_locale_json"),
            "arweave_txid": row.get("arweave_txid"),
            "image_txid": row.get("image_txid"),
            "image_hash": row.get("image_hash"),
        }
        legacy_payload = row.get("payload")
        assembled = assemble_public_issue_from_storage_row(
            row_dict,
            legacy_payload_json=legacy_payload if isinstance(legacy_payload, dict) else None,
        )
        from core.projection.read_filters import merge_projection_columns

        return merge_projection_columns(
            issue_id=issue_id,
            row_status=str(row["status"]),
            payload=assembled,
            created_at=created_at_text,
        )


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


@dataclass
class InMemoryLabelTranslationMissStore:
    _rows: dict[tuple[str, str], tuple[int, str]] | None = None

    def __post_init__(self) -> None:
        if self._rows is None:
            self._rows = {}

    def record_miss(self, label_key: str, locale: str) -> None:
        assert self._rows is not None
        key = (label_key, locale)
        count, _ = self._rows.get(key, (0, ""))
        self._rows[key] = (count + 1, datetime.now(UTC).isoformat())

    def get_miss_count(self, label_key: str, locale: str) -> int:
        assert self._rows is not None
        row = self._rows.get((label_key, locale))
        return row[0] if row is not None else 0

