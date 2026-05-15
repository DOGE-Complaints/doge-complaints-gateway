from __future__ import annotations

from core.application.issue_create import (
    IssueCreateCommand,
    IssueCreateService,
    StoryPromotionProjectionBridge,
)
from core.application.services import StoryIntakeService
from core.infrastructure.repositories import (
    InMemoryIdempotencyRepository,
    InMemoryIssueProjectionEmbeddingStore,
    InMemoryStoryEmbeddingStore,
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


def _intake_payload(*, text: str, title_hint: str, user_id: str) -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": user_id, "identity_issuer": "https://idp.example.com/eid"},
        "narrative": {
            "original_text": text,
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": title_hint},
            "description": {"et": "d", "ru": "d", "en": text},
        },
    }


def test_story_embedding_uses_policy_version_and_canonical_source() -> None:
    repo = InMemoryStoryRepository()
    embedding_store = InMemoryStoryEmbeddingStore()
    intake = StoryIntakeService(
        repository=repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
        story_embedding_store=embedding_store,
    )
    intake.create_story(
        parse_story_intake_request(
            _intake_payload(
                text="Street light outage in district A.",
                title_hint="Street light outage",
                user_id="u-1",
            )
        )
    )
    intake.create_story(
        parse_story_intake_request(
            _intake_payload(
                text="Street light outage in district A.",
                title_hint="Public safety outage",
                user_id="u-2",
            )
        )
    )

    assert embedding_store._rows is not None
    assert len(embedding_store._rows) == 2
    first = embedding_store._rows[0]
    second = embedding_store._rows[1]
    assert first["embedding_policy_version"] == "m2.story_embedding_policy.v1"
    assert second["embedding_policy_version"] == "m2.story_embedding_policy.v1"
    assert first["source_checksum"] != second["source_checksum"]
    # TC-21: direct output fields for save_story_embedding path
    assert first["model_name"] == "deterministic-baseline-v1"
    assert second["model_name"] == "deterministic-baseline-v1"
    assert first["story_id"] is not None
    assert second["story_id"] is not None
    assert first["story_id"] != second["story_id"]


def test_issue_embedding_persists_policy_version() -> None:
    repo = InMemoryStoryRepository()
    intake = StoryIntakeService(
        repository=repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )
    s1 = intake.create_story(
        parse_story_intake_request(
            _intake_payload(
                text="Road and safety incident near bridge.",
                title_hint="Road safety incident",
                user_id="u-10",
            )
        )
    )
    s2 = intake.create_story(
        parse_story_intake_request(
            _intake_payload(
                text="Road and safety incident near bridge, repeated.",
                title_hint="Road safety incident",
                user_id="u-11",
            )
        )
    )

    embedding_store = InMemoryIssueProjectionEmbeddingStore()
    service = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=repo),
        issue_projection_embedding_store=embedding_store,
    )
    service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:test:1",
            story_ids=(s1.story_id, s2.story_id),
            readiness_score=90,
            title="Road safety incident",
        )
    )

    assert embedding_store._rows is not None
    assert embedding_store._rows
    row = embedding_store._rows[0]
    assert row["embedding_policy_version"] == "m3.doge_issue_embedding_policy.v1"
