from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Mapping

from core.domain import (
    IdempotencyRecord,
    StoryDraftRecord,
    StoryGeoSnapshot,
    StoryLabel,
    StoryLifecycleStatus,
    StoryRecord,
)
from core.domain.narrative_i18n import I18N_LANGS, i18n_dict_from_json
from core.schema.payload import authoritative_payload_hash
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus, ReviewAuditEntry, ReviewDecision

try:
    import httpx  # pyright: ignore[reportMissingImports]
except Exception:  # pragma: no cover - optional dependency in local envs
    httpx = None

logger = logging.getLogger(__name__)

# Critical-path PostgREST tables for gateway readiness (intake, projection, clustering).
# Non-critical sinks (e.g. label miss telemetry) are intentionally excluded — GW-L10N-03 / D-L10N-3.
REQUIRED_READINESS_TABLES: frozenset[str] = frozenset(
    {
        "stories",
        "idempotency_keys",
        "story_embeddings",
        "doge_issues",
        "doge_issue_embeddings",
        "issue_candidates",
        "review_audit_log",
        "issue_story_links",
        "story_signals",
        "cluster_memberships",
        "story_drafts",
        "story_labels",
    }
)


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _coerce_jsonb_text_id_sequence(raw: Any) -> tuple[str, ...]:
    """Normalize JSONB story-id lists from PostgREST (often Python list) or JSON strings."""
    if raw is None:
        return ()
    if isinstance(raw, list):
        return tuple(str(x) for x in raw)
    if isinstance(raw, str):
        return tuple(json.loads(raw))
    return tuple(str(x) for x in list(raw))


_STORY_SELECT_FIELDS = (
    "story_id,schema_version,narrative_original_text,submitter_external_user_id,"
    "narrative_language,narrative_title_json,narrative_description_json,narrative_session_language,"
    "narrative_summary_json,institution_json,narrative_consistency_notes,narrative_canonical_type,narrative_canonical_labels_json,"
    "submitter_identity_issuer,lifecycle_status,created_at,updated_at,origin_source,origin_conversation_id,"
    "origin_tool_call_id,privacy_contains_pii,privacy_redaction_requested,"
    "geo_normalized_label,geo_latitude,geo_longitude,geo_confidence,geo_provider,geo_cluster_tags_json,"
    "geo_admin_district,geo_admin_settlement,geo_admin_region,geo_admin_country,"
    "geo_street,geo_house,geo_house_range,geo_houses_json,geo_address_line,"
    "schema_id,bound_schema_version,profile_id,profile_version,structured_payload,payload_hash"
)


def _i18n_dict_from_supabase_row(row: dict[str, Any], *, json_key: str) -> dict[str, str] | None:
    raw_json = row.get(json_key)
    if not raw_json:
        return None
    if isinstance(raw_json, dict):
        return {str(k): str(v) for k, v in raw_json.items()}
    return i18n_dict_from_json(str(raw_json))


def _summary_dict_from_supabase_row(row: dict[str, Any]) -> dict[str, str] | None:
    raw = row.get("narrative_summary_json")
    if not raw:
        return None
    if isinstance(raw, dict):
        return {str(k): str(v) for k, v in raw.items()}
    parsed = json.loads(str(raw))
    if isinstance(parsed, dict):
        return {str(k): str(v) for k, v in parsed.items()}
    return None


def _institution_dict_from_supabase_row(row: dict[str, Any]) -> dict[str, str] | None:
    raw = row.get("institution_json")
    if not raw:
        return None
    if isinstance(raw, dict):
        return {str(k): str(v) for k, v in raw.items()}
    parsed = json.loads(str(raw))
    if isinstance(parsed, dict):
        return {str(k): str(v) for k, v in parsed.items()}
    return None


def _structured_payload_from_supabase_row(row: dict[str, Any]) -> dict[str, Any] | None:
    raw = row.get("structured_payload")
    if raw is None or raw == "":
        return None
    if isinstance(raw, dict):
        return dict(raw)
    parsed = json.loads(str(raw))
    if isinstance(parsed, dict):
        return dict(parsed)
    return None


def _houses_from_supabase_row(row: dict[str, Any]) -> tuple[str, ...]:
    raw = row.get("geo_houses_json")
    if not raw:
        return ()
    if isinstance(raw, list):
        return tuple(str(item) for item in raw)
    parsed = json.loads(str(raw))
    if not isinstance(parsed, list):
        return ()
    return tuple(str(item) for item in parsed)


