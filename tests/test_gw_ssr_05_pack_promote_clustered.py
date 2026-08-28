"""GW-SSR-05 T03: pack promote + CLUSTERED after pack gate pass."""

from __future__ import annotations

from core.domain import StoryLifecycleStatus
from core.infrastructure.repositories import (
    InMemoryClusterMembershipStore,
    InMemoryStoryRepository,
)
from core.schema import pack_cluster_id
from tests.test_gw_ssr_04_schema_driven_cluster_lens import (
    GATEWAY_ROOT,
    _orchestrator,
    _pack_story,
)


def _cid(office_id: str) -> str:
    return pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=(office_id,),
    )


def test_two_pack_stories_stay_ready_below_min_size() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_pack_story("p1", office_id="station-42"))
    stories.save_story(_pack_story("p2", office_id="station-42"))
    orchestrator = _orchestrator(stories, store)
    created = orchestrator.process_all_pending()
    assert created == []
    assert store.get_cluster_members(_cid("station-42"), "police_station") == ["p1", "p2"]
    for sid in ("p1", "p2"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
        assert not row.narrative_canonical_type


def test_three_pack_stories_promote_without_civic_types() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    for sid in ("p1", "p2", "p3"):
        stories.save_story(_pack_story(sid, office_id="station-42"))
        row = stories.get_story(sid)
        assert row is not None
        assert row.narrative_canonical_type is None
        assert row.narrative_canonical_type not in {"complaint", "system_bug"}
    orchestrator = _orchestrator(stories, store)
    created = orchestrator.process_all_pending()
    assert len(created) == 1
    for sid in ("p1", "p2", "p3"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED
    assert store.get_cluster_members(_cid("station-42"), "police_station") == [
        "p1",
        "p2",
        "p3",
    ]
    # idempotent re-run: already CLUSTERED stories leave the ready pool
    created_again = orchestrator.process_all_pending()
    assert created_again == []


def test_process_story_returns_issue_id_only_after_pack_gate_pass() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_pack_story("p1", office_id="station-7"))
    stories.save_story(_pack_story("p2", office_id="station-7"))
    orchestrator = _orchestrator(stories, store)
    assert orchestrator.process_story("p1") is None
    assert orchestrator.process_story("p2") is None
    stories.save_story(_pack_story("p3", office_id="station-7"))
    issue_id = orchestrator.process_story("p3")
    assert issue_id is not None
    for sid in ("p1", "p2", "p3"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED


def test_pack_path_does_not_call_civic_readiness_score_for_cluster() -> None:
    text = (GATEWAY_ROOT / "src/core/application/cluster_orchestrator.py").read_text(
        encoding="utf-8"
    )
    promote_start = text.index("def _promote_pack_membership")
    next_fn = text.index("\n    def process_story")
    pack_fn = text[promote_start:next_fn]
    assert "readiness_score_for_cluster" not in pack_fn
    assert "_create_issue_for_cluster" not in pack_fn
    assert "gate_policy=gate_policy" in pack_fn


def test_cron_still_single_process_all_pending() -> None:
    text = (GATEWAY_ROOT / "src/core/scheduler/cluster_cron.py").read_text(encoding="utf-8")
    assert "process_all_pending" in text
    assert text.count("class ClusterCronJob") == 1
