from __future__ import annotations

import logging
from datetime import UTC, datetime

import pytest

from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict

from core.domain import StoryLifecycleStatus, StoryRecord
from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseStoryRepository


class _BrokenClient:
    def __enter__(self) -> "_BrokenClient":
        return self

    def __exit__(self, _exc_type: object, _exc: object, _tb: object) -> None:
        return None

    def request(self, **_kwargs: object) -> object:
        raise RuntimeError("transport down")


def test_supabase_request_failed_event_emitted(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    db = SupabaseDatabase(
        base_url="https://example.supabase.co",
        service_role_key="secret",
    )
    monkeypatch.setattr(db, "_client", lambda: _BrokenClient())
    with caplog.at_level(logging.ERROR, logger="core.infrastructure.db_supabase"):
        with pytest.raises(RuntimeError, match="transport down"):
            db._request(method="GET", path="/rest/v1/stories")
    failed = [r for r in caplog.records if r.getMessage() == "supabase.request_failed"]
    assert failed
    record = failed[-1]
    assert getattr(record, "method", None) == "GET"
    assert getattr(record, "path", None) == "/rest/v1/stories"
    assert getattr(record, "outcome", None) == "error"


def test_supabase_repo_save_story_failed_event_emitted(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    db = SupabaseDatabase(
        base_url="https://example.supabase.co",
        service_role_key="secret",
    )
    repository = SupabaseStoryRepository(db)
    now = datetime.now(UTC)
    record = StoryRecord(
        story_id="story-1",
        schema_version="m2.story_intake.v1",
        narrative_original_text="Broken traffic light",
        submitter_external_user_id="user-1",
        submitter_identity_issuer="https://idp.example.com/eid",
        lifecycle_status=StoryLifecycleStatus.ACCEPTED,
        created_at=now,
        updated_at=now,
        narrative_language="en",
        narrative_title=narrative_dict(en="Traffic light issue"),
        narrative_canonical_type="infrastructure",
        narrative_canonical_labels=("traffic",),
        geo=None,
        origin_source=None,
        origin_conversation_id=None,
        origin_tool_call_id=None,
        privacy_contains_pii=False,
        privacy_redaction_requested=False,
    )

    def _broken_request(**_kwargs: object) -> object:
        raise RuntimeError("repo transport down")

    monkeypatch.setattr(db, "_request", _broken_request)
    with caplog.at_level(logging.ERROR, logger="core.infrastructure.db_supabase"):
        with pytest.raises(RuntimeError, match="repo transport down"):
            repository.save_story(record)

    failed = [r for r in caplog.records if r.getMessage() == "repo.supabase.save_story_failed"]
    assert failed
    failure_record = failed[-1]
    assert getattr(failure_record, "story_id", None) == "story-1"
    assert getattr(failure_record, "backend", None) == "supabase"
    assert getattr(failure_record, "outcome", None) == "error"