def _story_geo_supabase_fields(record: StoryRecord) -> dict[str, Any]:
    if record.geo is None:
        return {
            "geo_normalized_label": None,
            "geo_latitude": None,
            "geo_longitude": None,
            "geo_confidence": None,
            "geo_provider": None,
            "geo_cluster_tags_json": "[]",
            "geo_admin_district": None,
            "geo_admin_settlement": None,
            "geo_admin_region": None,
            "geo_admin_country": None,
            "geo_street": None,
            "geo_house": None,
            "geo_house_range": None,
            "geo_houses_json": "[]",
            "geo_address_line": None,
        }
    geo = record.geo
    return {
        "geo_normalized_label": geo.normalized_label,
        "geo_latitude": geo.latitude,
        "geo_longitude": geo.longitude,
        "geo_confidence": geo.confidence,
        "geo_provider": geo.provider,
        "geo_cluster_tags_json": json.dumps(list(geo.cluster_tags)),
        "geo_admin_district": geo.admin_district,
        "geo_admin_settlement": geo.admin_settlement,
        "geo_admin_region": geo.admin_region,
        "geo_admin_country": geo.admin_country,
        "geo_street": geo.street,
        "geo_house": geo.house,
        "geo_house_range": geo.house_range,
        "geo_houses_json": json.dumps(list(geo.houses)),
        "geo_address_line": geo.address_line,
    }


def _story_record_from_supabase_row(row: dict[str, Any]) -> StoryRecord:
    geo: StoryGeoSnapshot | None = None
    if row.get("geo_normalized_label"):
        geo = StoryGeoSnapshot(
            normalized_label=str(row["geo_normalized_label"]),
            latitude=float(row["geo_latitude"]),
            longitude=float(row["geo_longitude"]),
            confidence=float(row["geo_confidence"]),
            provider=str(row["geo_provider"]),
            cluster_tags=tuple(json.loads(str(row.get("geo_cluster_tags_json") or "[]"))),
            admin_district=row.get("geo_admin_district"),
            admin_settlement=row.get("geo_admin_settlement"),
            admin_region=row.get("geo_admin_region"),
            admin_country=row.get("geo_admin_country"),
            street=row.get("geo_street"),
            house=row.get("geo_house"),
            house_range=row.get("geo_house_range"),
            houses=_houses_from_supabase_row(row),
            address_line=row.get("geo_address_line"),
        )
    return StoryRecord(
        story_id=str(row["story_id"]),
        schema_version=str(row["schema_version"]),
        narrative_original_text=str(row["narrative_original_text"]),
        submitter_external_user_id=str(row["submitter_external_user_id"]),
        narrative_language=row["narrative_language"],
        narrative_title=_i18n_dict_from_supabase_row(row, json_key="narrative_title_json"),
        narrative_description=_i18n_dict_from_supabase_row(row, json_key="narrative_description_json"),
        narrative_summary=_summary_dict_from_supabase_row(row),
        narrative_institution=_institution_dict_from_supabase_row(row),
        narrative_session_language=row.get("narrative_session_language"),
        narrative_consistency_notes=row.get("narrative_consistency_notes"),
        narrative_canonical_type=row["narrative_canonical_type"],
        narrative_canonical_labels=tuple(
            json.loads(str(row["narrative_canonical_labels_json"]))
        ),
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
        schema_id=row.get("schema_id"),
        bound_schema_version=row.get("bound_schema_version"),
        profile_id=row.get("profile_id"),
        profile_version=row.get("profile_version"),
        structured_payload=_structured_payload_from_supabase_row(row),
        payload_hash=row.get("payload_hash"),
    )


