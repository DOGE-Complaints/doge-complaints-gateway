from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Mapping

from core.domain import IdempotencyRecord, StoryGeoSnapshot, StoryLifecycleStatus, StoryRecord
from core.domain.narrative_i18n import I18N_LANGS, i18n_dict_from_json, i18n_dict_to_json
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus, ReviewAuditEntry, ReviewDecision

logger = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _geo_bind(record: StoryRecord) -> tuple:
    if record.geo is None:
        return (None, None, None, None, None, "[]", None, None, None, None)
    geo = record.geo
    return (
        geo.normalized_label,
        geo.latitude,
        geo.longitude,
        geo.confidence,
        geo.provider,
        json.dumps(list(geo.cluster_tags)),
        geo.admin_district,
        geo.admin_settlement,
        geo.admin_region,
        geo.admin_country,
    )


def _i18n_dict_from_sqlite_row(
    row: sqlite3.Row,
    keys: set[str],
    *,
    json_column: str,
    legacy_hint_column: str = "narrative_title_hint",
    legacy_lang_columns: tuple[tuple[str, str], ...] = (
        ("et", "narrative_title_hint_et"),
        ("ru", "narrative_title_hint_ru"),
        ("en", "narrative_title_hint_en"),
    ),
) -> dict[str, str] | None:
    if json_column in keys and row[json_column]:
        return i18n_dict_from_json(str(row[json_column]))
    legacy_values = {
        lang: str(row[col]).strip()
        for lang, col in legacy_lang_columns
        if col in keys and row[col]
    }
    if legacy_values:
        return {lang: legacy_values.get(lang, "") for lang in I18N_LANGS}
    if legacy_hint_column in keys and row[legacy_hint_column]:
        lang = str(row["narrative_language"] or "en")
        base = {code: "" for code in I18N_LANGS}
        if lang in base:
            base[lang] = str(row[legacy_hint_column]).strip()
        return base
    return None


def _summary_dict_from_sqlite_row(row: sqlite3.Row, keys: set[str]) -> dict[str, str] | None:
    if "narrative_summary_json" not in keys or not row["narrative_summary_json"]:
        return None
    parsed = json.loads(str(row["narrative_summary_json"]))
    if isinstance(parsed, dict):
        return {str(key): str(value) for key, value in parsed.items()}
    return None


def _institution_dict_from_sqlite_row(row: sqlite3.Row, keys: set[str]) -> dict[str, str] | None:
    if "institution_json" not in keys or not row["institution_json"]:
        return None
    return i18n_dict_from_json(str(row["institution_json"]))


_STORY_SELECT_COLUMNS = """
    story_id, schema_version, narrative_original_text, submitter_external_user_id,
    narrative_language, narrative_title_json, narrative_description_json, narrative_session_language,
    narrative_title_hint, narrative_title_hint_et, narrative_title_hint_ru, narrative_title_hint_en,
    narrative_summary_json, institution_json, narrative_consistency_notes,
    narrative_canonical_type, narrative_canonical_labels_json,
    submitter_identity_issuer, lifecycle_status, created_at, updated_at,
    origin_source, origin_conversation_id, origin_tool_call_id,
    privacy_contains_pii, privacy_redaction_requested,
    geo_normalized_label, geo_latitude, geo_longitude, geo_confidence, geo_provider, geo_cluster_tags_json,
    geo_admin_district, geo_admin_settlement, geo_admin_region, geo_admin_country
"""


