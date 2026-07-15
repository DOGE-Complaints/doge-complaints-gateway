from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Sequence

from core.cluster.vocabulary import (
    AFFECTED_SCOPE_VOCABULARY,
    CIVIC_DOMAIN_VOCABULARY,
    CIVIC_SIGNAL_PRIORITY,
    DESIRED_OUTCOME_VOCABULARY,
    FAILURE_PATTERN_VOCABULARY,
)
from core.domain import SignalDimension, StoryLabel
from core.taxonomy.disposition import (
    LabelDisposition,
    is_public_label_disposition,
    normalize_disposition,
)
from core.taxonomy.axes import normalize_axis


@dataclass(frozen=True)
class AxisLabelEntry:
    axis: str
    label: str
    disposition: str


def story_labels_from_narrative(*, story_id: str, narrative: object) -> tuple[StoryLabel, ...]:
    taxonomy = getattr(narrative, "taxonomy", ())
    canonical_type = getattr(narrative, "canonical_type", None)
    canonical_labels = getattr(narrative, "canonical_labels", ())
    if taxonomy:
        return tuple(
            StoryLabel(
                story_id=story_id,
                axis=entry.axis,
                label=entry.label,
                disposition=entry.disposition,
            )
            for entry in taxonomy
        )
    return legacy_flat_labels_to_story_labels(
        story_id=story_id,
        canonical_type=canonical_type,
        canonical_labels=canonical_labels,
    )


def legacy_flat_labels_to_story_labels(
    *,
    story_id: str,
    canonical_type: str | None,
    canonical_labels: tuple[str, ...],
) -> tuple[StoryLabel, ...]:
    if not canonical_labels:
        return ()
    rows: list[StoryLabel] = []
    for label in canonical_labels:
        axis = infer_axis_for_flat_label(label, canonical_type=canonical_type)
        rows.append(
            StoryLabel(
                story_id=story_id,
                axis=axis,
                label=label,
                disposition=LabelDisposition.CANONICAL.value,
            )
        )
    return tuple(rows)


def infer_axis_for_flat_label(label: str, *, canonical_type: str | None = None) -> str:
    normalized = label.strip().lower()
    if normalized in CIVIC_DOMAIN_VOCABULARY:
        return "topic_domain"
    if normalized in FAILURE_PATTERN_VOCABULARY:
        return "failure_mode"
    if normalized in AFFECTED_SCOPE_VOCABULARY:
        return "affected_scope"
    if normalized in DESIRED_OUTCOME_VOCABULARY:
        return "desired_outcome"
    if normalized in CIVIC_SIGNAL_PRIORITY:
        return "civic_signal"
    if canonical_type and normalized == (canonical_type or "").strip().lower():
        return "issue_archetype_support"
    return "topic_domain"


def canonical_flat_labels_from_taxonomy(
    taxonomy: tuple[AxisLabelEntry, ...],
) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for entry in taxonomy:
        if entry.disposition != LabelDisposition.CANONICAL.value:
            continue
        if entry.label in seen:
            continue
        seen.add(entry.label)
        ordered.append(entry.label)
    return tuple(ordered)


def public_label_strings(labels: Sequence[StoryLabel]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for row in labels:
        if not is_public_label_disposition(row.disposition):
            continue
        if row.label in seen:
            continue
        seen.add(row.label)
        ordered.append(row.label)
    return tuple(ordered)


def public_canonical_labels_for_stories(
    stories: Sequence[object],
    *,
    list_labels_for_story: Callable[[str], Sequence[StoryLabel]],
) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for story in stories:
        story_id = getattr(story, "story_id", None)
        if not isinstance(story_id, str):
            continue
        for label in public_label_strings(list_labels_for_story(story_id)):
            if label in seen:
                continue
            seen.add(label)
            ordered.append(label)
    return tuple(ordered)


_AXIS_TO_SIGNAL_DIMENSION: dict[str, SignalDimension] = {
    "topic_domain": SignalDimension.CIVIC_DOMAIN,
    "failure_mode": SignalDimension.FAILURE_PATTERN,
    "civic_signal": SignalDimension.CIVIC_WEIGHT,
    "desired_outcome": SignalDimension.DESIRED_OUTCOME,
    "affected_scope": SignalDimension.AFFECTED_GROUP,
    SignalDimension.CIVIC_DOMAIN.value: SignalDimension.CIVIC_DOMAIN,
    SignalDimension.FAILURE_PATTERN.value: SignalDimension.FAILURE_PATTERN,
    SignalDimension.CIVIC_WEIGHT.value: SignalDimension.CIVIC_WEIGHT,
    SignalDimension.DESIRED_OUTCOME.value: SignalDimension.DESIRED_OUTCOME,
    SignalDimension.AFFECTED_GROUP.value: SignalDimension.AFFECTED_GROUP,
}


def signals_from_story_labels(
    *,
    canonical_type: str | None,
    labels: Sequence[StoryLabel],
    geo_normalized_label: str | None = None,
) -> dict[str, str]:
    by_axis: dict[str, list[str]] = {}
    for row in labels:
        by_axis.setdefault(row.axis, []).append(row.label)

    type_value = (canonical_type or "unknown").strip().lower() or "unknown"
    geographic_district = (
        geo_normalized_label.strip().lower()
        if geo_normalized_label and geo_normalized_label.strip()
        else "unknown"
    )

    signals: dict[str, str] = {}
    for axis, dimension in _AXIS_TO_SIGNAL_DIMENSION.items():
        axis_labels = by_axis.get(axis, [])
        signals[dimension.value] = axis_labels[0] if axis_labels else "unknown"

    signals[SignalDimension.GEOGRAPHIC_DISTRICT.value] = geographic_district
    signals[SignalDimension.CANONICAL_TYPE.value] = type_value
    return signals


def parse_taxonomy_payload(raw: object) -> tuple[AxisLabelEntry, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, Mapping):
        raise ValueError("narrative.taxonomy must be an object.")
    entries: list[AxisLabelEntry] = []
    for axis_raw, items_raw in raw.items():
        axis = normalize_axis(axis_raw)
        if not isinstance(items_raw, (list, tuple)):
            raise ValueError(f"narrative.taxonomy.{axis} must be an array.")
        for idx, item in enumerate(items_raw):
            if not isinstance(item, Mapping):
                raise ValueError(f"narrative.taxonomy.{axis}[{idx}] must be an object.")
            label_raw = item.get("label")
            if not isinstance(label_raw, str) or not label_raw.strip():
                raise ValueError(f"narrative.taxonomy.{axis}[{idx}].label is required.")
            disposition = normalize_disposition(item.get("disposition"))
            entries.append(
                AxisLabelEntry(
                    axis=axis,
                    label=label_raw.strip().lower(),
                    disposition=disposition,
                )
            )
    return tuple(entries)
