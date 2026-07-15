from __future__ import annotations

import pytest

from core.application.services import StoryIntakeService
from core.domain import StoryLabel
from core.infrastructure.repositories import (
    InMemoryIdempotencyRepository,
    InMemoryStoryLabelRepository,
    InMemoryStoryRepository,
)
from core.intake import IntakeValidationError, parse_story_intake_request
from core.profile.enrichment import get_signals_for_story, infer_signals_from_canonical
from core.projection.extraction_policy import canonical_labels_from_cluster
from core.projection.read_filters import disposition_allows_public_read
from core.taxonomy import LabelDisposition, is_public_label_disposition
from tests.intake_v2_fixtures import make_story_record, valid_v2_intake_payload


def _per_axis_payload() -> dict:
    return valid_v2_intake_payload(
        narrative={
            "taxonomy": {
                "topic_domain": [
                    {"label": "transport", "disposition": "canonical"},
                    {"label": "pii_present", "disposition": "internal"},
                ],
                "deep_need": [
                    {"label": "predictability", "disposition": "metadata_only"},
                ],
            }
        }
    )


def test_intake_accepts_per_axis_taxonomy_and_derives_canonical_flat_labels() -> None:
    request = parse_story_intake_request(_per_axis_payload())
    assert len(request.narrative.taxonomy) == 3
    assert request.narrative.taxonomy[0].axis == "topic_domain"
    assert request.narrative.taxonomy[0].label == "transport"
    assert request.narrative.canonical_labels == ("transport",)


def test_intake_rejects_invalid_axis() -> None:
    payload = valid_v2_intake_payload(
        narrative={
            "taxonomy": {
                "not_a_real_axis": [{"label": "roads", "disposition": "canonical"}],
            }
        }
    )
    with pytest.raises(IntakeValidationError, match="Unsupported taxonomy axis"):
        parse_story_intake_request(payload)


def test_intake_rejects_invalid_disposition() -> None:
    payload = valid_v2_intake_payload(
        narrative={
            "taxonomy": {
                "topic_domain": [{"label": "transport", "disposition": "secret"}],
            }
        }
    )
    with pytest.raises(IntakeValidationError, match="Unsupported disposition"):
        parse_story_intake_request(payload)


def test_intake_legacy_flat_labels_still_accepted() -> None:
    request = parse_story_intake_request(
        valid_v2_intake_payload(
            narrative={"canonical_labels": ["roads", "broken_infrastructure"]}
        )
    )
    assert request.narrative.canonical_labels == ("roads", "broken_infrastructure")
    assert request.narrative.taxonomy == ()


def test_persist_all_dispositions_on_submit() -> None:
    repo = InMemoryStoryRepository()
    labels = InMemoryStoryLabelRepository()
    service = StoryIntakeService(
        repository=repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
        story_label_repository=labels,
    )
    result = service.create_story(parse_story_intake_request(_per_axis_payload()))
    stored = labels.list_by_story(result.story.story_id)
    assert len(stored) == 3
    dispositions = {row.disposition for row in stored}
    assert dispositions == {
        LabelDisposition.CANONICAL.value,
        LabelDisposition.INTERNAL.value,
        LabelDisposition.METADATA_ONLY.value,
    }


def test_public_read_filter_excludes_internal_and_metadata_only() -> None:
    labels_repo = InMemoryStoryLabelRepository()
    story = make_story_record(story_id="story-tax-1")
    labels_repo.save_labels(
        (
            StoryLabel(
                story_id=story.story_id,
                axis="topic_domain",
                label="transport",
                disposition=LabelDisposition.CANONICAL.value,
            ),
            StoryLabel(
                story_id=story.story_id,
                axis="risk_privacy_safety",
                label="pii_present",
                disposition=LabelDisposition.INTERNAL.value,
            ),
            StoryLabel(
                story_id=story.story_id,
                axis="deep_need",
                label="predictability",
                disposition=LabelDisposition.METADATA_ONLY.value,
            ),
        )
    )
    public = canonical_labels_from_cluster(
        (story,),
        story_label_repository=labels_repo,
    )
    assert public == ("transport",)
    assert not is_public_label_disposition(LabelDisposition.INTERNAL.value)
    assert not disposition_allows_public_read(LabelDisposition.METADATA_ONLY.value)


def test_per_axis_signals_do_not_reguess_axis_from_dictionaries() -> None:
    labels_repo = InMemoryStoryLabelRepository()
    story = make_story_record(
        story_id="story-tax-2",
        narrative_canonical_labels=("roads",),
    )
    labels_repo.save_labels(
        (
            StoryLabel(
                story_id=story.story_id,
                axis="service_object",
                label="roads",
                disposition=LabelDisposition.CANONICAL.value,
            ),
        )
    )
    signals = get_signals_for_story(story, story_label_repository=labels_repo)
    assert signals["civic_domain"] == "unknown"
    legacy = infer_signals_from_canonical(
        story.narrative_canonical_type,
        story.narrative_canonical_labels,
    )
    assert legacy["civic_domain"] == "roads"


def test_legacy_flat_labels_fallback_still_works() -> None:
    story = make_story_record(
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure"),
    )
    signals = get_signals_for_story(story)
    assert signals["civic_domain"] == "roads"
    assert signals["failure_pattern"] == "broken_infrastructure"
