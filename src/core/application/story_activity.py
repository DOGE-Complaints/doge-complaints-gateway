"""User cabinet story activity read model (GW-CAB-01)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.application.issue_create import IssueProjectionReadStore, IssueStoryLinkStore
from core.domain import StoryRepository
from core.projection.enums import DOGEIssueStatus
from core.projection.read_filters import canonicalize_status_on_read

CABINET_STATUS_PUBLISHED = "published"
CABINET_STATUS_UNDER_REVIEW = "under_review"


def map_issue_status_to_cabinet(raw_status: str | None, *, issue_id: str = "") -> str:
    """Map issue projection status to SPA cabinet enum (D-CAB01-2)."""
    if raw_status is None or not str(raw_status).strip():
        return CABINET_STATUS_UNDER_REVIEW
    canonical = canonicalize_status_on_read(raw_status, issue_id=issue_id, log_unknown=False)
    if canonical == DOGEIssueStatus.PUBLISHED.value:
        return CABINET_STATUS_PUBLISHED
    return CABINET_STATUS_UNDER_REVIEW


@dataclass(frozen=True)
class StoryActivityService:
    story_repository: StoryRepository
    issue_story_link_store: IssueStoryLinkStore | None
    issue_projection_read_store: IssueProjectionReadStore

    def build_activity(self, *, submitter_external_user_id: str) -> dict[str, Any]:
        sub = submitter_external_user_id.strip()
        stories = self.story_repository.list_stories_by_submitter(sub)
        rows: list[dict[str, str]] = []
        published_count = 0
        under_review_count = 0

        for story in sorted(stories, key=lambda s: s.created_at, reverse=True):
            issue_id = None
            if self.issue_story_link_store is not None:
                issue_id = self.issue_story_link_store.get_issue_id_for_story(story.story_id)

            raw_status: str | None = None
            if issue_id:
                projection = self.issue_projection_read_store.get_projection(issue_id)
                if projection is not None:
                    raw_status = str(projection.get("status", ""))

            cabinet_status = map_issue_status_to_cabinet(raw_status, issue_id=issue_id or "")
            if cabinet_status == CABINET_STATUS_PUBLISHED:
                published_count += 1
            else:
                under_review_count += 1

            rows.append(
                {
                    "story_id": story.story_id,
                    "status": cabinet_status,
                    "created_at": story.created_at.isoformat(),
                }
            )

        return {
            "metrics": {
                "submitted": len(stories),
                "published": published_count,
                "under_review": under_review_count,
            },
            "stories": rows,
        }
