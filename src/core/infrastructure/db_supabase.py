from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from core.domain import IdempotencyRecord, StoryLifecycleStatus, StoryRecord
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus, ReviewAuditEntry, ReviewDecision

try:
    import psycopg  # pyright: ignore[reportMissingImports]
    from psycopg.rows import dict_row  # pyright: ignore[reportMissingImports]
except Exception:  # pragma: no cover - optional dependency in local envs
    psycopg = None
    dict_row = None


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


@dataclass
class SupabaseDatabase:
    dsn: str

    @classmethod
    def from_url(cls, database_url: str) -> SupabaseDatabase:
        if not (
            database_url.startswith("postgresql://")
            or database_url.startswith("postgres://")
        ):
            raise ValueError(
                f"Unsupported database URL for supabase backend: {database_url!r}."
            )
        return cls(dsn=database_url)

    def _connect(self) -> Any:
        if psycopg is None or dict_row is None:
            raise RuntimeError(
                "Supabase backend requires psycopg. Install dependency: psycopg[binary]."
            )
        return psycopg.connect(self.dsn, row_factory=dict_row)

    def healthcheck(self) -> bool:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute("SELECT 1 AS ok")
                row = cur.fetchone()
                return bool(row and row["ok"] == 1)
        except Exception:
            return False

    def required_tables_ready(self) -> bool:
        required = {
            "stories",
            "idempotency_keys",
            "story_embeddings",
            "spa_issue_projections",
            "spa_issue_projection_embeddings",
            "issue_candidates",
            "review_audit_log",
            "issue_story_links",
        }
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    """
                )
                existing = {str(row["table_name"]) for row in cur.fetchall()}
                return required.issubset(existing)
        except Exception:
            return False

    def required_columns_ready(self) -> bool:
        required: dict[str, set[str]] = {
            "stories": {
                "story_id",
                "narrative_language",
                "narrative_title_hint",
                "narrative_canonical_type",
                "narrative_canonical_labels_json",
            },
            "story_embeddings": {
                "embedding_vector_json",
                "embedding_policy_version",
            },
            "spa_issue_projection_embeddings": {
                "embedding_vector_json",
                "embedding_policy_version",
            },
        }
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT table_name, column_name
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    """
                )
                columns_by_table: dict[str, set[str]] = {}
                for row in cur.fetchall():
                    table_name = str(row["table_name"])
                    column_name = str(row["column_name"])
                    columns_by_table.setdefault(table_name, set()).add(column_name)
                for table_name, columns in required.items():
                    if not columns.issubset(columns_by_table.get(table_name, set())):
                        return False
                return True
        except Exception:
            return False

    def service_role_policy_probe(self) -> bool:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS rows_count FROM stories")
                row = cur.fetchone()
                return bool(row and row["rows_count"] >= 0)
        except Exception:
            return False


