from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from core.domain import IdempotencyRecord, StoryLifecycleStatus, StoryRecord
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus, ReviewAuditEntry, ReviewDecision


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


@dataclass
class SqliteDatabase:
    connection: sqlite3.Connection

    @classmethod
    def from_url(cls, database_url: str) -> SqliteDatabase:
        if not database_url.startswith("sqlite:///"):
            raise ValueError(
                f"Unsupported database URL for sqlite backend: {database_url!r}."
            )
        db_path = database_url.removeprefix("sqlite:///")
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(db_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        return cls(connection=connection)

    def ensure_schema(self) -> None:
        self.connection.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS stories (
                story_id TEXT PRIMARY KEY,
                schema_version TEXT NOT NULL,
                narrative_original_text TEXT NOT NULL,
                narrative_language TEXT,
                narrative_title_hint TEXT,
                narrative_canonical_type TEXT,
                narrative_canonical_labels_json TEXT NOT NULL DEFAULT '[]',
                submitter_external_user_id TEXT NOT NULL,
                submitter_identity_issuer TEXT,
                lifecycle_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                origin_source TEXT,
                origin_conversation_id TEXT,
                origin_tool_call_id TEXT,
                privacy_contains_pii INTEGER NOT NULL DEFAULT 0,
                privacy_redaction_requested INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS idempotency_keys (
                key TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(story_id) REFERENCES stories(story_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS story_embeddings (
                embedding_id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id TEXT NOT NULL,
                model_name TEXT NOT NULL,
                embedding_vector_json TEXT NOT NULL,
                source_checksum TEXT NOT NULL,
                embedding_policy_version TEXT NOT NULL DEFAULT 'm2.story_embedding_policy.v1',
                created_at TEXT NOT NULL,
                FOREIGN KEY(story_id) REFERENCES stories(story_id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_story_embeddings_story_id
                ON story_embeddings(story_id);

            CREATE TABLE IF NOT EXISTS spa_issue_projections (
                issue_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                policy_version TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS spa_issue_projection_embeddings (
                embedding_id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_id TEXT NOT NULL,
                model_name TEXT NOT NULL,
                embedding_vector_json TEXT NOT NULL,
                source_checksum TEXT NOT NULL,
                embedding_policy_version TEXT NOT NULL DEFAULT 'm2.issue_embedding_policy.v1',
                created_at TEXT NOT NULL,
                FOREIGN KEY(issue_id) REFERENCES spa_issue_projections(issue_id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_issue_embeddings_issue_id
                ON spa_issue_projection_embeddings(issue_id);

            CREATE TABLE IF NOT EXISTS issue_candidates (
                candidate_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                cluster_id TEXT NOT NULL,
                story_ids_json TEXT NOT NULL,
                readiness_score INTEGER NOT NULL,
                title TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS review_audit_log (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                decision TEXT NOT NULL,
                rationale TEXT NOT NULL,
                related_cluster_id TEXT NOT NULL,
                related_story_ids_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_review_audit_candidate
                ON review_audit_log(candidate_id);

            CREATE TABLE IF NOT EXISTS issue_story_links (
                issue_id TEXT NOT NULL,
                cluster_id TEXT NOT NULL,
                story_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (issue_id, story_id)
            );
            CREATE INDEX IF NOT EXISTS idx_issue_story_links_issue
                ON issue_story_links(issue_id);
            """
        )
        self.connection.commit()

    def healthcheck(self) -> bool:
        try:
            row = self.connection.execute("SELECT 1 AS ok").fetchone()
            return bool(row and row["ok"] == 1)
        except sqlite3.DatabaseError:
            return False


@dataclass
class SqliteStoryRepository:
    db: SqliteDatabase

    def save_story(self, record: StoryRecord) -> StoryRecord:
        self.db.connection.execute(
            """
            INSERT INTO stories (
                story_id, schema_version, narrative_original_text, submitter_external_user_id,
                narrative_language, narrative_title_hint, narrative_canonical_type, narrative_canonical_labels_json,
                submitter_identity_issuer, lifecycle_status, created_at, updated_at,
                origin_source, origin_conversation_id, origin_tool_call_id,
                privacy_contains_pii, privacy_redaction_requested
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(story_id) DO UPDATE SET
                schema_version = excluded.schema_version,
                narrative_original_text = excluded.narrative_original_text,
                submitter_external_user_id = excluded.submitter_external_user_id,
                narrative_language = excluded.narrative_language,
                narrative_title_hint = excluded.narrative_title_hint,
                narrative_canonical_type = excluded.narrative_canonical_type,
                narrative_canonical_labels_json = excluded.narrative_canonical_labels_json,
                submitter_identity_issuer = excluded.submitter_identity_issuer,
                lifecycle_status = excluded.lifecycle_status,
                updated_at = excluded.updated_at,
                origin_source = excluded.origin_source,
                origin_conversation_id = excluded.origin_conversation_id,
                origin_tool_call_id = excluded.origin_tool_call_id,
                privacy_contains_pii = excluded.privacy_contains_pii,
                privacy_redaction_requested = excluded.privacy_redaction_requested
            """,
            (
                record.story_id,
                record.schema_version,
                record.narrative_original_text,
                record.submitter_external_user_id,
                record.narrative_language,
                record.narrative_title_hint,
                record.narrative_canonical_type,
                json.dumps(list(record.narrative_canonical_labels)),
                record.submitter_identity_issuer,
                record.lifecycle_status.value,
                record.created_at.isoformat(),
                record.updated_at.isoformat(),
                record.origin_source,
                record.origin_conversation_id,
                record.origin_tool_call_id,
                int(record.privacy_contains_pii),
                int(record.privacy_redaction_requested),
            ),
        )
        self.db.connection.commit()
        return record

    def get_story(self, story_id: str) -> StoryRecord | None:
        row = self.db.connection.execute(
            """
            SELECT story_id, schema_version, narrative_original_text, submitter_external_user_id,
                   narrative_language, narrative_title_hint, narrative_canonical_type, narrative_canonical_labels_json,
                   submitter_identity_issuer, lifecycle_status, created_at, updated_at,
                   origin_source, origin_conversation_id, origin_tool_call_id,
                   privacy_contains_pii, privacy_redaction_requested
            FROM stories
            WHERE story_id = ?
            """,
            (story_id,),
        ).fetchone()
        if row is None:
            return None
        return StoryRecord(
            story_id=str(row["story_id"]),
            schema_version=str(row["schema_version"]),
            narrative_original_text=str(row["narrative_original_text"]),
            submitter_external_user_id=str(row["submitter_external_user_id"]),
            narrative_language=row["narrative_language"],
            narrative_title_hint=row["narrative_title_hint"],
            narrative_canonical_type=row["narrative_canonical_type"],
            narrative_canonical_labels=tuple(json.loads(str(row["narrative_canonical_labels_json"]))),
            submitter_identity_issuer=row["submitter_identity_issuer"],
            lifecycle_status=StoryLifecycleStatus(str(row["lifecycle_status"])),
            created_at=_parse_dt(str(row["created_at"])),
            updated_at=_parse_dt(str(row["updated_at"])),
            origin_source=row["origin_source"],
            origin_conversation_id=row["origin_conversation_id"],
            origin_tool_call_id=row["origin_tool_call_id"],
            privacy_contains_pii=bool(row["privacy_contains_pii"]),
            privacy_redaction_requested=bool(row["privacy_redaction_requested"]),
        )

    def list_stories(self) -> list[StoryRecord]:
        rows = self.db.connection.execute(
            """
            SELECT story_id, schema_version, narrative_original_text, submitter_external_user_id,
                   narrative_language, narrative_title_hint, narrative_canonical_type, narrative_canonical_labels_json,
                   submitter_identity_issuer, lifecycle_status, created_at, updated_at,
                   origin_source, origin_conversation_id, origin_tool_call_id,
                   privacy_contains_pii, privacy_redaction_requested
            FROM stories
            ORDER BY created_at ASC
            """
        ).fetchall()
        result: list[StoryRecord] = []
        for row in rows:
            result.append(
                StoryRecord(
                    story_id=str(row["story_id"]),
                    schema_version=str(row["schema_version"]),
                    narrative_original_text=str(row["narrative_original_text"]),
                    submitter_external_user_id=str(row["submitter_external_user_id"]),
                    narrative_language=row["narrative_language"],
                    narrative_title_hint=row["narrative_title_hint"],
                    narrative_canonical_type=row["narrative_canonical_type"],
                    narrative_canonical_labels=tuple(
                        json.loads(str(row["narrative_canonical_labels_json"]))
                    ),
                    submitter_identity_issuer=row["submitter_identity_issuer"],
                    lifecycle_status=StoryLifecycleStatus(str(row["lifecycle_status"])),
                    created_at=_parse_dt(str(row["created_at"])),
                    updated_at=_parse_dt(str(row["updated_at"])),
                    origin_source=row["origin_source"],
                    origin_conversation_id=row["origin_conversation_id"],
                    origin_tool_call_id=row["origin_tool_call_id"],
                    privacy_contains_pii=bool(row["privacy_contains_pii"]),
                    privacy_redaction_requested=bool(row["privacy_redaction_requested"]),
                )
            )
        return result


@dataclass
class SqliteIdempotencyRepository:
    db: SqliteDatabase

    def get_by_key(self, key: str) -> IdempotencyRecord | None:
        row = self.db.connection.execute(
            """
            SELECT key, story_id, created_at
            FROM idempotency_keys
            WHERE key = ?
            """,
            (key,),
        ).fetchone()
        if row is None:
            return None
        return IdempotencyRecord(
            key=str(row["key"]),
            story_id=str(row["story_id"]),
            created_at=_parse_dt(str(row["created_at"])),
        )

    def save(self, record: IdempotencyRecord) -> IdempotencyRecord:
        self.db.connection.execute(
            """
            INSERT INTO idempotency_keys (key, story_id, created_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                story_id = excluded.story_id,
                created_at = excluded.created_at
            """,
            (record.key, record.story_id, record.created_at.isoformat()),
        )
        self.db.connection.commit()
        return record


@dataclass
class SqliteStoryEmbeddingStore:
    db: SqliteDatabase

    def save_story_embedding(
        self,
        *,
        story_id: str,
        model_name: str,
        embedding_vector: tuple[float, ...],
        source_checksum: str,
        embedding_policy_version: str,
    ) -> None:
        self.db.connection.execute(
            """
            INSERT INTO story_embeddings (
                story_id, model_name, embedding_vector_json, source_checksum, embedding_policy_version, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                story_id,
                model_name,
                json.dumps(list(embedding_vector)),
                source_checksum,
                embedding_policy_version,
                _utcnow().isoformat(),
            ),
        )
        self.db.connection.commit()


@dataclass
class SqliteIssueProjectionStore:
    db: SqliteDatabase

    def save_projection(
        self,
        *,
        issue_id: str,
        status: str,
        payload: dict[str, object],
        policy_version: str,
    ) -> None:
        now = _utcnow().isoformat()
        self.db.connection.execute(
            """
            INSERT INTO spa_issue_projections (issue_id, status, payload_json, policy_version, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(issue_id) DO UPDATE SET
                status = excluded.status,
                payload_json = excluded.payload_json,
                policy_version = excluded.policy_version,
                updated_at = excluded.updated_at
            """,
            (issue_id, status, json.dumps(payload), policy_version, now, now),
        )
        self.db.connection.commit()


@dataclass
class SqliteIssueProjectionEmbeddingStore:
    db: SqliteDatabase

    def save_projection_embedding(
        self,
        *,
        issue_id: str,
        model_name: str,
        embedding_vector: tuple[float, ...],
        source_checksum: str,
        embedding_policy_version: str,
    ) -> None:
        self.db.connection.execute(
            """
            INSERT INTO spa_issue_projection_embeddings (
                issue_id, model_name, embedding_vector_json, source_checksum, embedding_policy_version, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                issue_id,
                model_name,
                json.dumps(list(embedding_vector)),
                source_checksum,
                embedding_policy_version,
                _utcnow().isoformat(),
            ),
        )
        self.db.connection.commit()


@dataclass
class SqliteIssueCandidateStore:
    db: SqliteDatabase

    def save(self, record: IssueCandidateRecord) -> IssueCandidateRecord:
        self.db.connection.execute(
            """
            INSERT INTO issue_candidates (
                candidate_id, status, cluster_id, story_ids_json, readiness_score, title, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(candidate_id) DO UPDATE SET
                status = excluded.status,
                cluster_id = excluded.cluster_id,
                story_ids_json = excluded.story_ids_json,
                readiness_score = excluded.readiness_score,
                title = excluded.title,
                updated_at = excluded.updated_at
            """,
            (
                record.candidate_id,
                record.status.value,
                record.cluster_id,
                json.dumps(list(record.story_ids)),
                record.readiness_score,
                record.title,
                _utcnow().isoformat(),
            ),
        )
        self.db.connection.commit()
        return record

    def get(self, candidate_id: str) -> IssueCandidateRecord | None:
        row = self.db.connection.execute(
            """
            SELECT candidate_id, status, cluster_id, story_ids_json, readiness_score, title
            FROM issue_candidates
            WHERE candidate_id = ?
            """,
            (candidate_id,),
        ).fetchone()
        if row is None:
            return None
        return IssueCandidateRecord(
            candidate_id=str(row["candidate_id"]),
            status=IssueCandidateStatus(str(row["status"])),
            cluster_id=str(row["cluster_id"]),
            story_ids=tuple(json.loads(str(row["story_ids_json"]))),
            readiness_score=int(row["readiness_score"]),
            title=str(row["title"]),
        )

    def delete(self, candidate_id: str) -> None:
        self.db.connection.execute(
            "DELETE FROM issue_candidates WHERE candidate_id = ?",
            (candidate_id,),
        )
        self.db.connection.commit()


@dataclass
class SqliteReviewAuditLogRepository:
    db: SqliteDatabase

    def append(self, entry: ReviewAuditEntry) -> ReviewAuditEntry:
        self.db.connection.execute(
            """
            INSERT INTO review_audit_log (
                candidate_id, actor, decision, rationale, related_cluster_id, related_story_ids_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.candidate_id,
                entry.actor,
                entry.decision.value,
                entry.rationale,
                entry.related_cluster_id,
                json.dumps(list(entry.related_story_ids)),
                _utcnow().isoformat(),
            ),
        )
        self.db.connection.commit()
        return entry

    def list_for_candidate(self, candidate_id: str) -> tuple[ReviewAuditEntry, ...]:
        rows = self.db.connection.execute(
            """
            SELECT candidate_id, actor, decision, rationale, related_cluster_id, related_story_ids_json
            FROM review_audit_log
            WHERE candidate_id = ?
            ORDER BY audit_id ASC
            """,
            (candidate_id,),
        ).fetchall()
        return tuple(
            ReviewAuditEntry(
                candidate_id=str(row["candidate_id"]),
                actor=str(row["actor"]),
                decision=ReviewDecision(str(row["decision"])),
                rationale=str(row["rationale"]),
                related_cluster_id=str(row["related_cluster_id"]),
                related_story_ids=tuple(json.loads(str(row["related_story_ids_json"]))),
            )
            for row in rows
        )


@dataclass
class SqliteIssueStoryLinkStore:
    db: SqliteDatabase

    def save_issue_story_links(
        self,
        *,
        issue_id: str,
        cluster_id: str,
        story_ids: tuple[str, ...],
    ) -> None:
        now = _utcnow().isoformat()
        self.db.connection.execute(
            "DELETE FROM issue_story_links WHERE issue_id = ?",
            (issue_id,),
        )
        for story_id in story_ids:
            self.db.connection.execute(
                """
                INSERT INTO issue_story_links (issue_id, cluster_id, story_id, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(issue_id, story_id) DO UPDATE SET
                    cluster_id = excluded.cluster_id,
                    created_at = excluded.created_at
                """,
                (issue_id, cluster_id, story_id, now),
            )
        self.db.connection.commit()
