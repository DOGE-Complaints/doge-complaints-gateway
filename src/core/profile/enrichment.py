from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Sequence

from core.cluster.vocabulary import (
    AFFECTED_GROUP_DEFAULT,
    AFFECTED_SCOPE_VOCABULARY,
    CIVIC_DOMAIN_VOCABULARY,
    CIVIC_SIGNAL_PRIORITY,
    CIVIC_WEIGHT_DEFAULT,
    DESIRED_OUTCOME_VOCABULARY,
    FAILURE_PATTERN_VOCABULARY,
)
from core.domain import SignalDimension, StoryRecord
from core.taxonomy import signals_from_story_labels

if TYPE_CHECKING:
    from core.domain import StoryLabelRepository
    from core.logging_setup import StoryPipelineDebugLog


def log_story_signals_inferred(
    debug_logger: StoryPipelineDebugLog | None,
    *,
    signals: Mapping[str, str],
) -> None:
    if debug_logger is None:
        return
    debug_logger.log("signals", "inferred", {"signals": dict(signals)})


def _normalize_canonical_type(canonical_type: str | None) -> str:
    if canonical_type is None:
        return "unknown"
    normalized = canonical_type.strip().lower()
    return normalized if normalized else "unknown"


def infer_signals_from_canonical(
    canonical_type: str | None,
    canonical_labels: tuple[str, ...],
    geo_normalized_label: str | None = None,
) -> dict[str, str]:
    labels = set(canonical_labels)
    type_value = _normalize_canonical_type(canonical_type)

    civic_domain = next(
        (label for label in canonical_labels if label in CIVIC_DOMAIN_VOCABULARY),
        "unknown",
    )
    failure_pattern = next(
        (label for label in canonical_labels if label in FAILURE_PATTERN_VOCABULARY),
        "unknown",
    )
    civic_weight = next(
        (p for p in CIVIC_SIGNAL_PRIORITY if p in labels),
        CIVIC_WEIGHT_DEFAULT,
    )
    desired_outcome = next(
        (label for label in canonical_labels if label in DESIRED_OUTCOME_VOCABULARY),
        "unknown",
    )
    affected_group = next(
        (label for label in canonical_labels if label in AFFECTED_SCOPE_VOCABULARY),
        AFFECTED_GROUP_DEFAULT,
    )
    geographic_district = (
        geo_normalized_label.strip().lower()
        if geo_normalized_label and geo_normalized_label.strip()
        else "unknown"
    )

    return {
        SignalDimension.CIVIC_DOMAIN.value: civic_domain,
        SignalDimension.FAILURE_PATTERN.value: failure_pattern,
        SignalDimension.CIVIC_WEIGHT.value: civic_weight,
        SignalDimension.DESIRED_OUTCOME.value: desired_outcome,
        SignalDimension.AFFECTED_GROUP.value: affected_group,
        SignalDimension.SERVICE_OBJECT.value: "unknown",
        SignalDimension.NEED.value: "unknown",
        SignalDimension.ECOSYSTEM_SIGNAL.value: "unknown",
        SignalDimension.GEOGRAPHIC_DISTRICT.value: geographic_district,
        SignalDimension.CANONICAL_TYPE.value: type_value,
    }


def get_signals_for_story(
    story: StoryRecord,
    *,
    story_label_repository: StoryLabelRepository | None = None,
) -> dict[str, str]:
    if story_label_repository is not None:
        stored = story_label_repository.list_by_story(story.story_id)
        if stored:
            return signals_from_story_labels(
                canonical_type=story.narrative_canonical_type,
                labels=stored,
                geo_normalized_label=(
                    story.geo.normalized_label if story.geo is not None else None
                ),
            )
    return infer_signals_from_canonical(
        story.narrative_canonical_type,
        story.narrative_canonical_labels,
        story.geo.normalized_label if story.geo else None,
    )
