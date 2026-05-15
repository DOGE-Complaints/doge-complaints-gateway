from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from core.domain import StoryRecord
from core.projection.enums import DOGEIssueLabel, DOGEIssueStatus, DOGEIssueType
from core.projection.i18n import I18nText
from core.projection.input import ProjectionInput

EXTRACTION_POLICY_VERSION = "m3.story_to_doge_issue_policy.v2"


_CANONICAL_TYPE_TO_ISSUE_TYPE: dict[str, str] = {
    "complaint": DOGEIssueType.INCIDENT.value,
    "system_bug": DOGEIssueType.INCIDENT.value,
    "observation": DOGEIssueType.IMPROVEMENT.value,
    "absurdity": DOGEIssueType.IMPROVEMENT.value,
    "service_request": DOGEIssueType.SERVICE_REQUEST.value,
    "infrastructure": DOGEIssueType.IMPROVEMENT.value,
    "improvement": DOGEIssueType.IMPROVEMENT.value,
}


def select_dominant_story(stories: tuple[StoryRecord, ...]) -> StoryRecord:
    """Interim dominant-story picker until REQ-36 alpha_score() lands."""
    if not stories:
        raise ValueError("stories must be non-empty.")
    return max(
        stories,
        key=lambda story: (
            1 if story.narrative_canonical_type and story.narrative_canonical_type.strip() else 0,
            len(story.narrative_canonical_labels),
            story.story_id,
        ),
    )


def canonical_issue_type_from_story(story: StoryRecord) -> str:
    raw = (story.narrative_canonical_type or "observation").strip().lower()
    return _CANONICAL_TYPE_TO_ISSUE_TYPE.get(raw, DOGEIssueType.IMPROVEMENT.value)


def canonical_labels_from_cluster(stories: tuple[StoryRecord, ...]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for story in stories:
        for label in story.narrative_canonical_labels:
            normalized = label.strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            ordered.append(normalized)
    return tuple(ordered)


_SPA_LABEL_VALUES = frozenset(label.value for label in DOGEIssueLabel)

# Canonical GPT/taxonomy tokens → governed SPA board labels (REQ-34 §2.5 + SPA contract).
_CANONICAL_TO_SPA_LABEL: dict[str, str] = {
    "roads": DOGEIssueLabel.INFRASTRUCTURE.value,
    "broken_infrastructure": DOGEIssueLabel.INFRASTRUCTURE.value,
    "transport": DOGEIssueLabel.INFRASTRUCTURE.value,
    "parking": DOGEIssueLabel.INFRASTRUCTURE.value,
    "public_space": DOGEIssueLabel.INFRASTRUCTURE.value,
    "maintenance_gap": DOGEIssueLabel.INFRASTRUCTURE.value,
    "unsafe_condition": DOGEIssueLabel.SAFETY.value,
    "access_blocked": DOGEIssueLabel.SAFETY.value,
    "environment": DOGEIssueLabel.WASTE.value,
    "housing": DOGEIssueLabel.INFRASTRUCTURE.value,
    "education": DOGEIssueLabel.INFRASTRUCTURE.value,
    "healthcare": DOGEIssueLabel.INFRASTRUCTURE.value,
    "digital_service": DOGEIssueLabel.INFRASTRUCTURE.value,
    "accessibility": DOGEIssueLabel.SAFETY.value,
    "district": DOGEIssueLabel.DISTRICT.value,
}


def spa_labels_from_canonical(labels: tuple[str, ...]) -> tuple[str, ...]:
    """Map union of cluster canonical labels to governed SPA label vocabulary."""
    ordered: list[str] = []
    seen: set[str] = set()
    for label in labels:
        normalized = label.strip().lower()
        if not normalized:
            continue
        spa = (
            normalized
            if normalized in _SPA_LABEL_VALUES
            else _CANONICAL_TO_SPA_LABEL.get(normalized, DOGEIssueLabel.INFRASTRUCTURE.value)
        )
        if spa in seen:
            continue
        seen.add(spa)
        ordered.append(spa)
    if not ordered:
        return (DOGEIssueLabel.INFRASTRUCTURE.value,)
    return tuple(ordered)


@dataclass(frozen=True)
class StoryProjectionDraft:
    issue_type: str
    labels: tuple[str, ...]
    title: I18nText
    summary: I18nText
    description: I18nText
    policy_version: str


class StoryToProjectionPolicy(Protocol):
    def build_draft(
        self,
        *,
        promoted_title: str,
        aggregate_text: str,
        dominant_story: StoryRecord,
        cluster_stories: tuple[StoryRecord, ...],
    ) -> StoryProjectionDraft:
        """Build policy-governed projection draft from cluster stories."""
        ...


@dataclass(frozen=True)
class DeterministicStoryToProjectionPolicy:
    policy_version: str = EXTRACTION_POLICY_VERSION

    def build_draft(
        self,
        *,
        promoted_title: str,
        aggregate_text: str,
        dominant_story: StoryRecord,
        cluster_stories: tuple[StoryRecord, ...],
    ) -> StoryProjectionDraft:
        summary_text = aggregate_text[:220].strip()
        description_text = aggregate_text if aggregate_text else promoted_title
        issue_type = canonical_issue_type_from_story(dominant_story)
        labels = spa_labels_from_canonical(canonical_labels_from_cluster(cluster_stories))
        return StoryProjectionDraft(
            issue_type=issue_type,
            labels=labels,
            title=_to_i18n(promoted_title),
            summary=_to_i18n(summary_text if summary_text else promoted_title),
            description=_to_i18n(description_text),
            policy_version=self.policy_version,
        )


def build_projection_input_from_draft(
    *,
    issue_id: str,
    draft: StoryProjectionDraft,
) -> ProjectionInput:
    return ProjectionInput(
        issue_id=issue_id,
        status=DOGEIssueStatus.PUBLISHED.value,
        issue_type=draft.issue_type,
        labels=draft.labels,
        title=draft.title,
        summary=draft.summary,
        description=draft.description,
    )


def _to_i18n(text: str) -> I18nText:
    normalized = text.strip()
    if not normalized:
        normalized = "Issue details pending clarification"
    return I18nText(et=normalized, ru=normalized, en=normalized)
