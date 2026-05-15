from __future__ import annotations

from core.application.issue_create import (
    IssueCreateCommand,
    IssueCreateService,
    StoryPromotionProjectionBridge,
)
from core.application.services import StoryIntakeService
from core.infrastructure.db_sqlite import (
    SqliteDatabase,
    SqliteIssueCandidateStore,
    SqliteIssueStoryLinkStore,
    SqliteReviewAuditLogRepository,
)
from core.infrastructure.repositories import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy


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
            "original_text": f"District road light failure report #{idx}.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Road light failure"},
            "description": {"et": "d", "ru": "d", "en": f"District road light failure report #{idx}."},
            "canonical_type": "complaint",
            "canonical_labels": ["roads", "broken_infrastructure", "safety"],
                },
            }
        )
    )
    return story.story_id


def test_sqlite_process_linkage_persists_candidate_audit_and_issue_story_links() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    candidate_store = SqliteIssueCandidateStore(db)
    audit_store = SqliteReviewAuditLogRepository(db)
    link_store = SqliteIssueStoryLinkStore(db)

    story_repo = InMemoryStoryRepository()
    story_a = _create_story(story_repo, 1)
    story_b = _create_story(story_repo, 2)

    promotion = IssuePromotionService(
        candidates=candidate_store,
        audit_log=audit_store,
        gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
    )
    create_service = IssueCreateService(
        promotion_service=promotion,
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=story_repo),
        issue_story_link_store=link_store,
    )

    result = create_service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:demo:123",
            story_ids=(story_a, story_b),
            readiness_score=95,
            title="Road light failure in district",
        )
    )

    candidate = candidate_store.get(result.issue_id)
    assert candidate is not None
    assert candidate.status.value == "promoted"
    assert candidate.cluster_id == "cluster:demo:123"
    assert candidate.story_ids == (story_a, story_b)

    audit = audit_store.list_for_candidate(result.issue_id)
    assert len(audit) == 1
    assert audit[0].decision.value == "approve"

    rows = db.connection.execute(
        "SELECT issue_id, cluster_id, story_id FROM issue_story_links WHERE issue_id = ? ORDER BY story_id ASC",
        (result.issue_id,),
    ).fetchall()
    assert len(rows) == 2
    assert {str(row["story_id"]) for row in rows} == {story_a, story_b}
