from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from core.domain import IdempotencyRecord, StoryLifecycleStatus, StoryRecord
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus, ReviewAuditEntry, ReviewDecision

try:
    import httpx  # pyright: ignore[reportMissingImports]
except Exception:  # pragma: no cover - optional dependency in local envs
    httpx = None


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


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
        with self._client() as client:
            response = client.request(
                method=method,
                url=f"{self.base_url}{path}",
                headers=self._headers(prefer=prefer),
                params=params,
                json=json_body,
            )
        response.raise_for_status()
        if response.text.strip():
            return response.json()
        return None

    def _escape(self, value: str) -> str:
        return value.replace('"', '\\"')

    def _eq_filter(self, value: str) -> str:
        return f'eq."{self._escape(value)}"'

    def healthcheck(self) -> bool:
        try:
            self._request(method="GET", path="/rest/v1/", params={"limit": "1"})
            return True
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
            for table_name in required:
                self._request(
                    method="GET",
                    path=f"/rest/v1/{table_name}",
                    params={"select": "*", "limit": "1"},
                )
            return True
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
            for table_name, columns in required.items():
                self._request(
                    method="GET",
                    path=f"/rest/v1/{table_name}",
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


@dataclass
class SupabaseStoryRepository:
    db: SupabaseDatabase

    def save_story(self, record: StoryRecord) -> StoryRecord:
        self.db._request(
            method="POST",
            path="/rest/v1/stories",
            params={"on_conflict": "story_id"},
            json_body=[
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
                }
            ],
            prefer="resolution=merge-duplicates,return=minimal",
        )
        return record

    def get_story(self, story_id: str) -> StoryRecord | None:
        rows = self.db._request(
            method="GET",
            path="/rest/v1/stories",
            params={
                "select": "story_id,schema_version,narrative_original_text,submitter_external_user_id,narrative_language,narrative_title_hint,narrative_canonical_type,narrative_canonical_labels_json,submitter_identity_issuer,lifecycle_status,created_at,updated_at,origin_source,origin_conversation_id,origin_tool_call_id,privacy_contains_pii,privacy_redaction_requested",
                "story_id": self.db._eq_filter(story_id),
                "limit": "1",
            },
        )
        if not rows:
            return None
        row = rows[0]
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
        rows = self.db._request(
            method="GET",
            path="/rest/v1/stories",
            params={
                "select": "story_id,schema_version,narrative_original_text,submitter_external_user_id,narrative_language,narrative_title_hint,narrative_canonical_type,narrative_canonical_labels_json,submitter_identity_issuer,lifecycle_status,created_at,updated_at,origin_source,origin_conversation_id,origin_tool_call_id,privacy_contains_pii,privacy_redaction_requested",
                "order": "created_at.asc",
            },
        )
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
        now = _utcnow().isoformat()
        self.db._request(
            method="POST",
            path="/rest/v1/spa_issue_projections",
            params={"on_conflict": "issue_id"},
            json_body=[
                {
                    "issue_id": issue_id,
                    "status": status,
                    "payload_json": json.dumps(payload),
                    "policy_version": policy_version,
                    "created_at": now,
                    "updated_at": now,
                }
            ],
            prefer="resolution=merge-duplicates,return=minimal",
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
        self.db._request(
            method="POST",
            path="/rest/v1/spa_issue_projection_embeddings",
            json_body=[
                {
                    "issue_id": issue_id,
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
            story_ids=tuple(json.loads(str(row["story_ids_json"]))),
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
        self.db._request(
            method="DELETE",
            path="/rest/v1/issue_story_links",
            params={"issue_id": self.db._eq_filter(issue_id)},
            prefer="return=minimal",
        )
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
            prefer="resolution=merge-duplicates,return=minimal",
        )
