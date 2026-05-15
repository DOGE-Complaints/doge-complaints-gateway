from __future__ import annotations

from core.application import StoryPromotionProjectionBridge
from core.application.services import StoryIntakeService
from core.infrastructure.repositories import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict
from core.projection import I18nText, DOGEIssueStatus, StoryProjectionDraft


class _CustomPolicy:
    def build_draft(
        self,
        *,
        promoted_title: str,
        aggregate_text: str,
        dominant_story,
        cluster_stories,
    ) -> StoryProjectionDraft:
        return StoryProjectionDraft(
            issue_type="SERVICE_REQUEST",
            labels=("district",),
            title=I18nText(et=promoted_title, ru=promoted_title, en=promoted_title),
            summary=I18nText(et="custom-summary", ru="custom-summary", en="custom-summary"),
            description=I18nText(et=aggregate_text, ru=aggregate_text, en=aggregate_text),
            policy_version="test.custom-policy.v1",
        )


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
                "submitter": {"external_user_id": "u-1", "identity_issuer": "https://idp.example.com/eid"},
                "narrative": {
            "original_text": "Broken street light and unsafe crossing near district center.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Street light issue"},
            "description": {"et": "d", "ru": "d", "en": "Broken street light and unsafe crossing near district center."},
            "canonical_type": "complaint",
            "canonical_labels": ["roads", "safety"],
                },
            }
        )
    )
    story_b = intake_service.create_story(
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "u-2", "identity_issuer": "https://idp.example.com/eid"},
                "narrative": {
            "original_text": "Road infrastructure needs urgent repair.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Road repair request"},
            "description": {"et": "d", "ru": "d", "en": "Road infrastructure needs urgent repair."},
            "canonical_type": "complaint",
            "canonical_labels": ["roads", "infrastructure"],
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
    assert projection_input.status == DOGEIssueStatus.PUBLISHED.value
    assert "infrastructure" in projection_input.labels
    assert "safety" in projection_input.labels
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
                "submitter": {"external_user_id": "u-policy", "identity_issuer": "https://idp.example.com/eid"},
                "narrative": {
            "original_text": "Danger and unsafe road crossing with broken lights.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Safety incident"},
            "description": {"et": "d", "ru": "d", "en": "Danger and unsafe road crossing with broken lights."},
            "canonical_type": "complaint",
            "canonical_labels": ["safety", "roads"],
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


def test_bridge_supports_pluggable_projection_policy_boundary() -> None:
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
                "submitter": {"external_user_id": "u-custom", "identity_issuer": "https://idp.example.com/eid"},
                "narrative": {
            "original_text": "District services need predictable scheduling.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Service schedule"},
            "description": {"et": "d", "ru": "d", "en": "District services need predictable scheduling."},
                },
            }
        )
    )

    bridge = StoryPromotionProjectionBridge(
        story_repository=story_repository,
        extraction_policy=_CustomPolicy(),
    )
    projection_input = bridge.build_projection_input(
        issue_id="issue-custom-policy",
        promoted_title="Service schedule",
        story_ids=(story.story_id,),
    )

    assert projection_input.issue_type == "SERVICE_REQUEST"
    assert projection_input.labels == ("district",)
    assert projection_input.summary.en == "custom-summary"