@dataclass
class SupabaseStoryRepository:
    db: SupabaseDatabase

    def save_story(self, record: StoryRecord) -> StoryRecord:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO stories (
                    story_id, schema_version, narrative_original_text, submitter_external_user_id,
                    narrative_language, narrative_title_hint, narrative_canonical_type, narrative_canonical_labels_json,
                    submitter_identity_issuer, lifecycle_status, created_at, updated_at,
                    origin_source, origin_conversation_id, origin_tool_call_id,
                    privacy_contains_pii, privacy_redaction_requested
                ) VALUES (
                    %(story_id)s, %(schema_version)s, %(narrative_original_text)s, %(submitter_external_user_id)s,
                    %(narrative_language)s, %(narrative_title_hint)s, %(narrative_canonical_type)s, %(narrative_canonical_labels_json)s,
                    %(submitter_identity_issuer)s, %(lifecycle_status)s, %(created_at)s, %(updated_at)s,
                    %(origin_source)s, %(origin_conversation_id)s, %(origin_tool_call_id)s,
                    %(privacy_contains_pii)s, %(privacy_redaction_requested)s
                )
                ON CONFLICT(story_id) DO UPDATE SET
                    schema_version = EXCLUDED.schema_version,
                    narrative_original_text = EXCLUDED.narrative_original_text,
                    submitter_external_user_id = EXCLUDED.submitter_external_user_id,
                    narrative_language = EXCLUDED.narrative_language,
                    narrative_title_hint = EXCLUDED.narrative_title_hint,
                    narrative_canonical_type = EXCLUDED.narrative_canonical_type,
                    narrative_canonical_labels_json = EXCLUDED.narrative_canonical_labels_json,
                    submitter_identity_issuer = EXCLUDED.submitter_identity_issuer,
                    lifecycle_status = EXCLUDED.lifecycle_status,
                    updated_at = EXCLUDED.updated_at,
                    origin_source = EXCLUDED.origin_source,
                    origin_conversation_id = EXCLUDED.origin_conversation_id,
                    origin_tool_call_id = EXCLUDED.origin_tool_call_id,
                    privacy_contains_pii = EXCLUDED.privacy_contains_pii,
                    privacy_redaction_requested = EXCLUDED.privacy_redaction_requested
                """,
                {
                    "story_id": record.story_id,
                    "schema_version": record.schema_version,
                    "narrative_original_text": record.narrative_original_text,
                    "submitter_external_user_id": record.submitter_external_user_id,
                    "narrative_language": record.narrative_language,
                    "narrative_title_hint": record.narrative_title_hint,
                    "narrative_canonical_type": record.narrative_canonical_type,
                    "narrative_canonical_labels_json": json.dumps(
                        list(record.narrative_canonical_labels)
                    ),
                    "submitter_identity_issuer": record.submitter_identity_issuer,
                    "lifecycle_status": record.lifecycle_status.value,
                    "created_at": record.created_at.isoformat(),
                    "updated_at": record.updated_at.isoformat(),
                    "origin_source": record.origin_source,
                    "origin_conversation_id": record.origin_conversation_id,
                    "origin_tool_call_id": record.origin_tool_call_id,
                    "privacy_contains_pii": record.privacy_contains_pii,
                    "privacy_redaction_requested": record.privacy_redaction_requested,
                },
            )
            conn.commit()
        return record

    def get_story(self, story_id: str) -> StoryRecord | None:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT story_id, schema_version, narrative_original_text, submitter_external_user_id,
                       narrative_language, narrative_title_hint, narrative_canonical_type, narrative_canonical_labels_json,
                       submitter_identity_issuer, lifecycle_status, created_at, updated_at,
                       origin_source, origin_conversation_id, origin_tool_call_id,
                       privacy_contains_pii, privacy_redaction_requested
                FROM stories
                WHERE story_id = %(story_id)s
                """,
                {"story_id": story_id},
            )
            row = cur.fetchone()
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

    def list_stories(self) -> list[StoryRecord]:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT story_id, schema_version, narrative_original_text, submitter_external_user_id,
                       narrative_language, narrative_title_hint, narrative_canonical_type, narrative_canonical_labels_json,
                       submitter_identity_issuer, lifecycle_status, created_at, updated_at,
                       origin_source, origin_conversation_id, origin_tool_call_id,
                       privacy_contains_pii, privacy_redaction_requested
                FROM stories
                ORDER BY created_at ASC
                """
            )
            rows = cur.fetchall()
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
class SupabaseIdempotencyRepository:
    db: SupabaseDatabase

    def get_by_key(self, key: str) -> IdempotencyRecord | None:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT key, story_id, created_at
                FROM idempotency_keys
                WHERE key = %(key)s
                """,
                {"key": key},
            )
            row = cur.fetchone()
        if row is None:
            return None
        return IdempotencyRecord(
            key=str(row["key"]),
            story_id=str(row["story_id"]),
            created_at=_parse_dt(str(row["created_at"])),
        )

    def save(self, record: IdempotencyRecord) -> IdempotencyRecord:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO idempotency_keys (key, story_id, created_at)
                VALUES (%(key)s, %(story_id)s, %(created_at)s)
                ON CONFLICT(key) DO UPDATE SET
                    story_id = EXCLUDED.story_id,
                    created_at = EXCLUDED.created_at
                """,
                {
                    "key": record.key,
                    "story_id": record.story_id,
                    "created_at": record.created_at.isoformat(),
                },
            )
            conn.commit()
        return record


@dataclass
class SupabaseStoryEmbeddingStore:
    db: SupabaseDatabase

    def save_story_embedding(
        self,
        *,
        story_id: str,
        model_name: str,
        embedding_vector: tuple[float, ...],
        source_checksum: str,
        embedding_policy_version: str,
    ) -> None:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO story_embeddings (
                    story_id, model_name, embedding_vector_json, source_checksum, embedding_policy_version, created_at
                ) VALUES (%(story_id)s, %(model_name)s, %(embedding_vector_json)s, %(source_checksum)s, %(embedding_policy_version)s, %(created_at)s)
                """,
                {
                    "story_id": story_id,
                    "model_name": model_name,
                    "embedding_vector_json": json.dumps(list(embedding_vector)),
                    "source_checksum": source_checksum,
                    "embedding_policy_version": embedding_policy_version,
                    "created_at": _utcnow().isoformat(),
                },
            )
            conn.commit()


