"""Tests for GW-L10N-01/GW-L10N-02 backfill script (audit G1)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from core.application.issue_create import DERIVATION_POLICY_VERSION
from core.infrastructure.db_sqlite import (
    SqliteDatabase,
    SqliteIssueProjectionStore,
    SqliteIssueStoryLinkStore,
    SqliteStoryRepository,
)
from core.projection import DOGEIssueStatus
from tests.intake_v2_fixtures import make_story_record, narrative_dict

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

_SCRIPT_PATH = _ROOT / "scripts" / "reproject_issue_i18n.py"
_spec = importlib.util.spec_from_file_location("reproject_issue_i18n", _SCRIPT_PATH)
assert _spec and _spec.loader
_reproject = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _reproject
_spec.loader.exec_module(_reproject)
run_reproject = _reproject.run_reproject


def _flat_title_payload(*, issue_id: str, issue_type: str = "complaint") -> dict[str, object]:
    same = "Identical flat title"
    return {
        "id": issue_id,
        "status": DOGEIssueStatus.PUBLISHED.value,
        "type": issue_type,
        "labels": ["infrastructure"],
        "title": {"et": same, "ru": same, "en": same},
        "summary": {"et": same, "ru": same, "en": same},
        "description": {"et": same, "ru": same, "en": same},
    }


@pytest.fixture()
def sqlite_reproject_stores() -> tuple[
    SqliteStoryRepository,
    SqliteIssueProjectionStore,
    SqliteIssueStoryLinkStore,
]:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    return (
        SqliteStoryRepository(db),
        SqliteIssueProjectionStore(db),
        SqliteIssueStoryLinkStore(db),
    )


def test_reproject_dry_run_does_not_mutate_payload(
    sqlite_reproject_stores: tuple[
        SqliteStoryRepository,
        SqliteIssueProjectionStore,
        SqliteIssueStoryLinkStore,
    ],
) -> None:
    story_repo, projection_store, link_store = sqlite_reproject_stores
    issue_id = "issue-dry-run-1"
    dominant = make_story_record(
        story_id="story-dominant-1",
        narrative_title=narrative_dict(et="ET title", ru="RU title", en="EN title"),
        narrative_canonical_labels=("roads", "safety", "broken_infrastructure"),
    )
    story_repo.save_story(dominant)
    flat_payload = _flat_title_payload(issue_id=issue_id)
    projection_store.save_projection(
        issue_id=issue_id,
        status=DOGEIssueStatus.PUBLISHED.value,
        payload=flat_payload,
        policy_version=DERIVATION_POLICY_VERSION,
    )
    link_store.save_issue_story_links(
        issue_id=issue_id,
        cluster_id="cluster:1",
        story_ids=(dominant.story_id,),
    )

    before = projection_store.get_projection(issue_id)
    updated, skipped = run_reproject(
        projection_store=projection_store,
        link_store=link_store,
        story_repository=story_repo,
        dry_run=True,
    )
    after = projection_store.get_projection(issue_id)

    assert updated == 1
    assert skipped == 0
    assert before == after


def test_reproject_write_updates_per_locale_title_from_dominant_story(
    sqlite_reproject_stores: tuple[
        SqliteStoryRepository,
        SqliteIssueProjectionStore,
        SqliteIssueStoryLinkStore,
    ],
) -> None:
    story_repo, projection_store, link_store = sqlite_reproject_stores
    issue_id = "issue-write-1"
    dominant = make_story_record(
        story_id="story-rich",
        narrative_title=narrative_dict(et="ET rich", ru="RU rich", en="EN rich"),
        narrative_canonical_labels=("roads", "safety", "broken_infrastructure"),
    )
    sparse = make_story_record(
        story_id="story-sparse",
        narrative_title=narrative_dict(et="t", ru="t", en="t"),
        narrative_canonical_labels=("roads",),
    )
    story_repo.save_story(dominant)
    story_repo.save_story(sparse)
    projection_store.save_projection(
        issue_id=issue_id,
        status=DOGEIssueStatus.PUBLISHED.value,
        payload=_flat_title_payload(issue_id=issue_id, issue_type="observation"),
        policy_version=DERIVATION_POLICY_VERSION,
    )
    link_store.save_issue_story_links(
        issue_id=issue_id,
        cluster_id="cluster:1",
        story_ids=(sparse.story_id, dominant.story_id),
    )

    run_reproject(
        projection_store=projection_store,
        link_store=link_store,
        story_repository=story_repo,
        dry_run=False,
    )
    saved = projection_store.get_projection(issue_id)
    assert saved is not None
    title = saved["title"]
    assert isinstance(title, dict)
    assert title["et"] == "ET rich"
    assert title["en"] == "EN rich"
    assert title["et"] != title["en"]
    assert saved["type"] == "observation"


def test_reproject_write_sets_original_locale_from_cluster_stories(
    sqlite_reproject_stores: tuple[
        SqliteStoryRepository,
        SqliteIssueProjectionStore,
        SqliteIssueStoryLinkStore,
    ],
) -> None:
    story_repo, projection_store, link_store = sqlite_reproject_stores
    issue_id = "issue-original-locale-1"
    et_story = make_story_record(
        story_id="story-et-reproject",
        narrative_language="et",
        narrative_title=narrative_dict(et="ET reproject"),
        narrative_canonical_labels=("roads",),
    )
    ru_story = make_story_record(
        story_id="story-ru-reproject",
        narrative_language="ru",
        narrative_title=narrative_dict(ru="RU reproject"),
        narrative_canonical_labels=("roads",),
    )
    story_repo.save_story(et_story)
    story_repo.save_story(ru_story)
    projection_store.save_projection(
        issue_id=issue_id,
        status=DOGEIssueStatus.PUBLISHED.value,
        payload=_flat_title_payload(issue_id=issue_id),
        policy_version=DERIVATION_POLICY_VERSION,
    )
    link_store.save_issue_story_links(
        issue_id=issue_id,
        cluster_id="cluster:original-locale",
        story_ids=(ru_story.story_id, et_story.story_id),
    )

    run_reproject(
        projection_store=projection_store,
        link_store=link_store,
        story_repository=story_repo,
        dry_run=False,
    )
    saved = projection_store.get_projection(issue_id)
    assert saved is not None
    assert saved.get("original_locale") == ["et", "ru"]


def test_reproject_write_is_idempotent(
    sqlite_reproject_stores: tuple[
        SqliteStoryRepository,
        SqliteIssueProjectionStore,
        SqliteIssueStoryLinkStore,
    ],
) -> None:
    story_repo, projection_store, link_store = sqlite_reproject_stores
    issue_id = "issue-idempotent-1"
    dominant = make_story_record(
        story_id="story-idem",
        narrative_title=narrative_dict(et="ET", ru="RU", en="EN"),
    )
    story_repo.save_story(dominant)
    projection_store.save_projection(
        issue_id=issue_id,
        status=DOGEIssueStatus.PUBLISHED.value,
        payload=_flat_title_payload(issue_id=issue_id),
        policy_version=DERIVATION_POLICY_VERSION,
    )
    link_store.save_issue_story_links(
        issue_id=issue_id,
        cluster_id="cluster:1",
        story_ids=(dominant.story_id,),
    )

    run_reproject(
        projection_store=projection_store,
        link_store=link_store,
        story_repository=story_repo,
        dry_run=False,
    )
    first = projection_store.get_projection(issue_id)
    run_reproject(
        projection_store=projection_store,
        link_store=link_store,
        story_repository=story_repo,
        dry_run=False,
    )
    second = projection_store.get_projection(issue_id)
    assert first == second
