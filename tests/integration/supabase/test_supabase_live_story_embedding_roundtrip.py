from __future__ import annotations

import os
from datetime import UTC, datetime
from uuid import uuid4

import pytest  # pyright: ignore[reportMissingImports]

from core.domain.contracts import StoryLifecycleStatus, StoryRecord
from core.infrastructure.db_supabase import (
    SupabaseDatabase,
    SupabaseStoryEmbeddingStore,
    SupabaseStoryRepository,
)


def _require_live_http_env() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_TEST_URL", "").strip()
    key = os.environ.get("SUPABASE_TEST_SERVICE_ROLE", "").strip()
    if not url or not key:
        pytest.skip("SUPABASE_TEST_URL/SUPABASE_TEST_SERVICE_ROLE are not configured.")
    return url, key


def test_story_embedding_write_roundtrip_via_supabase_http() -> None:
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
    embedding_store = SupabaseStoryEmbeddingStore(db)

    now = datetime.now(UTC)
    story_id = f"story-{uuid4()}"
    source_checksum = f"checksum-{uuid4()}"

    story_repo.save_story(
        StoryRecord(
            story_id=story_id,
            schema_version="m2.story_intake_envelope.v1",
            narrative_original_text="Embedding contract story text",
            submitter_external_user_id="tc-p0-02-user",
            submitter_identity_issuer="tc-p0-02",
            lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
            created_at=now,
            updated_at=now,
            narrative_language="en",
            narrative_title_hint="Embedding contract title",
            narrative_canonical_type="infrastructure",
            narrative_canonical_labels=("lighting",),
            origin_source="tc_p0_02_live_contract",
        )
    )

    embedding_store.save_story_embedding(
        story_id=story_id,
        model_name="deterministic-baseline-v1",
        embedding_vector=(0.11, 0.22, 0.33),
        source_checksum=source_checksum,
        embedding_policy_version="m2.story_embedding_policy.v1",
    )

    rows = db._request(
        method="GET",
        path="/rest/v1/story_embeddings",
        params={
            "select": "story_id,model_name,source_checksum,embedding_policy_version,embedding_vector_json",
            "story_id": db._eq_filter(story_id),
            "source_checksum": db._eq_filter(source_checksum),
            "limit": "1",
            "order": "created_at.desc",
        },
    )

    assert rows
    row = rows[0]
    assert row["story_id"] == story_id
    assert row["model_name"] == "deterministic-baseline-v1"
    assert row["source_checksum"] == source_checksum
    assert row["embedding_policy_version"] == "m2.story_embedding_policy.v1"
    assert row["embedding_vector_json"] == "[0.11, 0.22, 0.33]"
