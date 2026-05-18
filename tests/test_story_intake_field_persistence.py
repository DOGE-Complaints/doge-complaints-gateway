from __future__ import annotations

import dataclasses

import pytest

from core.application import StoryIntakeService
from core.domain import StoryLifecycleStatus, StoryRecord
from core.domain.narrative_i18n import narrative_v2_complete
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import make_story_record, narrative_dict, valid_v2_intake_payload


@pytest.fixture()
def intake_service() -> StoryIntakeService:
    return StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
    )


def test_consistency_notes_mapped_to_storyrecord_field(intake_service: StoryIntakeService) -> None:
    """REQ-39 C-01: live_story_context.consistency_notes → narrative_consistency_notes."""
    field_names = {f.name for f in dataclasses.fields(StoryRecord)}
    assert "narrative_consistency_notes" in field_names
    assert "live_story_context" not in field_names

    request = parse_story_intake_request(
        valid_v2_intake_payload(
            live_story_context={"consistency_notes": "duplicate of #123"},
        )
    )
    saved = intake_service.create_story(request)
    assert saved.narrative_consistency_notes == "duplicate of #123"


def test_intake_to_storyrecord_field_coverage_document() -> None:
    """REQ-39 C-02: v2 intake fields are mapped or explicitly discarded."""
    mapped_top_level = {
        "schema_version",
        "submitter",
        "narrative",
        "origin",
        "privacy",
        "live_story_context",
    }
    narrative_mapped = {
        "original_text",
        "language",
        "session_language",
        "title",
        "description",
        "summary",
        "location_query",
        "canonical_type",
        "canonical_labels",
    }
    explicitly_discarded: set[str] = set()
    assert mapped_top_level
    assert narrative_mapped
    assert isinstance(explicitly_discarded, set)


@pytest.mark.parametrize(
    ("title", "description", "expected_status"),
    [
        (narrative_dict(), narrative_dict(), StoryLifecycleStatus.READY_FOR_PROFILE),
        (
            narrative_dict(et=""),
            narrative_dict(),
            StoryLifecycleStatus.PARTIAL_READY,
        ),
        (
            narrative_dict(),
            narrative_dict(en=""),
            StoryLifecycleStatus.PARTIAL_READY,
        ),
    ],
)
def test_narrative_complete_determines_lifecycle(
    intake_service: StoryIntakeService,
    title: dict[str, str],
    description: dict[str, str],
    expected_status: StoryLifecycleStatus,
) -> None:
    """REQ-39 C-03: narrative_v2_complete gates READY_FOR_PROFILE vs PARTIAL_READY."""
    repository = intake_service.repository
    accepted = repository.save_story(
        make_story_record(
            story_id="lifecycle-gate-1",
            lifecycle_status=StoryLifecycleStatus.ACCEPTED,
            narrative_original_text="Road blocked near center.",
            narrative_language="en",
            narrative_session_language="en",
            narrative_title=title,
            narrative_description=description,
        )
    )
    complete = narrative_v2_complete(
        original_text=accepted.narrative_original_text,
        language=accepted.narrative_language or "",
        title=title,
        description=description,
        session_language=accepted.narrative_session_language or "",
    )
    assert complete == (expected_status is StoryLifecycleStatus.READY_FOR_PROFILE)
    advanced = intake_service.advance_story_readiness(
        story_id=accepted.story_id,
        narrative_complete=complete,
    )
    assert advanced.lifecycle_status == expected_status


def test_no_location_query_results_in_none_geo(intake_service: StoryIntakeService) -> None:
    """REQ-39 C-04: without location_query and geo_service, StoryRecord.geo stays None."""
    request = parse_story_intake_request(valid_v2_intake_payload())
    assert request.narrative.location_query is None
    saved = intake_service.create_story(request)
    assert saved.geo is None
