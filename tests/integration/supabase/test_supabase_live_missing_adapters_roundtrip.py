from __future__ import annotations

import os
from datetime import UTC, datetime
from uuid import uuid4

import pytest  # pyright: ignore[reportMissingImports]

from core.domain.contracts import IdempotencyRecord, StoryLifecycleStatus, StoryRecord
from core.infrastructure.db_supabase import (
    SupabaseDatabase,
    SupabaseIdempotencyRepository,
    SupabaseIssueCandidateStore,
    SupabaseIssueProjectionEmbeddingStore,
    SupabaseIssueProjectionStore,
    SupabaseIssueStoryLinkStore,
    SupabaseReviewAuditLogRepository,
    SupabaseStoryRepository,
)
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus, ReviewAuditEntry, ReviewDecision


def _require_live_http_env() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_TEST_URL", "").strip()
    key = os.environ.get("SUPABASE_TEST_SERVICE_ROLE", "").strip()
    if not url or not key:
        pytest.skip("SUPABASE_TEST_URL/SUPABASE_TEST_SERVICE_ROLE are not configured.")
    return url, key


def test_supabase_missing_adapters_live_roundtrip() -> None:
    supabase_url, service_role_key = _require_live_http_env()
    db = SupabaseDatabase.from_http(
        supabase_url=supabase_url,
        service_role_key=service_role_key,
    )
    if not db.required_stories_narrative_extension_columns_ready():
        pytest.skip(
            "Stories narrative extension migration not applied; see "
            "supabase/migrations/20260511_1200_m2_02_stories_narrative_extensions.sql"
        )
    story_repo = SupabaseStoryRepository(db)
    idempotency_repo = SupabaseIdempotencyRepository(db)
    candidate_store = SupabaseIssueCandidateStore(db)
    audit_store = SupabaseReviewAuditLogRepository(db)
    link_store = SupabaseIssueStoryLinkStore(db)
    projection_store = SupabaseIssueProjectionStore(db)
    projection_embedding_store = SupabaseIssueProjectionEmbeddingStore(db)

    now = datetime.now(UTC)
    story_id = f"story-{uuid4()}"
    story_repo.save_story(
        StoryRecord(
            story_id=story_id,
            schema_version="m2.story_intake_envelope.v1",
            narrative_original_text="Supabase missing adapters roundtrip story",
            submitter_external_user_id="tc100-h-01-user",
            submitter_identity_issuer="tc100-h-01",
            lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
            created_at=now,
            updated_at=now,
            narrative_language="en",
            narrative_title_hint="TC100 H01 story",
            narrative_canonical_type="infrastructure",
            narrative_canonical_labels=("lighting",),
        )
    )

    idem_key = f"idem-{uuid4()}"
    idempotency_repo.save(
        IdempotencyRecord(
            key=idem_key,
            story_id=story_id,
            created_at=now,
        )
    )
    idem_row = idempotency_repo.get_by_key(idem_key)
    assert idem_row is not None
    assert idem_row.story_id == story_id

    candidate_id = f"candidate-{uuid4()}"
    candidate = IssueCandidateRecord(
        candidate_id=candidate_id,
        status=IssueCandidateStatus.IN_REVIEW,
        cluster_id="cluster:tc100:h01",
        story_ids=(story_id,),
        readiness_score=92,
        title="TC100 candidate",
    )
    candidate_store.save(candidate)
    loaded_candidate = candidate_store.get(candidate_id)
    assert loaded_candidate is not None
    assert loaded_candidate.status == IssueCandidateStatus.IN_REVIEW

    audit_entry = ReviewAuditEntry(
        candidate_id=candidate_id,
        actor="tc100",
        decision=ReviewDecision.APPROVE,
        rationale="live-roundtrip",
        related_cluster_id="cluster:tc100:h01",
        related_story_ids=(story_id,),
    )
    audit_store.append(audit_entry)
    audit_rows = audit_store.list_for_candidate(candidate_id)
    assert audit_rows
    assert audit_rows[-1].decision == ReviewDecision.APPROVE

    issue_id = f"issue-{uuid4()}"
    link_store.save_issue_story_links(
        issue_id=issue_id,
        cluster_id="cluster:tc100:h01",
        story_ids=(story_id,),
    )
    link_rows = db._request(
        method="GET",
        path="/rest/v1/issue_story_links",
        params={
            "select": "issue_id,story_id,cluster_id",
            "issue_id": db._eq_filter(issue_id),
            "limit": "1",
        },
    )
    assert link_rows
    assert link_rows[0]["story_id"] == story_id

    projection_store.save_projection(
        issue_id=issue_id,
        status="promoted",
        policy_version="m3.doge_issue_derivation.v1",
        payload={
            "type": "improvement",
            "title": {"en": "Issue title", "et": "Pealkiri", "ru": "Заголовок"},
            "summary": {"en": "Issue summary", "et": "Kokkuvote", "ru": "Сводка"},
            "description": {"en": "Issue description", "et": "Kirjeldus", "ru": "Описание"},
            "labels": ["district"],
        },
    )
    projection_embedding_store.save_projection_embedding(
        issue_id=issue_id,
        model_name="deterministic-baseline-v1",
        embedding_vector=(0.1, 0.2, 0.3),
        source_checksum=f"checksum-{uuid4()}",
        embedding_policy_version="m3.doge_issue_embedding_policy.v1",
    )
    projection_embedding_rows = db._request(
        method="GET",
        path="/rest/v1/doge_issue_embeddings",
        params={
            "select": "issue_id,embedding_policy_version",
            "issue_id": db._eq_filter(issue_id),
            "limit": "1",
            "order": "created_at.desc",
        },
    )
    assert projection_embedding_rows
    assert projection_embedding_rows[0]["embedding_policy_version"] == "m3.doge_issue_embedding_policy.v1"

    candidate_store.delete(candidate_id)
    assert candidate_store.get(candidate_id) is None