@dataclass
class SupabaseDatabase:
    base_url: str
    service_role_key: str
    timeout_s: float = 15.0

    @classmethod
    def from_http(
        cls,
        *,
        supabase_url: str,
        service_role_key: str,
        timeout_s: float = 15.0,
    ) -> SupabaseDatabase:
        if not supabase_url.startswith("http://") and not supabase_url.startswith(
            "https://"
        ):
            raise ValueError(f"Unsupported SUPABASE_URL: {supabase_url!r}.")
        if not service_role_key.strip():
            raise ValueError("SUPABASE_SERVICE_ROLE must be non-empty.")
        return cls(
            base_url=supabase_url.rstrip("/"),
            service_role_key=service_role_key.strip(),
            timeout_s=timeout_s,
        )

    def _client(self) -> Any:
        if httpx is None:
            raise RuntimeError(
                "Supabase HTTP backend requires httpx. Install dependency: httpx."
            )
        return httpx.Client(timeout=self.timeout_s)

    def _headers(self, *, prefer: str | None = None) -> dict[str, str]:
        headers = {
            "apikey": self.service_role_key,
            "Authorization": f"Bearer {self.service_role_key}",
            "Content-Type": "application/json",
        }
        if prefer is not None:
            headers["Prefer"] = prefer
        return headers

    def _request(
        self,
        *,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        json_body: Any = None,
        prefer: str | None = None,
    ) -> Any:
        logger.debug(
            "supabase.request",
            extra={"method": method, "path": path, "has_params": bool(params)},
        )
        try:
            with self._client() as client:
                response = client.request(
                    method=method,
                    url=f"{self.base_url}{path}",
                    headers=self._headers(prefer=prefer),
                    params=params,
                    json=json_body,
                )
            response.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            status_code = None
            error_body_preview = str(exc)
            if httpx is not None and isinstance(exc, httpx.HTTPStatusError):
                response = getattr(exc, "response", None)
                if response is not None:
                    status_code = getattr(response, "status_code", None)
                    error_body_preview = (getattr(response, "text", "") or "").strip()[
                        :300
                    ]
            logger.error(
                "supabase.request_failed",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "error_body_preview": error_body_preview,
                    "error_type": type(exc).__name__,
                    "outcome": "error",
                    "stage": "db.supabase",
                },
            )
            raise
        logger.debug(
            "supabase.response",
            extra={"method": method, "path": path, "status_code": response.status_code},
        )
        if response.text.strip():
            return response.json()
        return None

    def _escape(self, value: str) -> str:
        return value.replace('"', '\\"')

    def _eq_filter(self, value: str) -> str:
        return f"eq.{value}"

    def healthcheck(self) -> bool:
        try:
            self._request(method="GET", path="/rest/v1/", params={"limit": "1"})
            return True
        except Exception:
            return False

    def required_tables_ready(self) -> bool:
        try:
            for table_name in REQUIRED_READINESS_TABLES:
                self._request(
                    method="GET",
                    path=f"/rest/v1/{table_name}",
                    params={"select": "*", "limit": "1"},
                )
            return True
        except Exception:
            return False

    _STORIES_GEO_ADMIN_COLUMNS = frozenset(
        {
            "geo_admin_district",
            "geo_admin_settlement",
            "geo_admin_region",
            "geo_admin_country",
        }
    )
    _STORIES_BINDING_COLUMNS = frozenset(
        {
            "schema_id",
            "bound_schema_version",
            "profile_id",
            "profile_version",
            "structured_payload",
            "payload_hash",
        }
    )
    _STORIES_GEO_DETAIL_COLUMNS = frozenset(
        {
            "geo_street",
            "geo_house",
            "geo_house_range",
            "geo_houses_json",
            "geo_address_line",
        }
    )

    def required_stories_geo_admin_columns_ready(self) -> bool:
        """True when migration 20260510_* geo_admin_* columns exist on hosted stories."""
        try:
            self._request(
                method="GET",
                path="/rest/v1/stories",
                params={
                    "select": ",".join(sorted(self._STORIES_GEO_ADMIN_COLUMNS)),
                    "limit": "1",
                },
            )
            return True
        except Exception:
            return False

    def stories_geo_admin_columns_ready(self) -> bool:
        cached = getattr(self, "_stories_geo_admin_columns_ready", None)
        if cached is None:
            cached = self.required_stories_geo_admin_columns_ready()
            self._stories_geo_admin_columns_ready = cached
        return cached

    def required_stories_binding_columns_ready(self) -> bool:
        """True when GW-SSR-02 binding columns exist on hosted stories."""
        try:
            self._request(
                method="GET",
                path="/rest/v1/stories",
                params={
                    "select": ",".join(sorted(self._STORIES_BINDING_COLUMNS)),
                    "limit": "1",
                },
            )
            return True
        except Exception:
            return False

    def stories_binding_columns_ready(self) -> bool:
        cached = getattr(self, "_stories_binding_columns_ready", None)
        if cached is None:
            cached = self.required_stories_binding_columns_ready()
            self._stories_binding_columns_ready = cached
        return cached

    def required_stories_geo_detail_columns_ready(self) -> bool:
        """True when GW-SSR-24 geo depth columns exist on hosted stories."""
        try:
            self._request(
                method="GET",
                path="/rest/v1/stories",
                params={
                    "select": ",".join(sorted(self._STORIES_GEO_DETAIL_COLUMNS)),
                    "limit": "1",
                },
            )
            return True
        except Exception:
            return False

    def stories_geo_detail_columns_ready(self) -> bool:
        cached = getattr(self, "_stories_geo_detail_columns_ready", None)
        if cached is None:
            cached = self.required_stories_geo_detail_columns_ready()
            self._stories_geo_detail_columns_ready = cached
        return cached

    def required_columns_ready(self) -> bool:
        from core.projection.columnar_storage import DOGE_ISSUES_COLUMNAR_READINESS_COLUMNS

        required: dict[str, set[str]] = {
            "stories": {
                "story_id",
                "narrative_language",
                "narrative_canonical_type",
                "narrative_canonical_labels_json",
                "geo_normalized_label",
                "geo_latitude",
                "geo_longitude",
                "geo_confidence",
                "geo_provider",
                "geo_cluster_tags_json",
            },
            "story_embeddings": {
                "embedding_vector_json",
                "embedding_policy_version",
            },
            "doge_issue_embeddings": {
                "embedding_vector_json",
                "embedding_policy_version",
            },
            "doge_issues": set(DOGE_ISSUES_COLUMNAR_READINESS_COLUMNS),
        }
        try:
            for table_name, columns in required.items():
                self._request(
                    method="GET",
                    path=f"/rest/v1/{table_name}",
                    params={"select": ",".join(sorted(columns)), "limit": "1"},
                )
            return True
        except Exception:
            return False

    def required_stories_intake_v2_columns_ready(self) -> bool:
        """True when hosted DB has REQ-33 v2 narrative columns (migration 20260513_*)."""
        columns = (
            "narrative_title_json",
            "narrative_description_json",
            "narrative_session_language",
        )
        try:
            self._request(
                method="GET",
                path="/rest/v1/stories",
                params={"select": ",".join(sorted(columns)), "limit": "1"},
            )
            return True
        except Exception:
            return False

    def required_stories_narrative_extension_columns_ready(self) -> bool:
        """True when hosted DB has STORY-M2-02-06 narrative extension columns (migration 20260511_1200_*)."""
        columns = (
            "narrative_summary_json",
            "narrative_consistency_notes",
        )
        try:
            self._request(
                method="GET",
                path="/rest/v1/stories",
                params={"select": ",".join(sorted(columns)), "limit": "1"},
            )
            return True
        except Exception:
            return False

    def service_role_policy_probe(self) -> bool:
        try:
            self._request(
                method="GET",
                path="/rest/v1/stories",
                params={"select": "story_id", "limit": "1"},
            )
            return True
        except Exception:
            return False


