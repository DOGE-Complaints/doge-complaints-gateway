"""Public Network Pulse L1 aggregates (GW-ES-02 / REQ-49)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from core.domain import StoryLabelRepository, StoryRecord, StoryRepository
from core.taxonomy.disposition import is_public_label_disposition


def _area_key(story: StoryRecord) -> str | None:
    geo = story.geo
    if geo is None:
        return None
    for candidate in (geo.admin_district, geo.admin_settlement, geo.admin_region):
        if candidate is not None and str(candidate).strip():
            return str(candidate).strip()
    return None


def _sorted_key_counts(counter: Counter[str]) -> list[dict[str, Any]]:
    items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return [{"key": key, "count": count} for key, count in items]


@dataclass(frozen=True)
class NetworkPulseService:
    """Build non-PII public Network Pulse aggregates from stories + labels."""

    story_repository: StoryRepository
    story_label_repository: StoryLabelRepository | None = None

    def build_pulse(self, *, now: datetime | None = None) -> dict[str, Any]:
        clock = now if now is not None else datetime.now(UTC)
        if clock.tzinfo is None:
            clock = clock.replace(tzinfo=UTC)
        else:
            clock = clock.astimezone(UTC)

        stories = self.story_repository.list_stories()
        language_counts: Counter[str] = Counter()
        area_counts: Counter[str] = Counter()
        cutoff = clock - timedelta(days=7)
        recent = 0

        for story in stories:
            lang = story.narrative_language
            if lang is not None and str(lang).strip():
                language_counts[str(lang).strip()] += 1
            area = _area_key(story)
            if area is not None:
                area_counts[area] += 1
            created = story.created_at
            if created.tzinfo is None:
                created = created.replace(tzinfo=UTC)
            else:
                created = created.astimezone(UTC)
            if created >= cutoff:
                recent += 1

        topics: list[dict[str, Any]] = []
        if self.story_label_repository is not None:
            topic_counter: Counter[tuple[str, str]] = Counter()
            for story in stories:
                for row in self.story_label_repository.list_by_story(story.story_id):
                    if not is_public_label_disposition(row.disposition):
                        continue
                    label = row.label.strip()
                    axis = row.axis.strip()
                    if not label or not axis:
                        continue
                    topic_counter[(label, axis)] += 1
            topics = [
                {"label": label, "axis": axis, "count": count}
                for (label, axis), count in sorted(
                    topic_counter.items(), key=lambda item: (-item[1], item[0][0], item[0][1])
                )
            ]

        return {
            "stories_collected": len(stories),
            "languages": _sorted_key_counts(language_counts),
            "areas": _sorted_key_counts(area_counts),
            "topics": topics,
            "recent_stories_7d": recent,
        }