@dataclass
class SupabaseIssueProjectionStore:
    db: SupabaseDatabase

    def save_projection(
        self,
        *,
        issue_id: str,
        status: str,
        payload: dict[str, object],
        policy_version: str,
    ) -> None:
        now = _utcnow().isoformat()
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO spa_issue_projections (
                    issue_id, status, payload_json, policy_version, created_at, updated_at
                ) VALUES (
                    %(issue_id)s, %(status)s, %(payload_json)s, %(policy_version)s, %(created_at)s, %(updated_at)s
                )
                ON CONFLICT(issue_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    payload_json = EXCLUDED.payload_json,
                    policy_version = EXCLUDED.policy_version,
                    updated_at = EXCLUDED.updated_at
                """,
                {
                    "issue_id": issue_id,
                    "status": status,
                    "payload_json": json.dumps(payload),
                    "policy_version": policy_version,
                    "created_at": now,
                    "updated_at": now,
                },
            )
            conn.commit()


@dataclass
class SupabaseIssueProjectionEmbeddingStore:
    db: SupabaseDatabase

    def save_projection_embedding(
        self,
        *,
        issue_id: str,
        model_name: str,
        embedding_vector: tuple[float, ...],
        source_checksum: str,
        embedding_policy_version: str,
    ) -> None:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO spa_issue_projection_embeddings (
                    issue_id, model_name, embedding_vector_json, source_checksum, embedding_policy_version, created_at
                ) VALUES (
                    %(issue_id)s, %(model_name)s, %(embedding_vector_json)s, %(source_checksum)s, %(embedding_policy_version)s, %(created_at)s
                )
                """,
                {
                    "issue_id": issue_id,
                    "model_name": model_name,
                    "embedding_vector_json": json.dumps(list(embedding_vector)),
                    "source_checksum": source_checksum,
                    "embedding_policy_version": embedding_policy_version,
                    "created_at": _utcnow().isoformat(),
                },
            )
            conn.commit()


@dataclass
class SupabaseIssueCandidateStore:
    db: SupabaseDatabase

    def save(self, record: IssueCandidateRecord) -> IssueCandidateRecord:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO issue_candidates (
                    candidate_id, status, cluster_id, story_ids_json, readiness_score, title, updated_at
                ) VALUES (
                    %(candidate_id)s, %(status)s, %(cluster_id)s, %(story_ids_json)s, %(readiness_score)s, %(title)s, %(updated_at)s
                )
                ON CONFLICT(candidate_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    cluster_id = EXCLUDED.cluster_id,
                    story_ids_json = EXCLUDED.story_ids_json,
                    readiness_score = EXCLUDED.readiness_score,
                    title = EXCLUDED.title,
                    updated_at = EXCLUDED.updated_at
                """,
                {
                    "candidate_id": record.candidate_id,
                    "status": record.status.value,
                    "cluster_id": record.cluster_id,
                    "story_ids_json": json.dumps(list(record.story_ids)),
                    "readiness_score": record.readiness_score,
                    "title": record.title,
                    "updated_at": _utcnow().isoformat(),
                },
            )
            conn.commit()
        return record

    def get(self, candidate_id: str) -> IssueCandidateRecord | None:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT candidate_id, status, cluster_id, story_ids_json, readiness_score, title
                FROM issue_candidates
                WHERE candidate_id = %(candidate_id)s
                """,
                {"candidate_id": candidate_id},
            )
            row = cur.fetchone()
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
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM issue_candidates WHERE candidate_id = %(candidate_id)s",
                {"candidate_id": candidate_id},
            )
            conn.commit()


@dataclass
class SupabaseReviewAuditLogRepository:
    db: SupabaseDatabase

    def append(self, entry: ReviewAuditEntry) -> ReviewAuditEntry:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO review_audit_log (
                    candidate_id, actor, decision, rationale, related_cluster_id, related_story_ids_json, created_at
                ) VALUES (
                    %(candidate_id)s, %(actor)s, %(decision)s, %(rationale)s, %(related_cluster_id)s, %(related_story_ids_json)s, %(created_at)s
                )
                """,
                {
                    "candidate_id": entry.candidate_id,
                    "actor": entry.actor,
                    "decision": entry.decision.value,
                    "rationale": entry.rationale,
                    "related_cluster_id": entry.related_cluster_id,
                    "related_story_ids_json": json.dumps(list(entry.related_story_ids)),
                    "created_at": _utcnow().isoformat(),
                },
            )
            conn.commit()
        return entry

    def list_for_candidate(self, candidate_id: str) -> tuple[ReviewAuditEntry, ...]:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT candidate_id, actor, decision, rationale, related_cluster_id, related_story_ids_json
                FROM review_audit_log
                WHERE candidate_id = %(candidate_id)s
                ORDER BY audit_id ASC
                """,
                {"candidate_id": candidate_id},
            )
            rows = cur.fetchall()
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
class SupabaseIssueStoryLinkStore:
    db: SupabaseDatabase

    def save_issue_story_links(
        self,
        *,
        issue_id: str,
        cluster_id: str,
        story_ids: tuple[str, ...],
    ) -> None:
        with self.db._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM issue_story_links WHERE issue_id = %(issue_id)s",
                {"issue_id": issue_id},
            )
            now = _utcnow().isoformat()
            for story_id in story_ids:
                cur.execute(
                    """
                    INSERT INTO issue_story_links (issue_id, cluster_id, story_id, created_at)
                    VALUES (%(issue_id)s, %(cluster_id)s, %(story_id)s, %(created_at)s)
                    ON CONFLICT(issue_id, story_id) DO UPDATE SET
                        cluster_id = EXCLUDED.cluster_id,
                        created_at = EXCLUDED.created_at
                    """,
                    {
                        "issue_id": issue_id,
                        "cluster_id": cluster_id,
                        "story_id": story_id,
                        "created_at": now,
                    },
                )
            conn.commit()