def _story_select_fields_for_db(db: SupabaseDatabase) -> str:
    """SELECT list for hosted DB; omits geo_admin_* / binding / geo-detail cols when not migrated."""
    omit: set[str] = set()
    if not db.stories_geo_admin_columns_ready():
        omit |= set(SupabaseDatabase._STORIES_GEO_ADMIN_COLUMNS)
    if not db.stories_binding_columns_ready():
        omit |= set(SupabaseDatabase._STORIES_BINDING_COLUMNS)
    detail_probe = getattr(db, "stories_geo_detail_columns_ready", None)
    if detail_probe is not None and not detail_probe():
        omit |= set(SupabaseDatabase._STORIES_GEO_DETAIL_COLUMNS)
    if not omit:
        return _STORY_SELECT_FIELDS
    parts = [
        field.strip()
        for field in _STORY_SELECT_FIELDS.split(",")
        if field.strip() and field.strip() not in omit
    ]
    return ",".join(parts)


@dataclass
class SupabaseStoryRepository:
    db: SupabaseDatabase

    def save_story(self, record: StoryRecord) -> StoryRecord:
        logger.debug(
            "supabase.save_story_start",
            extra={"story_id": record.story_id, "status": record.lifecycle_status.value},
        )
        row: dict[str, Any] = {
            "story_id": record.story_id,
            "schema_version": record.schema_version,
            "narrative_original_text": record.narrative_original_text,
            "submitter_external_user_id": record.submitter_external_user_id,
            "narrative_language": record.narrative_language,
            "narrative_title_json": record.narrative_title,
            "narrative_description_json": record.narrative_description,
            "narrative_session_language": record.narrative_session_language,
            "narrative_summary_json": record.narrative_summary,
            "institution_json": record.narrative_institution,
            "narrative_consistency_notes": record.narrative_consistency_notes,
            "narrative_canonical_type": record.narrative_canonical_type,
            "narrative_canonical_labels_json": json.dumps(list(record.narrative_canonical_labels)),
            "submitter_identity_issuer": record.submitter_identity_issuer,
            "lifecycle_status": record.lifecycle_status.value,
            "created_at": record.created_at.isoformat(),
            "updated_at": record.updated_at.isoformat(),
            "origin_source": record.origin_source,
            "origin_conversation_id": record.origin_conversation_id,
            "origin_tool_call_id": record.origin_tool_call_id,
            "privacy_contains_pii": record.privacy_contains_pii,
            "privacy_redaction_requested": record.privacy_redaction_requested,
            "schema_id": record.schema_id,
            "bound_schema_version": record.bound_schema_version,
            "profile_id": record.profile_id,
            "profile_version": record.profile_version,
            "structured_payload": record.structured_payload,
            "payload_hash": authoritative_payload_hash(record.structured_payload),
        }
        row.update(_story_geo_supabase_fields(record))
        if not self.db.stories_geo_admin_columns_ready():
            for key in SupabaseDatabase._STORIES_GEO_ADMIN_COLUMNS:
                row.pop(key, None)
        if not self.db.stories_binding_columns_ready():
            for key in SupabaseDatabase._STORIES_BINDING_COLUMNS:
                row.pop(key, None)
        if not self.db.stories_geo_detail_columns_ready():
            for key in SupabaseDatabase._STORIES_GEO_DETAIL_COLUMNS:
                row.pop(key, None)
        try:
            self.db._request(
                method="POST",
                path="/rest/v1/stories",
                params={"on_conflict": "story_id"},
                json_body=[row],
                prefer="resolution=merge-duplicates,return=minimal",
            )
        except Exception as exc:  # noqa: BLE001
            logger.error(
                "repo.supabase.save_story_failed",
                extra={
                    "story_id": record.story_id,
                    "path": "/rest/v1/stories",
                    "error_type": type(exc).__name__,
                    "backend": "supabase",
                    "repository_class": self.__class__.__name__,
                    "stage": "repository.supabase.save_story",
                    "outcome": "error",
                },
            )
            raise
        logger.info(
            "repo.supabase.save_story_done",
            extra={
                "story_id": record.story_id,
                "path": "/rest/v1/stories",
                "backend": "supabase",
                "repository_class": self.__class__.__name__,
                "stage": "repository.supabase.save_story",
                "outcome": "success",
            },
        )
        logger.debug("supabase.save_story_done", extra={"story_id": record.story_id})
        return record

    def get_story(self, story_id: str) -> StoryRecord | None:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/stories",
            params={
                "select": _story_select_fields_for_db(self.db),
                "story_id": self.db._eq_filter(story_id),
                "limit": "1",
            },
        )
        if not rows:
            return None
        return _story_record_from_supabase_row(rows[0])

    def list_stories(self) -> list[StoryRecord]:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/stories",
            params={
                "select": _story_select_fields_for_db(self.db),
                "order": "created_at.asc",
            },
        )
        return [_story_record_from_supabase_row(row) for row in rows]

    def list_stories_by_submitter(self, submitter_external_user_id: str) -> list[StoryRecord]:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/stories",
            params={
                "select": _story_select_fields_for_db(self.db),
                "submitter_external_user_id": self.db._eq_filter(
                    submitter_external_user_id.strip()
                ),
                "order": "created_at.desc",
            },
        )
        return [_story_record_from_supabase_row(row) for row in rows]

    def list_stories_ready_for_clustering(self) -> list[StoryRecord]:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/stories",
            params={
                "select": _story_select_fields_for_db(self.db),
                "lifecycle_status": self.db._eq_filter(
                    StoryLifecycleStatus.READY_FOR_PROFILE.value
                ),
                "order": "created_at.asc",
            },
        )
        return [_story_record_from_supabase_row(row) for row in rows]

    def update_lifecycle_status(self, story_id: str, status: StoryLifecycleStatus) -> None:
        self.db._request(
            method="PATCH",
            path="/rest/v1/stories",
            params={"story_id": self.db._eq_filter(story_id)},
            json_body={
                "lifecycle_status": status.value,
                "updated_at": _utcnow().isoformat(),
            },
            prefer="return=minimal",
        )


