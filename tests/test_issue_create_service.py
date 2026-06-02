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
from core.intake import INTAKE_SCHEMA_VERSION
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)


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
                "submitter": {"external_user_id": f"user-{idx}", "identity_issuer": "https://idp.example.com/eid"},
                "narrative": {
            "original_text": f"District lights outage report #{idx}.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "District lights outage"},
            "description": {"et": "d", "ru": "d", "en": f"District lights outage report #{idx}."},
            "canonical_type": "complaint",
            "canonical_labels": ["roads", "broken_infrastructure", "safety"],
                },
            }
        )
    )
    return story.story.story_id


def test_issue_create_service_create_then_extend_reuses_issue_id() -> None:
    stories = InMemoryStoryRepository()
    story_1 = _create_story(stories, 1)
    story_2 = _create_story(stories, 2)
    story_3 = _create_story(stories, 3)
    candidate_store = InMemoryIssueCandidateStore()
    audit_store = InMemoryReviewAuditLogRepository()
    projection_store = InMemoryIssueProjectionStore()
    link_store = InMemoryIssueStoryLinkStore()
    service = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=candidate_store,
            audit_log=audit_store,
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
        issue_projection_store=projection_store,
        issue_story_link_store=link_store,
    )

    first = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:living:1",
            story_ids=(story_1, story_2),
            readiness_score=81,
            title="Living cluster issue",
        )
    )
    second = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:living:1",
            story_ids=(story_2, story_3),
            readiness_score=90,
            title="Living cluster issue",
        )
    )

    assert first.issue_id == second.issue_id
    first_description = first.projection["description"]["en"]
    second_description = second.projection["description"]["en"]
    promoted = candidate_store.get(first.issue_id)
    assert promoted is not None
    assert promoted.story_ids == tuple(sorted((story_1, story_2, story_3)))
    assert promoted.readiness_score == 90
    assert second_description != first_description
    assert "report #3" in second_description
    assert link_store._rows is not None
    assert set(link_store._rows[first.issue_id][1]) == {story_1, story_2, story_3}
    audit = audit_store.list_for_candidate(first.issue_id)
    assert [entry.rationale for entry in audit] == [
        "http_create_issue_auto_promote",
        "cluster_growth_extend",
    ]


def test_issue_create_service_idempotent_extend_when_no_new_stories() -> None:
    stories = InMemoryStoryRepository()
    story_1 = _create_story(stories, 1)
    story_2 = _create_story(stories, 2)
    candidate_store = InMemoryIssueCandidateStore()
    audit_store = InMemoryReviewAuditLogRepository()
    service = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=candidate_store,
            audit_log=audit_store,
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
    )

    created = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:living:idempotent",
            story_ids=(story_1, story_2),
            readiness_score=70,
            title="Idempotent living issue",
        )
    )
    repeated = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:living:idempotent",
            story_ids=(story_1, story_2),
            readiness_score=99,
            title="Idempotent living issue",
        )
    )

    assert created.issue_id == repeated.issue_id
    promoted = candidate_store.get(created.issue_id)
    assert promoted is not None
    assert promoted.story_ids == (story_1, story_2)
    assert promoted.readiness_score == 70
    audit = audit_store.list_for_candidate(created.issue_id)
    assert len(audit) == 1
