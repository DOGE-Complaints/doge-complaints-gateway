from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from core.projection.enums import DOGEIssueStatus, DOGEIssueType
from core.projection.i18n import I18nText
from core.projection.input import ProjectionInput

EXTRACTION_POLICY_VERSION = "m3.story_to_doge_issue_policy.v1"


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
    ) -> StoryProjectionDraft:
        """Build policy-governed projection draft from story aggregate."""
        ...


@dataclass(frozen=True)
class DeterministicStoryToProjectionPolicy:
    policy_version: str = EXTRACTION_POLICY_VERSION

    def build_draft(
        self,
        *,
        promoted_title: str,
        aggregate_text: str,
    ) -> StoryProjectionDraft:
        summary_text = aggregate_text[:220].strip()
        description_text = aggregate_text if aggregate_text else promoted_title
        issue_type = _derive_issue_type(promoted_title, aggregate_text)
        labels = _derive_labels(promoted_title, aggregate_text)
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


def _derive_issue_type(title: str, aggregate_text: str) -> str:
    corpus = f"{title} {aggregate_text}".lower()
    if any(token in corpus for token in ("broken", "outage", "accident", "hazard", "danger")):
        return DOGEIssueType.INCIDENT.value
    if any(token in corpus for token in ("request", "need", "please", "could you")):
        return DOGEIssueType.SERVICE_REQUEST.value
    return DOGEIssueType.IMPROVEMENT.value


def _derive_labels(title: str, aggregate_text: str) -> tuple[str, ...]:
    corpus = f"{title} {aggregate_text}".lower()
    labels: list[str] = []
    if any(token in corpus for token in ("waste", "garbage", "trash")):
        labels.append("waste")
    if any(token in corpus for token in ("district", "neighborhood", "quarter")):
        labels.append("district")
    if any(token in corpus for token in ("road", "street", "light", "water", "bridge", "infrastructure")):
        labels.append("infrastructure")
    if any(token in corpus for token in ("danger", "unsafe", "hazard", "security", "safety")):
        labels.append("safety")
    if not labels:
        labels.append("infrastructure")
    return tuple(dict.fromkeys(labels))
