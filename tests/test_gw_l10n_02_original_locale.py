"""GW-L10N-02 acceptance tests — original_locale in public projection."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryRepository,
)
from core.projection import IssueProjectionService
from core.projection.i18n import original_locale_from_languages
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from tests.intake_v2_fixtures import make_story_record, narrative_dict


def test_original_locale_from_languages_canonical_order_and_dedup() -> None:
    assert original_locale_from_languages(["ru", "et", "ru", "en", "et"]) == ("et", "ru", "en")
    assert original_locale_from_languages(["ru"]) == ("ru",)
    assert original_locale_from_languages(["xx", None, ""]) == ()


def test_mono_et_cluster_produces_original_locale_et() -> None:
    stories = InMemoryStoryRepository()
    story = make_story_record(
        story_id="story-et-only",
        narrative_language="et",
        narrative_title=narrative_dict(et="ET title"),
    )
    stories.save_story(story)
    bridge = StoryPromotionProjectionBridge(story_repository=stories)
    projection_input = bridge.build_projection_input(
        issue_id="issue-mono-et",
        promoted_title="ET title",
        story_ids=(story.story_id,),
    )
    assert projection_input.original_locale == ("et",)

    public = IssueProjectionService().project(projection_input).to_public_dict()
    assert public["original_locale"] == ["et"]


def test_mixed_et_ru_cluster_produces_canonical_order() -> None:
    stories = InMemoryStoryRepository()
    et_story = make_story_record(
        story_id="story-et",
        narrative_language="et",
        narrative_title=narrative_dict(et="ET"),
    )
    ru_story = make_story_record(
        story_id="story-ru",
        narrative_language="ru",
        narrative_title=narrative_dict(ru="RU"),
    )
    stories.save_story(et_story)
    stories.save_story(ru_story)

    bridge = StoryPromotionProjectionBridge(story_repository=stories)
    projection_input = bridge.build_projection_input(
        issue_id="issue-mixed",
        promoted_title="Mixed cluster",
        story_ids=(ru_story.story_id, et_story.story_id),
    )
    assert projection_input.original_locale == ("et", "ru")

    public = IssueProjectionService().project(projection_input).to_public_dict()
    assert public["original_locale"] == ["et", "ru"]


def test_unknown_language_omits_original_locale_from_public_dict() -> None:
    stories = InMemoryStoryRepository()
    story = make_story_record(
        story_id="story-unknown-lang",
        narrative_language=None,
    )
    stories.save_story(story)
    bridge = StoryPromotionProjectionBridge(story_repository=stories)
    projection_input = bridge.build_projection_input(
        issue_id="issue-no-lang",
        promoted_title="No language",
        story_ids=(story.story_id,),
    )
    assert projection_input.original_locale == ()

    public = IssueProjectionService().project(projection_input).to_public_dict()
    assert "original_locale" not in public


def _issue_create_service(
    stories: InMemoryStoryRepository,
    projection_store: InMemoryIssueProjectionStore,
) -> IssueCreateService:
    return IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
        issue_projection_store=projection_store,
        issue_story_link_store=InMemoryIssueStoryLinkStore(),
    )


def test_manual_create_includes_original_locale_from_story_ids() -> None:
    stories = InMemoryStoryRepository()
    story = make_story_record(
        story_id="manual-et-story",
        narrative_language="et",
        narrative_title=narrative_dict(et="Manual ET"),
    )
    stories.save_story(story)
    projection_store = InMemoryIssueProjectionStore()
    service = _issue_create_service(stories, projection_store)

    issue_id = service.create_manual_issue(
        cluster_id="cluster:manual-original-locale",
        story_ids=[story.story_id],
        title={"et": "Manual ET", "ru": "Manual RU", "en": "Manual EN"},
        issue_type="complaint",
    )
    saved = projection_store.get_projection(issue_id)
    assert saved is not None
    assert saved.get("original_locale") == ["et"]


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch.setenv("SERVICE_API_TOKEN", "gw-l10n-02-test-token")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer gw-l10n-02-test-token"}


def test_tallinn_list_and_get_return_original_locale(client: TestClient) -> None:
    stories = get_api_dependencies().story_cluster_orchestrator.story_repository
    et_story = make_story_record(
        story_id="api-story-et",
        narrative_language="et",
        narrative_title=narrative_dict(et="API ET"),
    )
    ru_story = make_story_record(
        story_id="api-story-ru",
        narrative_language="ru",
        narrative_title=narrative_dict(ru="API RU"),
    )
    stories.save_story(et_story)
    stories.save_story(ru_story)

    create_response = client.post(
        "/node/issues",
        headers=_auth_headers(),
        json={
            "cluster_id": "cluster:api-original-locale",
            "story_ids": [et_story.story_id, ru_story.story_id],
            "title": {"et": "API ET", "ru": "API RU", "en": "API EN"},
            "type": "complaint",
        },
    )
    assert create_response.status_code == 201
    issue_id = str(create_response.json()["data"]["issue_id"])

    list_response = client.get("/node/issues")
    assert list_response.status_code == 200
    listed = list_response.json()["data"]["issues"]
    match = next(item for item in listed if item["id"] == issue_id)
    assert match["original_locale"] == ["et", "ru"]

    get_response = client.get(f"/node/issues/{issue_id}")
    assert get_response.status_code == 200
    issue = get_response.json()["data"]["issue"]
    assert issue["original_locale"] == ["et", "ru"]
