from __future__ import annotations

from core.application import StoryPromotionProjectionBridge
from core.application.services import StoryIntakeService
from core.infrastructure.repositories import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION, parse_story_intake_request
from core.projection import SpaIssueStatus


def test_bridge_builds_projection_input_from_story_records() -> None:
    story_repository = InMemoryStoryRepository()
    intake_service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )
    story_a = intake_service.create_story(
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "u-1"},
                "narrative": {
                    "original_text": "Broken street light and unsafe crossing near district center.",
                    "language": "en",
                    "title_hint": "Street light issue",
                },
            }
        )
    )
    story_b = intake_service.create_story(
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "u-2"},
                "narrative": {
                    "original_text": "Road infrastructure needs urgent repair.",
                    "language": "en",
                    "title_hint": "Road repair request",
                },
            }
        )
    )

    bridge = StoryPromotionProjectionBridge(story_repository=story_repository)
    projection_input = bridge.build_projection_input(
        issue_id="issue-bridge-1",
        promoted_title="Street safety and infrastructure issue",
        story_ids=(story_a.story_id, story_b.story_id),
    )

    assert projection_input.issue_id == "issue-bridge-1"
    assert projection_input.status == SpaIssueStatus.PUBLISHED.value
    assert "infrastructure" in projection_input.labels
    assert projection_input.description.en


def test_bridge_raises_for_unknown_story_id() -> None:
    bridge = StoryPromotionProjectionBridge(story_repository=InMemoryStoryRepository())
    try:
        bridge.build_projection_input(
            issue_id="issue-bridge-missing",
            promoted_title="Any title",
            story_ids=("missing-story",),
        )
    except ValueError as exc:
        assert "Unknown story_id" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing story_id.")


def test_bridge_derivation_rules_are_deterministic_for_type_and_labels() -> None:
    story_repository = InMemoryStoryRepository()
    intake_service = StoryIntakeService(
        repository=story_repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )
    story = intake_service.create_story(
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "u-policy"},
                "narrative": {
                    "original_text": "Danger and unsafe road crossing with broken lights.",
                    "language": "en",
                    "title_hint": "Safety incident",
                },
            }
        )
    )
    bridge = StoryPromotionProjectionBridge(story_repository=story_repository)
    projection_input = bridge.build_projection_input(
        issue_id="issue-policy-1",
        promoted_title="Safety incident in district",
        story_ids=(story.story_id,),
    )

    assert projection_input.issue_type == "INCIDENT"
    assert "safety" in projection_input.labels
