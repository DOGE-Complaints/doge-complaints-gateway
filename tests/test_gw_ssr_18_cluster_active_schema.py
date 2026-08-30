"""GW-SSR-18: pack/dual iff persist binding == NODE_SCHEMA_*; mismatch skip."""

from __future__ import annotations

import logging
from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.cluster import ClusterLens
from core.domain import StoryLifecycleStatus
from core.infrastructure.repositories import (
    InMemoryClusterMembershipStore,
    InMemoryStoryRepository,
)
from core.schema import pack_cluster_id
from tests.test_gw_ssr_04_schema_driven_cluster_lens import (
    CLUSTERLENS_BASELINE,
    _civic_clustering,
    _civic_story,
    _engine,
    _issue_service,
    _orchestrator,
    _pack_story,
)


def test_clusterlens_still_ten_civic_members() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE


def test_mismatch_bound_skips_without_pack_membership(caplog: logging.LogCaptureFixture) -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_pack_story("p-foreign", office_id="station-42"))
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_clustering(),
        issue_create_service=_issue_service(stories),
        cluster_membership_store=store,
        schema_pack_engine=_engine(),
        node_schema_id="tallinn_civic",
        node_schema_version="v1",
    )
    caplog.set_level(logging.INFO, logger="core.application.cluster_orchestrator")
    assert orchestrator.process_story("p-foreign") is None
    cid = pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=("station-42",),
    )
    assert store.get_cluster_members(cid, "police_station") == []
    row = stories.get_story("p-foreign")
    assert row is not None
    assert row.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
    assert any(
        rec.message == "cluster.skipped_schema_mismatch" for rec in caplog.records
    )


def test_mismatch_bound_does_not_enter_civic_path() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_civic_story("c1"))
    stories.save_story(_civic_story("c2"))
    stories.save_story(_pack_story("p-foreign", office_id="station-99"))
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_clustering(),
        issue_create_service=_issue_service(stories),
        cluster_membership_store=store,
        schema_pack_engine=_engine(),
        node_schema_id="tallinn_civic",
        node_schema_version="v1",
    )
    created = orchestrator.process_all_pending()
    assert created
    foreign = stories.get_story("p-foreign")
    assert foreign is not None
    assert foreign.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
    cid = pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=("station-99",),
    )
    assert store.get_cluster_members(cid, "police_station") == []
    for sid in ("c1", "c2"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED


def test_match_active_pair_persists_pack_membership() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_pack_story("p1", office_id="station-42"))
    orchestrator = _orchestrator(stories, store)
    assert orchestrator.node_schema_id == "legal_process"
    assert orchestrator.process_story("p1") is None
    cid = pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=("station-42",),
    )
    assert store.get_cluster_members(cid, "police_station") == ["p1"]
    row = stories.get_story("p1")
    assert row is not None
    assert row.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE


def test_unbound_civic_ready_as_is() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_civic_story("c1"))
    stories.save_story(_civic_story("c2"))
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_clustering(),
        issue_create_service=_issue_service(stories),
        cluster_membership_store=store,
        schema_pack_engine=_engine(),
        node_schema_id="legal_process",
        node_schema_version="v1",
    )
    bound = _pack_story("p1", office_id="station-1")
    civic_ready = orchestrator._civic_ready(
        [stories.get_story("c1"), stories.get_story("c2"), bound]  # type: ignore[list-item]
    )
    assert {s.story_id for s in civic_ready} == {"c1", "c2"}
    created = orchestrator.process_all_pending()
    assert created
    for sid in ("c1", "c2"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED
