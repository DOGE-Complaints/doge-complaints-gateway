"""Public Emerging L2 derived read-model (GW-ES-03 / REQ-50).

Normative: Topic/label language ≠ Issues; source is story labels, not
``list_projections``. No persistent ``EmergingSignal`` entity.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from core.application.issue_create import IssueProjectionReadStore, IssueStoryLinkStore
from core.application.story_activity import (
    CABINET_STATUS_PUBLISHED,
    map_issue_status_to_cabinet,
)
from core.domain import StoryLabelRepository, StoryRepository
from core.taxonomy.disposition import is_public_label_disposition

DEFAULT_TOP_N = 10
MIN_TOP_N = 1
MAX_TOP_N = 50


def clamp_top_n(top_n: int) -> int:
    """Clamp query/default top_n to REQ-50 bounds [1, 50]."""
    if top_n < MIN_TOP_N:
        return MIN_TOP_N
    if top_n > MAX_TOP_N:
        return MAX_TOP_N
    return top_n


@dataclass(frozen=True)
class EmergingSignalsService:
    """Build non-PII Emerging L2 aggregates from labels + published exclusion."""

    story_repository: StoryRepository
    story_label_repository: StoryLabelRepository
    issue_story_link_store: IssueStoryLinkStore | None
    issue_projection_read_store: IssueProjectionReadStore

    def _story_is_published_linked(self, story_id: str) -> bool:
        if self.issue_story_link_store is None:
            return False
        issue_id = self.issue_story_link_store.get_issue_id_for_story(story_id)
        if not issue_id:
            return False
        projection = self.issue_projection_read_store.get_projection(issue_id)
        if projection is None:
            return False
        raw_status = str(projection.get("status", ""))
        cabinet = map_issue_status_to_cabinet(raw_status, issue_id=issue_id)
        return cabinet == CABINET_STATUS_PUBLISHED

    def build_emerging(self, *, top_n: int = DEFAULT_TOP_N) -> dict[str, Any]:
        applied = clamp_top_n(int(top_n))
        stories = self.story_repository.list_stories()
        freq: Counter[tuple[str, str]] = Counter()

        for story in stories:
            if self._story_is_published_linked(story.story_id):
                continue
            for row in self.story_label_repository.list_by_story(story.story_id):
                if not is_public_label_disposition(row.disposition):
                    continue
                label = row.label.strip()
                axis = row.axis.strip()
                if not label or not axis:
                    continue
                freq[(label, axis)] += 1

        ranked = sorted(freq.items(), key=lambda item: (-item[1], item[0][0], item[0][1]))
        signals = [
            {"label": label, "axis": axis, "story_count": count}
            for (label, axis), count in ranked[:applied]
        ]
        return {"signals": signals, "top_n": applied}
