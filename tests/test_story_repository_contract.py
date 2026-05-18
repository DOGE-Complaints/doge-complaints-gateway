from __future__ import annotations

from collections.abc import Callable

import pytest

from core.domain import StoryGeoSnapshot, StoryLifecycleStatus
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteStoryRepository
from core.infrastructure.repositories import InMemoryStoryRepository
from tests.intake_v2_fixtures import make_story_record, narrative_dict

RepoFactory = Callable[[], InMemoryStoryRepository | SqliteStoryRepository]


def _in_memory_factory() -> InMemoryStoryRepository:
    return InMemoryStoryRepository()


def _sqlite_factory() -> SqliteStoryRepository:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    return SqliteStoryRepository(db)


@pytest.mark.parametrize("repo_factory", [_in_memory_factory, _sqlite_factory])
def test_save_get_roundtrip_preserves_all_fields(repo_factory: RepoFactory) -> None:
    """REQ-39 D-01: save→get preserves StoryRecord fields (InMemory + SQLite)."""
    repo = repo_factory()
    geo = StoryGeoSnapshot(
        normalized_label="kalamaja",
        latitude=59.44,
        longitude=24.73,
        confidence=0.9,
        provider="test",
        cluster_tags=("tallinn",),
        admin_district="Kesklinn",
    )
    original = make_story_record(
        story_id="contract-roundtrip-1",
        narrative_original_text="Full field roundtrip text.",
        narrative_language="et",
        narrative_title=narrative_dict(et="Pealkiri", ru="Заголовок", en="Title"),
        narrative_description=narrative_dict(et="Kirjeldus", ru="Описание", en="Description"),
        narrative_canonical_type="infrastructure",
        narrative_canonical_labels=("lighting", "roads"),
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        geo=geo,
        origin_source="contract_test",
        origin_conversation_id="conv-1",
        privacy_contains_pii=True,
        privacy_redaction_requested=True,
    )
    repo.save_story(original)
    loaded = repo.get_story(original.story_id)
    assert loaded is not None
    assert loaded.story_id == original.story_id
    assert loaded.narrative_original_text == original.narrative_original_text
    assert loaded.narrative_language == original.narrative_language
    assert loaded.narrative_title == original.narrative_title
    assert loaded.narrative_canonical_type == original.narrative_canonical_type
    assert loaded.narrative_canonical_labels == original.narrative_canonical_labels
    assert loaded.lifecycle_status == original.lifecycle_status
    assert loaded.geo == original.geo
    assert loaded.origin_source == original.origin_source
    assert loaded.privacy_contains_pii == original.privacy_contains_pii


@pytest.mark.parametrize("repo_factory", [_in_memory_factory, _sqlite_factory])
def test_list_ready_for_clustering_filters_correctly(repo_factory: RepoFactory) -> None:
    """REQ-39 D-02: only READY_FOR_PROFILE stories are listed."""
    repo = repo_factory()
    ready = make_story_record(
        story_id="ready-1", lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE
    )
    partial = make_story_record(
        story_id="partial-1", lifecycle_status=StoryLifecycleStatus.PARTIAL_READY
    )
    accepted = make_story_record(
        story_id="accepted-1", lifecycle_status=StoryLifecycleStatus.ACCEPTED
    )
    for record in (ready, partial, accepted):
        repo.save_story(record)
    result = repo.list_stories_ready_for_clustering()
    ids = {s.story_id for s in result}
    assert ready.story_id in ids
    assert partial.story_id not in ids
    assert accepted.story_id not in ids


def test_update_lifecycle_unknown_story_raises_in_memory() -> None:
    """REQ-39 D-03: InMemoryStoryRepository raises ValueError for unknown id."""
    repo = _in_memory_factory()
    with pytest.raises(ValueError, match="Unknown story_id"):
        repo.update_lifecycle_status("nonexistent", StoryLifecycleStatus.READY_FOR_PROFILE)


def test_update_lifecycle_unknown_story_sqlite_is_noop() -> None:
    """REQ-39 D-03 note: SqliteStoryRepository does not raise on missing story_id (no row updated)."""
    repo = _sqlite_factory()
    repo.update_lifecycle_status("nonexistent", StoryLifecycleStatus.READY_FOR_PROFILE)
    assert repo.get_story("nonexistent") is None


@pytest.mark.parametrize("repo_factory", [_in_memory_factory, _sqlite_factory])
def test_double_save_is_idempotent(repo_factory: RepoFactory) -> None:
    """REQ-39 D-04: duplicate save does not create duplicate rows."""
    repo = repo_factory()
    record = make_story_record(story_id="idem-save-1")
    repo.save_story(record)
    repo.save_story(record)
    all_stories = repo.list_stories()
    assert len([s for s in all_stories if s.story_id == record.story_id]) == 1
