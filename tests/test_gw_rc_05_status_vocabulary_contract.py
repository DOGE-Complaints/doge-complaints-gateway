"""STORY-GW-RC-05 acceptance: write board-vocab + real create→extend pipeline contract."""

from __future__ import annotations

from core.application.issue_create import (
    IssueCreateCommand,
    IssueCreateService,
    StoryPromotionProjectionBridge,
)
from core.application.services import StoryIntakeService
from core.infrastructure.repositories import (
    InMemoryIdempotencyRepository,
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryRepository,
)
from core.intake import INTAKE_SCHEMA_VERSION, parse_story_intake_request
from core.projection import IssueProjectionService
from core.projection.enums import DOGEIssueStatus
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)

_VALID_STATUSES = frozenset(status.value for status in DOGEIssueStatus)


def _create_story(repo: InMemoryStoryRepository, idx: int) -> str:
    intake = StoryIntakeService(
        repository=repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )
    story = intake.create_story(
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {
                    "external_user_id": f"user-{idx}",
                    "identity_issuer": "https://idp.example.com/eid",
                },
                "narrative": {
                    "original_text": f"District lights outage report #{idx}.",
                    "language": "en",
                    "session_language": "en",
                    "title": {"et": "t", "ru": "t", "en": "District lights outage"},
                    "description": {
                        "et": "d",
                        "ru": "d",
                        "en": f"District lights outage report #{idx}.",
                    },
                    "canonical_type": "complaint",
                    "canonical_labels": ["roads", "broken_infrastructure", "safety"],
                },
            }
        )
    )
    return story.story.story_id


def _build_service(
    stories: InMemoryStoryRepository | None = None,
) -> tuple[
    IssueCreateService,
    InMemoryIssueProjectionStore,
    InMemoryIssueCandidateStore,
]:
    story_repo = stories or InMemoryStoryRepository()
    candidate_store = InMemoryIssueCandidateStore()
    projection_store = InMemoryIssueProjectionStore()
    service = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=candidate_store,
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=story_repo),
        issue_projection_store=projection_store,
        issue_story_link_store=InMemoryIssueStoryLinkStore(),
    )
    return service, projection_store, candidate_store


def test_create_then_extend_writes_board_status_not_candidate_promoted() -> None:
    stories = InMemoryStoryRepository()
    story_1 = _create_story(stories, 1)
    story_2 = _create_story(stories, 2)
    story_3 = _create_story(stories, 3)
    service, projection_store, candidate_store = _build_service(stories)

    first = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:gw-rc-05:1",
            story_ids=(story_1, story_2),
            readiness_score=81,
            title="GW-RC-05 living cluster issue",
        )
    )
    assert projection_store._rows is not None
    assert projection_store._rows[first.issue_id]["status"] == "PUBLISHED"

    second = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:gw-rc-05:1",
            story_ids=(story_2, story_3),
            readiness_score=90,
            title="GW-RC-05 living cluster issue",
        )
    )
    assert second.issue_id == first.issue_id
    assert projection_store._rows[second.issue_id]["status"] == "PUBLISHED"
    assert projection_store._rows[second.issue_id]["status"] != "promoted"

    candidate = candidate_store.get(first.issue_id)
    assert candidate is not None
    assert candidate.status.value == "promoted"

    listed = projection_store.list_projections()
    issue = next(item for item in listed if item["id"] == first.issue_id)
    assert issue["status"] in _VALID_STATUSES
    assert issue["status"] == "PUBLISHED"


def test_read_path_canonicalizes_legacy_promoted_storage_row() -> None:
    projection_store = InMemoryIssueProjectionStore()
    projection_store.save_projection(
        issue_id="gw-rc-05-legacy-promoted-row",
        status="promoted",
        payload={
            "type": "IMPROVEMENT",
            "labels": ["infra"],
            "title": {"et": "t", "ru": "t", "en": "t"},
            "summary": {"et": "s", "ru": "s", "en": "s"},
            "description": {"et": "d", "ru": "d", "en": "d"},
        },
        policy_version="m3.doge_issue_derivation.v1",
    )
    fetched = projection_store.get_projection("gw-rc-05-legacy-promoted-row")
    assert fetched is not None
    assert fetched["status"] == "PUBLISHED"
    assert fetched["status"] in _VALID_STATUSES