@dataclass
class SupabaseIdempotencyRepository:
    db: SupabaseDatabase

    def get_by_key(self, key: str) -> IdempotencyRecord | None:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/idempotency_keys",
            params={
                "select": "key,story_id,created_at",
                "key": self.db._eq_filter(key),
                "limit": "1",
            },
        )
        if not rows:
            return None
        row = rows[0]
        return IdempotencyRecord(
            key=str(row["key"]),
            story_id=str(row["story_id"]),
            created_at=_parse_dt(str(row["created_at"])),
        )

    def save(self, record: IdempotencyRecord) -> IdempotencyRecord:
        self.db._request(
            method="POST",
            path="/rest/v1/idempotency_keys",
            params={"on_conflict": "key"},
            json_body=[
                {
                    "key": record.key,
                    "story_id": record.story_id,
                    "created_at": record.created_at.isoformat(),
                }
            ],
            prefer="resolution=merge-duplicates,return=minimal",
        )
        return record


@dataclass
class SupabaseStoryDraftRepository:
    db: SupabaseDatabase

    def save_draft(self, record: StoryDraftRecord) -> StoryDraftRecord:
        self.db._request(
            method="POST",
            path="/rest/v1/story_drafts",
            params={"on_conflict": "draft_id"},
            json_body=[
                {
                    "draft_id": record.draft_id,
                    "payload_json": record.payload,
                    "created_at": record.created_at.isoformat(),
                    "expires_at": record.expires_at.isoformat(),
                    "updated_at": record.updated_at.isoformat(),
                }
            ],
            prefer="resolution=merge-duplicates,return=minimal",
        )
        return record

    def get_draft(self, draft_id: str) -> StoryDraftRecord | None:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/story_drafts",
            params={
                "select": "draft_id,payload_json,created_at,expires_at,updated_at",
                "draft_id": self.db._eq_filter(draft_id),
                "limit": "1",
            },
        )
        if not rows:
            return None
        row = rows[0]
        expires_at = _parse_dt(str(row["expires_at"]))
        if expires_at <= _utcnow():
            self.db._request(
                method="DELETE",
                path="/rest/v1/story_drafts",
                params={"draft_id": self.db._eq_filter(draft_id)},
                prefer="return=minimal",
            )
            return None
        payload = row["payload_json"]
        if isinstance(payload, str):
            payload = json.loads(payload)
        created_at = _parse_dt(str(row["created_at"]))
        updated_raw = row.get("updated_at")
        updated_at = (
            _parse_dt(str(updated_raw))
            if updated_raw is not None
            else created_at
        )
        return StoryDraftRecord(
            draft_id=str(row["draft_id"]),
            payload=dict(payload),
            created_at=created_at,
            expires_at=expires_at,
            updated_at=updated_at,
        )

    def delete_draft(self, draft_id: str) -> None:
        self.db._request(
            method="DELETE",
            path="/rest/v1/story_drafts",
            params={"draft_id": self.db._eq_filter(draft_id)},
            prefer="return=minimal",
        )


