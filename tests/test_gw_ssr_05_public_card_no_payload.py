"""GW-SSR-05 T04: public Issue card has no structured_payload."""

from __future__ import annotations

from pathlib import Path

from core.application.issue_create import IssueCreateCommand
from core.domain import StoryLifecycleStatus
from core.infrastructure.repositories import (
    InMemoryClusterMembershipStore,
    InMemoryStoryRepository,
)
from core.projection.dto import DOGEIssue
from core.schema import pack_cluster_id
from tests.test_gw_ssr_04_schema_driven_cluster_lens import _orchestrator, _pack_story

GATEWAY_ROOT = Path(__file__).resolve().parents[1]


def test_dto_source_and_to_public_dict_omit_structured_payload() -> None:
    text = (GATEWAY_ROOT / "src/core/projection/dto.py").read_text(encoding="utf-8")
    assert "structured_payload" not in text
    issue = DOGEIssue(
        id="i1",
        status="open",
        type="complaint",
        labels=(),
        title={"en": "t", "et": "t", "ru": "t"},
        summary={"en": "s", "et": "s", "ru": "s"},
        description={"en": "d", "et": "d", "ru": "d"},
    )
    public = issue.to_public_dict()
    assert "structured_payload" not in public
    assert public["title"]["en"] == "t"
    assert "type" in public


def test_pack_promoted_issue_projection_uses_civic_narrative_not_payload() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    for sid in ("p1", "p2", "p3"):
        stories.save_story(_pack_story(sid, office_id="station-card"))
    orchestrator = _orchestrator(stories, store)
    created = orchestrator.process_all_pending()
    assert len(created) == 1
    cid = pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=("station-card",),
    )
    replay = orchestrator.issue_create_service.create_issue(
        IssueCreateCommand(
            cluster_id=cid,
            story_ids=("p1", "p2", "p3"),
            readiness_score=40,
            title="legal",
        )
    )
    assert "structured_payload" not in replay.projection
    assert "title" in replay.projection
    assert "description" in replay.projection
    for sid in ("p1", "p2", "p3"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED
        assert row.structured_payload is not None
