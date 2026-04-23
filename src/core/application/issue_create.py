from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.domain import StoryRepository
from core.projection import I18nText, IssueProjectionService, ProjectionInput, SpaIssueStatus, SpaIssueType
from core.promotion import IssuePromotionService, ReviewDecision

DERIVATION_POLICY_VERSION = "m2.spa_issue_derivation.v1"


@dataclass(frozen=True)
class IssueCreateCommand:
    cluster_id: str
    story_ids: tuple[str, ...]
    readiness_score: int
    title: str


@dataclass(frozen=True)
class IssueCreateResult:
    issue_id: str
    status: str
    projection: dict[str, Any]
    policy_version: str = DERIVATION_POLICY_VERSION

    def as_dict(self) -> dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "status": self.status,
            "projection": self.projection,
            "policy_version": self.policy_version,
        }


@dataclass(frozen=True)
class StoryPromotionProjectionBridge:
    story_repository: StoryRepository

    def build_projection_input(
        self,
        *,
        issue_id: str,
        promoted_title: str,
        story_ids: tuple[str, ...],
    ) -> ProjectionInput:
        stories = []
        for story_id in story_ids:
            story = self.story_repository.get_story(story_id)
            if story is None:
                raise ValueError(f"Unknown story_id: {story_id}.")
            stories.append(story)

        narrative_chunks = [story.narrative_original_text.strip() for story in stories if story.narrative_original_text.strip()]
        aggregate_text = " ".join(narrative_chunks) if narrative_chunks else promoted_title
        summary = aggregate_text[:220].strip()
        description = aggregate_text if aggregate_text else promoted_title

        issue_type = _derive_issue_type(promoted_title, aggregate_text)
        labels = _derive_labels(promoted_title, aggregate_text)

        i18n_title = _to_i18n(promoted_title)
        i18n_summary = _to_i18n(summary if summary else promoted_title)
        i18n_description = _to_i18n(description)

        return ProjectionInput(
            issue_id=issue_id,
            status=SpaIssueStatus.PUBLISHED.value,
            issue_type=issue_type,
            labels=labels,
            title=i18n_title,
            summary=i18n_summary,
            description=i18n_description,
        )


@dataclass(frozen=True)
class IssueCreateService:
    promotion_service: IssuePromotionService
    projection_service: IssueProjectionService
    bridge: StoryPromotionProjectionBridge

    def create_issue(self, command: IssueCreateCommand) -> IssueCreateResult:
        if not command.cluster_id.strip():
            raise ValueError("cluster_id must be non-empty.")
        if not command.story_ids:
            raise ValueError("story_ids must contain at least one story id.")
        if not command.title.strip():
            raise ValueError("title must be non-empty.")

        candidate = self.promotion_service.create_candidate(
            cluster_id=command.cluster_id.strip(),
            story_ids=tuple(story_id.strip() for story_id in command.story_ids if story_id.strip()),
            readiness_score=command.readiness_score,
            title=command.title.strip(),
        )
        self.promotion_service.submit_for_review(candidate.candidate_id)
        self.promotion_service.start_review(candidate.candidate_id)
        promoted = self.promotion_service.record_review(
            candidate_id=candidate.candidate_id,
            actor="system",
            decision=ReviewDecision.APPROVE,
            rationale="http_create_issue_auto_promote",
        )

        projection_input = self.bridge.build_projection_input(
            issue_id=promoted.candidate_id,
            promoted_title=promoted.title,
            story_ids=promoted.story_ids,
        )
        projection = self.projection_service.project(projection_input)

        return IssueCreateResult(
            issue_id=promoted.candidate_id,
            status=promoted.status.value,
            projection=projection.to_public_dict(),
        )


def _to_i18n(text: str) -> I18nText:
    normalized = text.strip()
    if not normalized:
        normalized = "Issue details pending clarification"
    # Baseline deterministic fallback until dedicated translation stage is introduced.
    return I18nText(et=normalized, ru=normalized, en=normalized)


def _derive_issue_type(title: str, aggregate_text: str) -> str:
    corpus = f"{title} {aggregate_text}".lower()
    if any(token in corpus for token in ("broken", "outage", "accident", "hazard", "danger")):
        return SpaIssueType.INCIDENT.value
    if any(token in corpus for token in ("request", "need", "please", "could you")):
        return SpaIssueType.SERVICE_REQUEST.value
    return SpaIssueType.IMPROVEMENT.value


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