@dataclass
class SupabaseDraftOwnerRepository:
    db: SupabaseDatabase

    def set_owner(self, draft_id: str, submitter_external_user_id: str) -> None:
        now = _utcnow().isoformat()
        self.db._request(
            method="POST",
            path="/rest/v1/draft_owner",
            params={"on_conflict": "draft_id"},
            json_body=[
                {
                    "draft_id": draft_id,
                    "submitter_external_user_id": submitter_external_user_id,
                    "created_at": now,
                }
            ],
            prefer="resolution=ignore-duplicates,return=minimal",
        )

    def get_current_draft(
        self, submitter_external_user_id: str
    ) -> StoryDraftRecord | None:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/draft_owner",
            params={
                "select": "draft_id",
                "submitter_external_user_id": self.db._eq_filter(
                    submitter_external_user_id
                ),
            },
        )
        if not rows:
            return None
        draft_repo = SupabaseStoryDraftRepository(self.db)
        candidates: list[StoryDraftRecord] = []
        for row in rows:
            record = draft_repo.get_draft(str(row["draft_id"]))
            if record is not None:
                candidates.append(record)
        if not candidates:
            return None
        return max(candidates, key=lambda record: record.created_at)


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
        self.db._request(
            method="POST",
            path="/rest/v1/story_embeddings",
            json_body=[
                {
                    "story_id": story_id,
                    "model_name": model_name,
                    "embedding_vector_json": json.dumps(list(embedding_vector)),
                    "source_checksum": source_checksum,
                    "embedding_policy_version": embedding_policy_version,
                    "created_at": _utcnow().isoformat(),
                }
            ],
            prefer="return=minimal",
        )


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
        from core.projection.columnar_storage import payload_to_storage_fields

        now = _utcnow().isoformat()
        storage_fields = payload_to_storage_fields(payload)
        self.db._request(
            method="POST",
            path="/rest/v1/doge_issues",
            params={"on_conflict": "issue_id"},
            json_body=[
                {
                    "issue_id": issue_id,
                    "status": status,
                    "policy_version": policy_version,
                    "created_at": now,
                    "updated_at": now,
                    **storage_fields,
                }
            ],
            prefer="resolution=merge-duplicates,return=minimal",
        )

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
        from core.projection.columnar_storage import (
            COLUMNAR_ROW_SELECT,
            assemble_public_issue_from_storage_row,
        )
        from core.projection.read_filters import filter_projection_rows

        rows_data = self.db._request(
            method="GET",
            path="/rest/v1/doge_issues",
            params={
                "select": COLUMNAR_ROW_SELECT,
                "order": "created_at.desc",
            },
        )
        rows: list[tuple[str, str, dict[str, object], str]] = []
        for row in rows_data:
            assembled = assemble_public_issue_from_storage_row(dict(row))
            rows.append(
                (
                    str(row["issue_id"]),
                    str(row["status"]),
                    assembled,
                    str(row["created_at"]),
                )
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
        from core.projection.columnar_storage import (
            COLUMNAR_ROW_SELECT,
            assemble_public_issue_from_storage_row,
        )

        rows = self.db._request(
            method="GET",
            path="/rest/v1/doge_issues",
            params={
                "select": COLUMNAR_ROW_SELECT,
                "issue_id": self.db._eq_filter(issue_id),
                "limit": "1",
            },
        )
        if not rows:
            return None
        from core.projection.read_filters import merge_projection_columns

        row = dict(rows[0])
        assembled = assemble_public_issue_from_storage_row(row)
        return merge_projection_columns(
            issue_id=str(row["issue_id"]),
            row_status=str(row["status"]),
            payload=assembled,
            created_at=str(row["created_at"]),
        )


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
        now = _utcnow().isoformat()
        updated = self.db._request(
            method="PATCH",
            path="/rest/v1/doge_issue_embeddings",
            params={
                "issue_id": self.db._eq_filter(issue_id),
                "select": "issue_id",
            },
            json_body={
                "model_name": model_name,
                "embedding_vector_json": json.dumps(list(embedding_vector)),
                "source_checksum": source_checksum,
                "embedding_policy_version": embedding_policy_version,
                "created_at": now,
            },
            prefer="return=representation",
        )
        if not updated:
            self.db._request(
                method="POST",
                path="/rest/v1/doge_issue_embeddings",
                json_body=[
                    {
                        "issue_id": issue_id,
                        "model_name": model_name,
                        "embedding_vector_json": json.dumps(list(embedding_vector)),
                        "source_checksum": source_checksum,
                        "embedding_policy_version": embedding_policy_version,
                        "created_at": now,
                    }
                ],
                prefer="return=minimal",
            )


@dataclass
class SupabaseIssueCandidateStore:
    db: SupabaseDatabase

    def save(self, record: IssueCandidateRecord) -> IssueCandidateRecord:
        self.db._request(
            method="POST",
            path="/rest/v1/issue_candidates",
            params={"on_conflict": "candidate_id"},
            json_body=[
                {
                    "candidate_id": record.candidate_id,
                    "status": record.status.value,
                    "cluster_id": record.cluster_id,
                    "story_ids_json": json.dumps(list(record.story_ids)),
                    "readiness_score": record.readiness_score,
                    "title": record.title,
                    "updated_at": _utcnow().isoformat(),
                }
            ],
            prefer="resolution=merge-duplicates,return=minimal",
        )
        return record

    def get(self, candidate_id: str) -> IssueCandidateRecord | None:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/issue_candidates",
            params={
                "select": "candidate_id,status,cluster_id,story_ids_json,readiness_score,title",
                "candidate_id": self.db._eq_filter(candidate_id),
                "limit": "1",
            },
        )
        if not rows:
            return None
        row = rows[0]
        return IssueCandidateRecord(
            candidate_id=str(row["candidate_id"]),
            status=IssueCandidateStatus(str(row["status"])),
            cluster_id=str(row["cluster_id"]),
            story_ids=_coerce_jsonb_text_id_sequence(row["story_ids_json"]),
            readiness_score=int(row["readiness_score"]),
            title=str(row["title"]),
        )

    def find_promoted_by_cluster_id(self, cluster_id: str) -> IssueCandidateRecord | None:
        link_rows = self.db._request(
            method="GET",
            path="/rest/v1/issue_story_links",
            params={
                "select": "issue_id",
                "cluster_id": self.db._eq_filter(cluster_id),
            },
        )
        for link_row in link_rows:
            issue_id = str(link_row["issue_id"])
            rows = self.db._request(
                method="GET",
                path="/rest/v1/issue_candidates",
                params={
                    "select": "candidate_id,status,cluster_id,story_ids_json,readiness_score,title",
                    "candidate_id": self.db._eq_filter(issue_id),
                    "status": self.db._eq_filter(IssueCandidateStatus.PROMOTED.value),
                    "limit": "1",
                },
            )
            if rows:
                row = rows[0]
                return IssueCandidateRecord(
                    candidate_id=str(row["candidate_id"]),
                    status=IssueCandidateStatus(str(row["status"])),
                    cluster_id=str(row["cluster_id"]),
                    story_ids=_coerce_jsonb_text_id_sequence(row["story_ids_json"]),
                    readiness_score=int(row["readiness_score"]),
                    title=str(row["title"]),
                )
        rows = self.db._request(
            method="GET",
            path="/rest/v1/issue_candidates",
            params={
                "select": "candidate_id,status,cluster_id,story_ids_json,readiness_score,title",
                "cluster_id": self.db._eq_filter(cluster_id),
                "status": self.db._eq_filter(IssueCandidateStatus.PROMOTED.value),
                "limit": "1",
            },
        )
        if not rows:
            return None
        row = rows[0]
        return IssueCandidateRecord(
            candidate_id=str(row["candidate_id"]),
            status=IssueCandidateStatus(str(row["status"])),
            cluster_id=str(row["cluster_id"]),
            story_ids=_coerce_jsonb_text_id_sequence(row["story_ids_json"]),
            readiness_score=int(row["readiness_score"]),
            title=str(row["title"]),
        )

    def delete(self, candidate_id: str) -> None:
        self.db._request(
            method="DELETE",
            path="/rest/v1/issue_candidates",
            params={"candidate_id": self.db._eq_filter(candidate_id)},
            prefer="return=minimal",
        )


