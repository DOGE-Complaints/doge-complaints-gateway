from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.application.issue_create import IssueCreateCommand, IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine
from core.application.services import StoryIntakeService
from core.domain import StoryLifecycleStatus, StoryRecord
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteIssueCandidateStore
from core.infrastructure.repositories import InMemoryIdempotencyRepository, InMemoryStoryRepository
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import InMemoryIssueCandidateStore, InMemoryReviewAuditLogRepository


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_api_branch_generates_trace_id_when_header_absent(client: TestClient) -> None:
    response = client.post(
        "/intake/stories",
        json=intake_payload_simple(
            external_user_id="branch-user",
            original_text="Branch closure story",
            title_en="Branch title",
        ),
    )
    assert response.status_code == 202
    assert response.json()["trace_id"]


def test_application_branch_rejects_empty_cluster_id() -> None:
    issue_create = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=InMemoryStoryRepository()),
    )
    with pytest.raises(ValueError, match="cluster_id must be non-empty"):
        issue_create.create_issue(
            IssueCreateCommand(
                cluster_id="   ",
                story_ids=("s-1",),
                readiness_score=90,
                title="Some title",
            )
        )


def test_application_branch_rejects_empty_story_ids() -> None:
    issue_create = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=InMemoryStoryRepository()),
    )
    with pytest.raises(ValueError, match="story_ids must contain at least one story id"):
        issue_create.create_issue(
            IssueCreateCommand(
                cluster_id="cluster-1",
                story_ids=(),
                readiness_score=90,
                title="Some title",
            )
        )


def test_domain_branch_disallows_ready_for_profile_regression() -> None:
    story_repo = InMemoryStoryRepository()
    now = datetime.now(UTC)
    story_repo.save_story(
        make_story_record(
            story_id="story-ready",
            narrative_original_text="Ready story",
            submitter_external_user_id="u1",
            narrative_title=narrative_dict(en="Ready"),
        )
    )
    service = StoryIntakeService(
        repository=story_repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    with pytest.raises(ValueError, match="Cannot regress story lifecycle"):
        service.advance_story_readiness(story_id="story-ready", narrative_complete=False)


def test_infra_branch_sqlite_candidate_get_missing_returns_none() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    store = SqliteIssueCandidateStore(db)
    assert store.get("missing-candidate") is None


def test_domain_branch_inmemory_list_stories_returns_all_items() -> None:
    repo = InMemoryStoryRepository()
    now = datetime.now(UTC)
    repo.save_story(
        make_story_record(
            story_id="list-1",
            narrative_original_text="Story one",
            submitter_external_user_id="u1",
            narrative_title=narrative_dict(en="One"),
        )
    )
    repo.save_story(
        make_story_record(
            story_id="list-2",
            narrative_original_text="Story two",
            submitter_external_user_id="u2",
            lifecycle_status=StoryLifecycleStatus.PARTIAL_READY,
            narrative_title=narrative_dict(en="Two"),
        )
    )
    stories = repo.list_stories()
    assert {item.story_id for item in stories} == {"list-1", "list-2"}


def test_domain_branch_clustering_memberships_empty_input_returns_empty_mapping() -> None:
    engine = ClusteringEngine()
    assert engine.memberships(tuple()) == {}
