"""GW-L10N-01 acceptance tests — projection i18n preservation."""

from __future__ import annotations

from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryRepository,
)
from core.projection import DeterministicStoryToProjectionPolicy, IssueProjectionService
from tests.intake_v2_fixtures import make_story_record, narrative_dict


def test_dominant_story_distinct_title_locales_produce_distinct_projection_title() -> None:
    story = make_story_record(
        narrative_title=narrative_dict(
            et="Katki tänav ET",
            ru="Сломанная улица RU",
            en="Broken street EN",
        ),
        narrative_description=narrative_dict(
            et="Kirjeldus ET",
            ru="Описание RU",
            en="Description EN",
        ),
        narrative_summary=narrative_dict(
            et="Kokkuvõte ET",
            ru="Резюме RU",
            en="Summary EN",
        ),
    )
    draft = DeterministicStoryToProjectionPolicy().build_draft(
        promoted_title="flattened fallback title",
        aggregate_text="aggregate body text",
        dominant_story=story,
        cluster_stories=(story,),
    )

    assert draft.title.et == "Katki tänav ET"
    assert draft.title.en == "Broken street EN"
    assert draft.title.et != draft.title.en
    assert draft.description.ru == "Описание RU"
    assert draft.summary.en == "Summary EN"


def test_dominant_story_missing_narrative_title_falls_back_to_promoted_title() -> None:
    story = make_story_record(narrative_title=None)
    promoted = "Single promoted title"
    draft = DeterministicStoryToProjectionPolicy().build_draft(
        promoted_title=promoted,
        aggregate_text="aggregate body",
        dominant_story=story,
        cluster_stories=(story,),
    )

    assert draft.title.et == promoted
    assert draft.title.ru == promoted
    assert draft.title.en == promoted


def test_manual_create_preserves_request_i18n_title() -> None:
    stories = InMemoryStoryRepository()
    story = make_story_record(
        story_id="manual-story-1",
        narrative_title=narrative_dict(en="Dominant EN only"),
    )
    stories.save_story(story)
    projection_store = InMemoryIssueProjectionStore()
    from core.promotion import IssuePromotionService
    from core.promotion.gates import PromotionGatePolicy
    from core.promotion.repositories import (
        InMemoryIssueCandidateStore,
        InMemoryReviewAuditLogRepository,
    )

    service = IssueCreateService(
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
    request_title = {"et": "Katki ET", "ru": "Сломано RU", "en": "Broken EN"}
    issue_id = service.create_manual_issue(
        cluster_id="cluster:manual-i18n",
        story_ids=[story.story_id],
        title=request_title,
        issue_type="complaint",
    )
    saved = projection_store.get_projection(issue_id)
    assert saved is not None
    title = saved["title"]
    assert isinstance(title, dict)
    assert title["et"] == "Katki ET"
    assert title["en"] == "Broken EN"
    assert title["et"] != title["en"]


def test_bridge_multi_story_cluster_preserves_per_locale_title_in_public_dict() -> None:
    stories = InMemoryStoryRepository()
    rich = make_story_record(
        story_id="story-rich-i18n",
        narrative_title=narrative_dict(et="ET bridge", ru="RU bridge", en="EN bridge"),
        narrative_description=narrative_dict(et="d-et", ru="d-ru", en="d-en"),
        narrative_canonical_labels=("roads", "safety", "broken_infrastructure"),
    )
    sparse = make_story_record(
        story_id="story-sparse-i18n",
        narrative_title=narrative_dict(et="t", ru="t", en="t"),
        narrative_canonical_labels=("roads",),
    )
    stories.save_story(rich)
    stories.save_story(sparse)

    bridge = StoryPromotionProjectionBridge(story_repository=stories)
    projection_input = bridge.build_projection_input(
        issue_id="issue-bridge-cluster-1",
        promoted_title="flattened promoted title",
        story_ids=(sparse.story_id, rich.story_id),
    )

    assert projection_input.title.et == "ET bridge"
    assert projection_input.title.en == "EN bridge"
    assert projection_input.title.et != projection_input.title.en

    projection = IssueProjectionService().project(projection_input)
    public = projection.to_public_dict()
    title = public["title"]
    assert isinstance(title, dict)
    assert title["et"] == "ET bridge"
    assert title["en"] == "EN bridge"
    assert title["et"] != title["en"]