@dataclass
class SupabaseReviewAuditLogRepository:
    db: SupabaseDatabase

    def append(self, entry: ReviewAuditEntry) -> ReviewAuditEntry:
        self.db._request(
            method="POST",
            path="/rest/v1/review_audit_log",
            json_body=[
                {
                    "candidate_id": entry.candidate_id,
                    "actor": entry.actor,
                    "decision": entry.decision.value,
                    "rationale": entry.rationale,
                    "related_cluster_id": entry.related_cluster_id,
                    "related_story_ids_json": json.dumps(list(entry.related_story_ids)),
                    "created_at": _utcnow().isoformat(),
                }
            ],
            prefer="return=minimal",
        )
        return entry

    def list_for_candidate(self, candidate_id: str) -> tuple[ReviewAuditEntry, ...]:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/review_audit_log",
            params={
                "select": "candidate_id,actor,decision,rationale,related_cluster_id,related_story_ids_json",
                "candidate_id": self.db._eq_filter(candidate_id),
                "order": "audit_id.asc",
            },
        )
        return tuple(
            ReviewAuditEntry(
                candidate_id=str(row["candidate_id"]),
                actor=str(row["actor"]),
                decision=ReviewDecision(str(row["decision"])),
                rationale=str(row["rationale"]),
                related_cluster_id=str(row["related_cluster_id"]),
                related_story_ids=_coerce_jsonb_text_id_sequence(row["related_story_ids_json"]),
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
        now = _utcnow().isoformat()
        if not story_ids:
            return
        payload = [
            {
                "issue_id": issue_id,
                "cluster_id": cluster_id,
                "story_id": story_id,
                "created_at": now,
            }
            for story_id in story_ids
        ]
        self.db._request(
            method="POST",
            path="/rest/v1/issue_story_links",
            params={"on_conflict": "issue_id,story_id"},
            json_body=payload,
            prefer="resolution=ignore-duplicates,return=minimal",
        )

    def get_issue_id_for_story(self, story_id: str) -> str | None:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/issue_story_links",
            params={
                "select": "issue_id",
                "story_id": self.db._eq_filter(story_id),
                "order": "created_at.desc",
                "limit": "1",
            },
        )
        if not rows:
            return None
        return str(rows[0]["issue_id"])


@dataclass
class SupabaseStorySignalStore:
    db: SupabaseDatabase

    def save_signals(self, story_id: str, policy: str, signals: Mapping[str, str]) -> None:
        self.db._request(
            method="POST",
            path="/rest/v1/story_signals",
            params={"on_conflict": "story_id,extraction_policy"},
            json_body=[
                {
                    "story_id": story_id,
                    "extraction_policy": policy,
                    "signals_json": dict(signals),
                    "extracted_at": _utcnow().isoformat(),
                }
            ],
            prefer="resolution=merge-duplicates,return=minimal",
        )

    def get_signals(self, story_id: str, policy: str) -> Mapping[str, str] | None:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/story_signals",
            params={
                "select": "signals_json",
                "story_id": self.db._eq_filter(story_id),
                "extraction_policy": self.db._eq_filter(policy),
                "limit": "1",
            },
        )
        if not rows:
            return None
        raw = rows[0]["signals_json"]
        if isinstance(raw, str):
            return dict(json.loads(raw))
        return dict(raw)


