from __future__ import annotations

import os
from datetime import UTC, datetime
from uuid import uuid4

import pytest  # pyright: ignore[reportMissingImports]

from core.domain.contracts import StoryLifecycleStatus, StoryRecord
from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseStoryRepository


def _require_live_http_env() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_TEST_URL", "").strip()
    key = os.environ.get("SUPABASE_TEST_SERVICE_ROLE", "").strip()
    if not url or not key:
        pytest.skip("SUPABASE_TEST_URL/SUPABASE_TEST_SERVICE_ROLE are not configured.")
    return url, key


def test_story_write_read_roundtrip_via_supabase_http() -> None:
    supabase_url, service_role_key = _require_live_http_env()
    db = SupabaseDatabase.from_http(
        supabase_url=supabase_url,
        service_role_key=service_role_key,
    )
    if not db.required_stories_narrative_extension_columns_ready():
        pytest.skip(
            "Hosted stories schema missing narrative extension columns; apply "
            "supabase/migrations/20260511_1200_m2_02_stories_narrative_extensions.sql"
        )
    repo = SupabaseStoryRepository(db)
    now = datetime.now(UTC)
    story_id = f"story-{uuid4()}"

    record = StoryRecord(
        story_id=story_id,
        schema_version="m2.story_intake_envelope.v1",
        narrative_original_text="Roundtrip contract story text",
        submitter_external_user_id="tc-p0-01-user",
        submitter_identity_issuer="tc-p0-01",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        created_at=now,
        updated_at=now,
        narrative_language="en",
        narrative_title={"en": "Roundtrip title", "et": "", "ru": ""},
        narrative_canonical_type="infrastructure",
        narrative_canonical_labels=("lighting", "safety"),
        origin_source="tc_p0_01_live_contract",
        privacy_contains_pii=False,
        privacy_redaction_requested=False,
    )

    saved = repo.save_story(record)
    fetched = repo.get_story(story_id)
    missing = repo.get_story(f"missing-{uuid4()}")

    assert saved.story_id == story_id
    assert fetched is not None
    assert fetched.story_id == story_id
    assert fetched.narrative_original_text == record.narrative_original_text
    assert fetched.narrative_language == "en"
    assert fetched.narrative_title == {"en": "Roundtrip title", "et": "", "ru": ""}
    assert fetched.narrative_canonical_type == "infrastructure"
    assert fetched.narrative_canonical_labels == ("lighting", "safety")
    assert fetched.lifecycle_status == StoryLifecycleStatus.READY_FOR_PROFILE
    assert missing is None