def _story_record_from_sqlite_row(row: sqlite3.Row) -> StoryRecord:
    keys = set(row.keys())
    geo: StoryGeoSnapshot | None = None
    if "geo_normalized_label" in keys and row["geo_normalized_label"] is not None:
        geo = StoryGeoSnapshot(
            normalized_label=str(row["geo_normalized_label"]),
            latitude=float(row["geo_latitude"]),
            longitude=float(row["geo_longitude"]),
            confidence=float(row["geo_confidence"]),
            provider=str(row["geo_provider"]),
            cluster_tags=tuple(json.loads(str(row["geo_cluster_tags_json"] or "[]"))),
            admin_district=(
                str(row["geo_admin_district"])
                if "geo_admin_district" in keys and row["geo_admin_district"]
                else None
            ),
            admin_settlement=(
                str(row["geo_admin_settlement"])
                if "geo_admin_settlement" in keys and row["geo_admin_settlement"]
                else None
            ),
            admin_region=(
                str(row["geo_admin_region"])
                if "geo_admin_region" in keys and row["geo_admin_region"]
                else None
            ),
            admin_country=(
                str(row["geo_admin_country"])
                if "geo_admin_country" in keys and row["geo_admin_country"]
                else None
            ),
        )
    session_language = (
        str(row["narrative_session_language"]).strip()
        if "narrative_session_language" in keys and row["narrative_session_language"]
        else None
    )
    return StoryRecord(
        story_id=str(row["story_id"]),
        schema_version=str(row["schema_version"]),
        narrative_original_text=str(row["narrative_original_text"]),
        submitter_external_user_id=str(row["submitter_external_user_id"]),
        narrative_language=row["narrative_language"],
        narrative_title=_i18n_dict_from_sqlite_row(
            row, keys, json_column="narrative_title_json"
        ),
        narrative_description=_i18n_dict_from_sqlite_row(
            row,
            keys,
            json_column="narrative_description_json",
            legacy_hint_column="__none__",
            legacy_lang_columns=(),
        ),
        narrative_summary=_summary_dict_from_sqlite_row(row, keys),
        narrative_institution=_institution_dict_from_sqlite_row(row, keys),
        narrative_session_language=session_language,
        narrative_consistency_notes=(
            row["narrative_consistency_notes"] if "narrative_consistency_notes" in keys else None
        ),
        narrative_canonical_type=row["narrative_canonical_type"],
        narrative_canonical_labels=tuple(json.loads(str(row["narrative_canonical_labels_json"]))),
        submitter_identity_issuer=str(row["submitter_identity_issuer"] or ""),
        lifecycle_status=StoryLifecycleStatus(str(row["lifecycle_status"])),
        created_at=_parse_dt(str(row["created_at"])),
        updated_at=_parse_dt(str(row["updated_at"])),
        origin_source=row["origin_source"],
        origin_conversation_id=row["origin_conversation_id"],
        origin_tool_call_id=row["origin_tool_call_id"],
        privacy_contains_pii=bool(row["privacy_contains_pii"]),
        privacy_redaction_requested=bool(row["privacy_redaction_requested"]),
        geo=geo,
    )


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
                submitter_identity_issuer TEXT NOT NULL,
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

            CREATE TABLE IF NOT EXISTS doge_issues (
                issue_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                policy_version TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS doge_issue_embeddings (
                embedding_id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_id TEXT NOT NULL,
                model_name TEXT NOT NULL,
                embedding_vector_json TEXT NOT NULL,
                source_checksum TEXT NOT NULL,
                embedding_policy_version TEXT NOT NULL DEFAULT 'm3.doge_issue_embedding_policy.v1',
                created_at TEXT NOT NULL,
                FOREIGN KEY(issue_id) REFERENCES doge_issues(issue_id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_issue_embeddings_issue_id
                ON doge_issue_embeddings(issue_id);

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
        self._ensure_sqlite_schema_migrations()

    def _ensure_sqlite_schema_migrations(self) -> None:
        cur = self.connection.execute("PRAGMA table_info(stories)")
        cols = {row[1] for row in cur.fetchall()}
        for name, ddl in (
            ("geo_normalized_label", "ALTER TABLE stories ADD COLUMN geo_normalized_label TEXT"),
            ("geo_latitude", "ALTER TABLE stories ADD COLUMN geo_latitude REAL"),
            ("geo_longitude", "ALTER TABLE stories ADD COLUMN geo_longitude REAL"),
            ("geo_confidence", "ALTER TABLE stories ADD COLUMN geo_confidence REAL"),
            ("geo_provider", "ALTER TABLE stories ADD COLUMN geo_provider TEXT"),
            (
                "geo_cluster_tags_json",
                "ALTER TABLE stories ADD COLUMN geo_cluster_tags_json TEXT DEFAULT '[]'",
            ),
            ("geo_admin_district", "ALTER TABLE stories ADD COLUMN geo_admin_district TEXT"),
            ("geo_admin_settlement", "ALTER TABLE stories ADD COLUMN geo_admin_settlement TEXT"),
            ("geo_admin_region", "ALTER TABLE stories ADD COLUMN geo_admin_region TEXT"),
            ("geo_admin_country", "ALTER TABLE stories ADD COLUMN geo_admin_country TEXT"),
            ("narrative_title_hint_et", "ALTER TABLE stories ADD COLUMN narrative_title_hint_et TEXT"),
            ("narrative_title_hint_ru", "ALTER TABLE stories ADD COLUMN narrative_title_hint_ru TEXT"),
            ("narrative_title_hint_en", "ALTER TABLE stories ADD COLUMN narrative_title_hint_en TEXT"),
            ("narrative_summary_json", "ALTER TABLE stories ADD COLUMN narrative_summary_json TEXT"),
            (
                "narrative_consistency_notes",
                "ALTER TABLE stories ADD COLUMN narrative_consistency_notes TEXT",
            ),
            ("narrative_title_json", "ALTER TABLE stories ADD COLUMN narrative_title_json TEXT"),
            (
                "narrative_description_json",
                "ALTER TABLE stories ADD COLUMN narrative_description_json TEXT",
            ),
            (
                "narrative_session_language",
                "ALTER TABLE stories ADD COLUMN narrative_session_language TEXT",
            ),
            (
                "institution_json",
                "ALTER TABLE stories ADD COLUMN institution_json TEXT",
            ),
        ):
            if name not in cols:
                self.connection.execute(ddl)
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS story_signals (
                story_id TEXT NOT NULL,
                extraction_policy TEXT NOT NULL,
                signals_json TEXT NOT NULL,
                extracted_at TEXT NOT NULL,
                PRIMARY KEY (story_id, extraction_policy)
            );
            CREATE INDEX IF NOT EXISTS idx_story_signals_policy ON story_signals(extraction_policy);

            CREATE TABLE IF NOT EXISTS cluster_memberships (
                story_id TEXT NOT NULL,
                lens TEXT NOT NULL,
                cluster_id TEXT NOT NULL,
                computed_at TEXT NOT NULL,
                PRIMARY KEY (story_id, lens)
            );
            CREATE INDEX IF NOT EXISTS idx_cluster_memberships_cluster ON cluster_memberships(cluster_id);
            CREATE INDEX IF NOT EXISTS idx_cluster_memberships_lens ON cluster_memberships(lens);

            CREATE INDEX IF NOT EXISTS idx_issue_candidates_cluster_status
                ON issue_candidates(cluster_id, status);
            CREATE INDEX IF NOT EXISTS idx_issue_story_links_cluster ON issue_story_links(cluster_id);
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
        logger.info(
            "repo.sqlite.save_story_start story_id=%s",
            record.story_id,
            extra={
                "story_id": record.story_id,
                "backend": "sqlite",
                "repository_class": self.__class__.__name__,
                "stage": "repository.sqlite.save_story",
                "outcome": "start",
            },
        )
        geo = _geo_bind(record)
        cursor = self.db.connection.execute(
            """
            INSERT INTO stories (
                story_id, schema_version, narrative_original_text, submitter_external_user_id,
                narrative_language, narrative_title_json, narrative_description_json, narrative_session_language,
                narrative_title_hint, narrative_title_hint_et, narrative_title_hint_ru,
                narrative_title_hint_en, narrative_summary_json, institution_json,
                narrative_consistency_notes,
                narrative_canonical_type, narrative_canonical_labels_json,
                submitter_identity_issuer, lifecycle_status, created_at, updated_at,
                origin_source, origin_conversation_id, origin_tool_call_id,
                privacy_contains_pii, privacy_redaction_requested,
                geo_normalized_label, geo_latitude, geo_longitude, geo_confidence, geo_provider, geo_cluster_tags_json,
                geo_admin_district, geo_admin_settlement, geo_admin_region, geo_admin_country
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(story_id) DO UPDATE SET
                schema_version = excluded.schema_version,
                narrative_original_text = excluded.narrative_original_text,
                submitter_external_user_id = excluded.submitter_external_user_id,
                narrative_language = excluded.narrative_language,
                narrative_title_json = excluded.narrative_title_json,
                narrative_description_json = excluded.narrative_description_json,
                narrative_session_language = excluded.narrative_session_language,
                narrative_title_hint = excluded.narrative_title_hint,
                narrative_title_hint_et = excluded.narrative_title_hint_et,
                narrative_title_hint_ru = excluded.narrative_title_hint_ru,
                narrative_title_hint_en = excluded.narrative_title_hint_en,
                narrative_summary_json = excluded.narrative_summary_json,
                institution_json = excluded.institution_json,
                narrative_consistency_notes = excluded.narrative_consistency_notes,
                narrative_canonical_type = excluded.narrative_canonical_type,
                narrative_canonical_labels_json = excluded.narrative_canonical_labels_json,
                submitter_identity_issuer = excluded.submitter_identity_issuer,
                lifecycle_status = excluded.lifecycle_status,
                updated_at = excluded.updated_at,
                origin_source = excluded.origin_source,
                origin_conversation_id = excluded.origin_conversation_id,
                origin_tool_call_id = excluded.origin_tool_call_id,
                privacy_contains_pii = excluded.privacy_contains_pii,
                privacy_redaction_requested = excluded.privacy_redaction_requested,
                geo_normalized_label = excluded.geo_normalized_label,
                geo_latitude = excluded.geo_latitude,
                geo_longitude = excluded.geo_longitude,
                geo_confidence = excluded.geo_confidence,
                geo_provider = excluded.geo_provider,
                geo_cluster_tags_json = excluded.geo_cluster_tags_json,
                geo_admin_district = excluded.geo_admin_district,
                geo_admin_settlement = excluded.geo_admin_settlement,
                geo_admin_region = excluded.geo_admin_region,
                geo_admin_country = excluded.geo_admin_country
            """,
            (
                record.story_id,
                record.schema_version,
                record.narrative_original_text,
                record.submitter_external_user_id,
                record.narrative_language,
                i18n_dict_to_json(record.narrative_title),
                i18n_dict_to_json(record.narrative_description),
                record.narrative_session_language,
                None,
                None,
                None,
                None,
                i18n_dict_to_json(record.narrative_summary),
                i18n_dict_to_json(record.narrative_institution),
                record.narrative_consistency_notes,
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
                *geo,
            ),
        )
        self.db.connection.commit()
        logger.info(
            "repo.sqlite.save_story_done story_id=%s rows_affected=%s",
            record.story_id,
            cursor.rowcount,
            extra={
                "story_id": record.story_id,
                "rows_affected": cursor.rowcount,
                "backend": "sqlite",
                "repository_class": self.__class__.__name__,
                "stage": "repository.sqlite.save_story",
                "outcome": "success",
            },
        )
        return record

    def get_story(self, story_id: str) -> StoryRecord | None:
        row = self.db.connection.execute(
            f"""
            SELECT {_STORY_SELECT_COLUMNS}
            FROM stories
            WHERE story_id = ?
            """,
            (story_id,),
        ).fetchone()
        if row is None:
            return None
        return _story_record_from_sqlite_row(row)

    def list_stories(self) -> list[StoryRecord]:
        rows = self.db.connection.execute(
            f"""
            SELECT {_STORY_SELECT_COLUMNS}
            FROM stories
            ORDER BY created_at ASC
            """
        ).fetchall()
        return [_story_record_from_sqlite_row(row) for row in rows]

    def list_stories_ready_for_clustering(self) -> list[StoryRecord]:
        rows = self.db.connection.execute(
            f"""
            SELECT {_STORY_SELECT_COLUMNS}
            FROM stories
            WHERE lifecycle_status = ?
            ORDER BY created_at ASC
            """,
            (StoryLifecycleStatus.READY_FOR_PROFILE.value,),
        ).fetchall()
        return [_story_record_from_sqlite_row(row) for row in rows]

    def update_lifecycle_status(self, story_id: str, status: StoryLifecycleStatus) -> None:
        self.db.connection.execute(
            "UPDATE stories SET lifecycle_status = ?, updated_at = ? WHERE story_id = ?",
            (status.value, _utcnow().isoformat(), story_id),
        )
        self.db.connection.commit()


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
            INSERT INTO doge_issues (issue_id, status, payload_json, policy_version, created_at, updated_at)
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
        from core.projection.read_filters import filter_projection_rows, parse_payload_json

        query = (
            "SELECT status, payload_json, created_at FROM doge_issues WHERE 1=1"
        )
        params: list[object] = []
        if status:
            placeholders = ",".join("?" for _ in status)
            query += f" AND status IN ({placeholders})"
            params.extend(status)
        if created_after:
            query += " AND created_at >= ?"
            params.append(created_after)
        if created_before:
            query += " AND created_at <= ?"
            params.append(created_before)
        query += " ORDER BY created_at DESC"
        cursor = self.db.connection.execute(query, tuple(params))
        rows: list[tuple[str, dict[str, object], str]] = []
        for row_status, payload_json, created_at in cursor.fetchall():
            rows.append(
                (str(row_status), parse_payload_json(payload_json), str(created_at))
            )
        return filter_projection_rows(
            rows,
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
        from core.projection.read_filters import parse_payload_json

        cursor = self.db.connection.execute(
            "SELECT payload_json FROM doge_issues WHERE issue_id = ?",
            (issue_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return parse_payload_json(row[0])


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
        now = _utcnow().isoformat()
        cursor = self.db.connection.execute(
            """
            UPDATE doge_issue_embeddings
            SET
                model_name = ?,
                embedding_vector_json = ?,
                source_checksum = ?,
                embedding_policy_version = ?,
                created_at = ?
            WHERE issue_id = ?
            """,
            (
                model_name,
                json.dumps(list(embedding_vector)),
                source_checksum,
                embedding_policy_version,
                now,
                issue_id,
            ),
        )
        if cursor.rowcount == 0:
            self.db.connection.execute(
                """
                INSERT INTO doge_issue_embeddings (
                    issue_id, model_name, embedding_vector_json, source_checksum, embedding_policy_version, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    issue_id,
                    model_name,
                    json.dumps(list(embedding_vector)),
                    source_checksum,
                    embedding_policy_version,
                    now,
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

    def find_promoted_by_cluster_id(self, cluster_id: str) -> IssueCandidateRecord | None:
        row = self.db.connection.execute(
            """
            SELECT ic.candidate_id, ic.status, ic.cluster_id, ic.story_ids_json,
                   ic.readiness_score, ic.title
            FROM issue_candidates ic
            WHERE ic.status = ?
              AND (
                ic.cluster_id = ?
                OR ic.candidate_id IN (
                    SELECT issue_id FROM issue_story_links WHERE cluster_id = ?
                )
              )
            LIMIT 1
            """,
            (
                IssueCandidateStatus.PROMOTED.value,
                cluster_id,
                cluster_id,
            ),
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
        for story_id in story_ids:
            self.db.connection.execute(
                """
                INSERT INTO issue_story_links (issue_id, cluster_id, story_id, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(issue_id, story_id) DO NOTHING
                """,
                (issue_id, cluster_id, story_id, now),
            )
        self.db.connection.commit()


@dataclass
class SqliteStorySignalStore:
    db: SqliteDatabase

    def save_signals(self, story_id: str, policy: str, signals: Mapping[str, str]) -> None:
        self.db.connection.execute(
            """
            INSERT INTO story_signals (story_id, extraction_policy, signals_json, extracted_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(story_id, extraction_policy) DO UPDATE SET
                signals_json = excluded.signals_json,
                extracted_at = excluded.extracted_at
            """,
            (story_id, policy, json.dumps(dict(signals)), _utcnow().isoformat()),
        )
        self.db.connection.commit()

    def get_signals(self, story_id: str, policy: str) -> Mapping[str, str] | None:
        row = self.db.connection.execute(
            """
            SELECT signals_json FROM story_signals
            WHERE story_id = ? AND extraction_policy = ?
            """,
            (story_id, policy),
        ).fetchone()
        if row is None:
            return None
        return dict(json.loads(str(row["signals_json"])))


@dataclass
class SqliteClusterMembershipStore:
    db: SqliteDatabase

    def save_membership(self, story_id: str, lens: str, cluster_id: str) -> None:
        self.db.connection.execute(
            """
            INSERT INTO cluster_memberships (story_id, lens, cluster_id, computed_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(story_id, lens) DO UPDATE SET
                cluster_id = excluded.cluster_id,
                computed_at = excluded.computed_at
            """,
            (story_id, lens, cluster_id, _utcnow().isoformat()),
        )
        self.db.connection.commit()

    def get_cluster_members(self, cluster_id: str, lens: str) -> list[str]:
        rows = self.db.connection.execute(
            """
            SELECT story_id FROM cluster_memberships
            WHERE cluster_id = ? AND lens = ?
            ORDER BY story_id ASC
            """,
            (cluster_id, lens),
        ).fetchall()
        return [str(row["story_id"]) for row in rows]