@dataclass
class SupabaseStoryLabelRepository:
    db: SupabaseDatabase

    def save_labels(self, labels: tuple[StoryLabel, ...]) -> None:
        if not labels:
            return
        story_ids = sorted({label.story_id for label in labels})
        for story_id in story_ids:
            self.db._request(
                method="DELETE",
                path="/rest/v1/story_labels",
                params={"story_id": self.db._eq_filter(story_id)},
                prefer="return=minimal",
            )
        self.db._request(
            method="POST",
            path="/rest/v1/story_labels",
            json_body=[
                {
                    "story_id": row.story_id,
                    "axis": row.axis,
                    "label": row.label,
                    "disposition": row.disposition,
                }
                for row in labels
            ],
            prefer="return=minimal",
        )

    def list_by_story(self, story_id: str) -> tuple[StoryLabel, ...]:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/story_labels",
            params={
                "select": "story_id,axis,label,disposition",
                "story_id": self.db._eq_filter(story_id),
                "order": "axis.asc,label.asc",
            },
        )
        return tuple(
            StoryLabel(
                story_id=str(row["story_id"]),
                axis=str(row["axis"]),
                label=str(row["label"]),
                disposition=str(row["disposition"]),
            )
            for row in rows
        )

    def list_by_axis(self, axis: str) -> tuple[StoryLabel, ...]:
        normalized = axis.strip().lower()
        rows = self.db._request(
            method="GET",
            path="/rest/v1/story_labels",
            params={
                "select": "story_id,axis,label,disposition",
                "axis": self.db._eq_filter(normalized),
                "order": "story_id.asc,label.asc",
            },
        )
        return tuple(
            StoryLabel(
                story_id=str(row["story_id"]),
                axis=str(row["axis"]),
                label=str(row["label"]),
                disposition=str(row["disposition"]),
            )
            for row in rows
        )


@dataclass
class SupabaseClusterMembershipStore:
    db: SupabaseDatabase

    def save_membership(self, story_id: str, lens: str, cluster_id: str) -> None:
        self.db._request(
            method="POST",
            path="/rest/v1/cluster_memberships",
            params={"on_conflict": "story_id,lens"},
            json_body=[
                {
                    "story_id": story_id,
                    "lens": lens,
                    "cluster_id": cluster_id,
                    "computed_at": _utcnow().isoformat(),
                }
            ],
            prefer="resolution=merge-duplicates,return=minimal",
        )

    def get_cluster_members(self, cluster_id: str, lens: str) -> list[str]:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/cluster_memberships",
            params={
                "select": "story_id",
                "cluster_id": self.db._eq_filter(cluster_id),
                "lens": self.db._eq_filter(lens),
                "order": "story_id.asc",
            },
        )
        return [str(row["story_id"]) for row in rows]


@dataclass
class SupabaseLabelTranslationMissStore:
    db: SupabaseDatabase

    def record_miss(self, label_key: str, locale: str) -> None:
        now = _utcnow().isoformat()
        rows = self.db._request(
            method="GET",
            path="/rest/v1/label_translation_misses",
            params={
                "select": "miss_count",
                "label_key": self.db._eq_filter(label_key),
                "locale": self.db._eq_filter(locale),
                "limit": "1",
            },
        )
        if rows:
            current = int(rows[0]["miss_count"])
            self.db._request(
                method="PATCH",
                path="/rest/v1/label_translation_misses",
                params={
                    "label_key": self.db._eq_filter(label_key),
                    "locale": self.db._eq_filter(locale),
                },
                json_body={"miss_count": current + 1, "last_seen_at": now},
                prefer="return=minimal",
            )
            return
        self.db._request(
            method="POST",
            path="/rest/v1/label_translation_misses",
            json_body=[
                {
                    "label_key": label_key,
                    "locale": locale,
                    "miss_count": 1,
                    "last_seen_at": now,
                }
            ],
            prefer="return=minimal",
        )

    def get_miss_count(self, label_key: str, locale: str) -> int:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/label_translation_misses",
            params={
                "select": "miss_count",
                "label_key": self.db._eq_filter(label_key),
                "locale": self.db._eq_filter(locale),
                "limit": "1",
            },
        )
        if not rows:
            return 0
        return int(rows[0]["miss_count"])

