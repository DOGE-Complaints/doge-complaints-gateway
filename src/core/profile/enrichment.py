from __future__ import annotations

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
from core.profile.schema import REQUIRED_SIGNAL_DIMENSIONS


def infer_signals_from_narrative(narrative: str) -> dict[str, str]:
    text = narrative.lower()
    inferred: dict[str, str] = {}

    inferred[SignalDimension.TOPIC.value] = (
        "infrastructure" if "road" in text or "water" in text else "public_service"
    )
    inferred[SignalDimension.SYSTEM_FAILURE.value] = (
        "service_disruption" if "blocked" in text or "leak" in text else "quality_gap"
    )
    inferred[SignalDimension.NEED.value] = (
        "restore_access" if "blocked" in text else "resolve_issue"
    )
    inferred[SignalDimension.DESIRED_STATE.value] = "stable_public_service"
    inferred[SignalDimension.REPEATABILITY.value] = (
        "recurrent" if "again" in text or "repeated" in text else "single_or_unknown"
    )
    inferred[SignalDimension.RELEVANCE.value] = "high"

    if "waste" in text or "garbage" in text or "trash" in text:
        inferred[SignalDimension.CIVIC_DOMAIN.value] = "waste"
    elif "road" in text or "street" in text:
        inferred[SignalDimension.CIVIC_DOMAIN.value] = "roads"
    if "broken" in text or "damage" in text or "unsafe" in text:
        inferred[SignalDimension.FAILURE_PATTERN.value] = "broken_infrastructure"

    for dimension in REQUIRED_SIGNAL_DIMENSIONS:
        inferred.setdefault(dimension.value, "unknown")
    return inferred


def infer_signals_from_canonical(
    canonical_type: str | None,
    canonical_labels: tuple[str, ...],
    geo_normalized_label: str | None = None,
) -> dict[str, str]:
    _ = canonical_type
    labels = set(canonical_labels)

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
        SignalDimension.GEOGRAPHIC_DISTRICT.value: geographic_district,
    }


def get_signals_for_story(story: StoryRecord, signal_source: str) -> dict[str, str]:
    src = signal_source.strip().lower()
    if src == "narrative":
        src = "keyword"
    if src == "canonical":
        return infer_signals_from_canonical(
            story.narrative_canonical_type,
            story.narrative_canonical_labels,
            story.geo.normalized_label if story.geo else None,
        )
    if src == "keyword":
        return infer_signals_from_narrative(story.narrative_original_text)
    if src == "hybrid":
        canonical = infer_signals_from_canonical(
            story.narrative_canonical_type,
            story.narrative_canonical_labels,
            story.geo.normalized_label if story.geo else None,
        )
        if all(v != "unknown" for v in canonical.values()):
            return canonical
        keyword = infer_signals_from_narrative(story.narrative_original_text)
        return {
            key: (val if val != "unknown" else keyword.get(key, "unknown"))
            for key, val in canonical.items()
        }
    raise ValueError(f"Unsupported signal_source={signal_source!r}")
