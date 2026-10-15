"""GW-REQ57-01: bind-in + sense-brief projection apply (stub payloads, no live LLM)."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.application.issue_create import (
    IssueCreateCommand,
    IssueCreateService,
    StoryPromotionProjectionBridge,
)
from core.application.sense_brief_bind import (
    IssueSenseBriefBindService,
    preserve_brief_wins_fields,
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
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from tests.civic_pack_overrides import monkeypatch_civic_knobs
from tests.intake_v2_fixtures import with_active_schema_binding

_TOKEN = "req57-test-service-token"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch_civic_knobs(monkeypatch, min_size=1, readiness_threshold=1)
    monkeypatch.setenv("SERVICE_API_TOKEN", _TOKEN)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _service_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {_TOKEN}"}


def _seed_issue(
    issue_id: str = "issue-req57-01",
    *,
    title_en: str = "Dominant story title",
) -> None:
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    store.save_projection(
        issue_id=issue_id,
        status="PUBLISHED",
        payload={
            "id": issue_id,
            "status": "PUBLISHED",
            "type": "INCIDENT",
            "labels": ["infrastructure"],
            "title": {"et": title_en, "ru": title_en, "en": title_en},
            "summary": {"et": "alpha", "ru": "alpha", "en": "alpha"},
            "description": {"et": "d", "ru": "d", "en": "d"},
            "generation_status": "pending",
            "generation_version": "v0",
        },
        policy_version="m3.doge_issue_derivation.v1",
    )


def test_req57_01_bind_requires_service_auth(client: TestClient) -> None:
    _seed_issue()
    response = client.post(
        "/v1/issue-sense-brief/bind",
        json={
            "issue_id": "issue-req57-01",
            "generation_version": "v1",
            "outcome": "success",
            "poster_url": "https://cdn.example/poster.png",
            "apply": {"title": "Brief title", "summary": {"en": "Brief summary"}},
        },
    )
    assert response.status_code == 401


def test_req57_01_success_bind_applies_title_summary_ready(
    client: TestClient,
) -> None:
    _seed_issue()
    response = client.post(
        "/v1/issue-sense-brief/bind",
        headers=_service_headers(),
        json={
            "issue_id": "issue-req57-01",
            "generation_version": "v1",
            "outcome": "success",
            "poster_url": "https://cdn.example/poster.png",
            "apply": {
                "title": "Civic brief title under eighty",
                "summary": {
                    "et": "Lühikokkuvõte",
                    "ru": "Краткое резюме",
                    "en": "Brief summary",
                },
            },
        },
    )
    assert response.status_code == 200, response.text
    issue = response.json()["data"]["issue"]
    assert issue["title"]["en"] == "Civic brief title under eighty"
    assert issue["summary"]["en"] == "Brief summary"
    assert issue["generation_status"] == "ready"
    assert issue["generation_version"] == "v1"
    assert issue["poster_url"] == "https://cdn.example/poster.png"
    assert issue["title"]["en"] != "Dominant story title"

    got = client.get("/node/issues/issue-req57-01")
    assert got.status_code == 200
    public = got.json()["data"]["issue"]
    assert public["generation_status"] == "ready"
    assert public["poster_url"] == "https://cdn.example/poster.png"
    assert "generation_reason_class" not in public


def test_req57_01_title_max_80(client: TestClient) -> None:
    _seed_issue()
    response = client.post(
        "/v1/issue-sense-brief/bind",
        headers=_service_headers(),
        json={
            "issue_id": "issue-req57-01",
            "generation_version": "v1",
            "outcome": "success",
            "poster_url": "https://cdn.example/p.png",
            "apply": {"title": "x" * 81, "summary": {"en": "s"}},
        },
    )
    assert response.status_code == 400


def test_req57_01_fail_bind_sets_failed_no_pretend(client: TestClient) -> None:
    _seed_issue()
    response = client.post(
        "/v1/issue-sense-brief/bind",
        headers=_service_headers(),
        json={
            "issue_id": "issue-req57-01",
            "generation_version": "v2",
            "outcome": "failure",
            "reason_class": "corpus_insufficient",
        },
    )
    assert response.status_code == 200, response.text
    issue = response.json()["data"]["issue"]
    assert issue["generation_status"] == "failed"
    assert issue["generation_version"] == "v2"
    assert "poster_url" not in issue
    assert issue["title"]["en"] == "[Brief unavailable]"
    assert issue["title"]["en"] != "Dominant story title"


def test_req57_01_fail_rejects_apply_body(client: TestClient) -> None:
    _seed_issue()
    response = client.post(
        "/v1/issue-sense-brief/bind",
        headers=_service_headers(),
        json={
            "issue_id": "issue-req57-01",
            "generation_version": "v2",
            "outcome": "failure",
            "reason_class": "internal_error",
            "apply": {"title": "nope", "summary": {"en": "x"}},
        },
    )
    assert response.status_code == 400


def test_req57_01_public_list_exposes_generation_keys(client: TestClient) -> None:
    _seed_issue("issue-req57-list")
    client.post(
        "/v1/issue-sense-brief/bind",
        headers=_service_headers(),
        json={
            "issue_id": "issue-req57-list",
            "generation_version": "v3",
            "outcome": "success",
            "poster_url": "https://cdn.example/list.png",
            "apply": {"title": "List brief", "summary": {"en": "Listed"}},
        },
    )
    listed = client.get("/node/issues", params={"status": "PUBLISHED"})
    assert listed.status_code == 200
    issues = listed.json()["data"]["issues"]
    match = next(i for i in issues if i["id"] == "issue-req57-list")
    assert match["generation_status"] == "ready"
    assert match["generation_version"] == "v3"
    assert match["poster_url"] == "https://cdn.example/list.png"


def test_req57_01_brief_wins_guard_unit() -> None:
    existing = {
        "title": {"en": "Brief wins"},
        "summary": {"en": "From bind"},
        "generation_status": "ready",
        "generation_version": "v1",
        "poster_url": "https://cdn.example/x.png",
    }
    rebuilt = {
        "title": {"en": "Dominant overwrite"},
        "summary": {"en": "Story alpha"},
        "generation_status": "pending",
    }
    preserved = preserve_brief_wins_fields(new_payload=rebuilt, existing=existing)
    assert preserved["title"]["en"] == "Brief wins"
    assert preserved["summary"]["en"] == "From bind"
    assert preserved["generation_status"] == "ready"
    assert preserved["poster_url"] == "https://cdn.example/x.png"


def test_req57_01_brief_wins_on_extend_save(client: TestClient) -> None:
    _seed_issue("issue-req57-wins")
    client.post(
        "/v1/issue-sense-brief/bind",
        headers=_service_headers(),
        json={
            "issue_id": "issue-req57-wins",
            "generation_version": "v9",
            "outcome": "success",
            "poster_url": "https://cdn.example/wins.png",
            "apply": {"title": "Locked brief", "summary": {"en": "Locked summary"}},
        },
    )
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    # Simulate dominant Story rebuild overwrite attempt via save path + guard helper
    existing = store.get_projection("issue-req57-wins")  # type: ignore[attr-defined]
    assert existing is not None
    attempted = {
        **existing,
        "title": {"et": "Story", "ru": "Story", "en": "Story dominant"},
        "summary": {"et": "a", "ru": "a", "en": "alpha again"},
    }
    guarded = preserve_brief_wins_fields(new_payload=attempted, existing=existing)
    store.save_projection(
        issue_id="issue-req57-wins",
        status="PUBLISHED",
        payload=guarded,
        policy_version="m3.doge_issue_derivation.v1",
    )
    got = client.get("/node/issues/issue-req57-wins")
    issue = got.json()["data"]["issue"]
    assert issue["title"]["en"] == "Locked brief"
    assert issue["generation_status"] == "ready"


def test_req57_01_bind_rejects_wrong_bearer(client: TestClient) -> None:
    """G5: Authorization Bearer ≠ SERVICE_API_TOKEN → 401 (not only missing header)."""
    _seed_issue("issue-req57-wrong-bearer")
    response = client.post(
        "/v1/issue-sense-brief/bind",
        headers={"Authorization": "Bearer channel-or-wrong-token"},
        json={
            "issue_id": "issue-req57-wrong-bearer",
            "generation_version": "v1",
            "outcome": "success",
            "poster_url": "https://cdn.example/wrong.png",
            "apply": {"title": "Should not apply", "summary": {"en": "nope"}},
        },
    )
    assert response.status_code == 401


def _create_story_for_extend(repo: InMemoryStoryRepository, idx: int) -> str:
    intake = StoryIntakeService(
        repository=repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )
    story = intake.create_story(
        parse_story_intake_request(
            with_active_schema_binding(
                {
                    "schema_version": INTAKE_SCHEMA_VERSION,
                    "submitter": {
                        "external_user_id": f"req57-user-{idx}",
                        "identity_issuer": "https://idp.example.com/eid",
                    },
                    "narrative": {
                        "original_text": f"District lights outage report #{idx}.",
                        "language": "en",
                        "session_language": "en",
                        "title": {
                            "et": "t",
                            "ru": "t",
                            "en": f"District lights outage #{idx}",
                        },
                        "description": {
                            "et": "d",
                            "ru": "d",
                            "en": f"District lights outage report #{idx}.",
                        },
                        "canonical_type": "complaint",
                        "canonical_labels": [
                            "roads",
                            "broken_infrastructure",
                            "safety",
                        ],
                    },
                }
            )
        )
    )
    return story.story.story_id


def test_req57_01_brief_wins_via_live_extend_issue() -> None:
    """G3: AC-06 evidence through IssueCreateService.create_issue → _extend_issue."""
    stories = InMemoryStoryRepository()
    story_1 = _create_story_for_extend(stories, 1)
    story_2 = _create_story_for_extend(stories, 2)
    story_3 = _create_story_for_extend(stories, 3)
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

    created = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:req57:extend",
            story_ids=(story_1, story_2),
            readiness_score=81,
            title="Living cluster issue",
        )
    )
    bind = IssueSenseBriefBindService(store=projection_store)
    bound = bind.apply_bind(
        {
            "issue_id": created.issue_id,
            "generation_version": "v-extend",
            "outcome": "success",
            "poster_url": "https://cdn.example/extend.png",
            "apply": {
                "title": "Brief locked on extend",
                "summary": {"en": "Brief summary locked"},
            },
        }
    )
    assert bound["generation_status"] == "ready"
    assert bound["title"]["en"] == "Brief locked on extend"

    extended = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:req57:extend",
            story_ids=(story_2, story_3),
            readiness_score=90,
            title="Dominant overwrite attempt",
        )
    )
    assert extended.issue_id == created.issue_id
    assert extended.projection["title"]["en"] == "Brief locked on extend"
    assert extended.projection["summary"]["en"] == "Brief summary locked"
    assert extended.projection["generation_status"] == "ready"
    assert extended.projection["poster_url"] == "https://cdn.example/extend.png"
    audit = audit_store.list_for_candidate(created.issue_id)
    assert any(entry.rationale == "cluster_growth_extend" for entry in audit)
