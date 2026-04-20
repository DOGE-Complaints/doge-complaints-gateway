from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from core.domain import (
    HealthReport,
    IdempotencyRecord,
    SignalProfileRecord,
    StoryRecord,
)


@dataclass(frozen=True)
class InMemoryHealthRepository:
    default_status: str = "ok"

    def get_health(self) -> HealthReport:
        return HealthReport(status=self.default_status)


@dataclass
class InMemoryStoryRepository:
    _records: Dict[str, StoryRecord] | None = None

    def __post_init__(self) -> None:
        if self._records is None:
            self._records = {}

    def save_story(self, record: StoryRecord) -> StoryRecord:
        self._records[record.story_id] = record
        return record

    def get_story(self, story_id: str) -> StoryRecord | None:
        return self._records.get(story_id)


@dataclass
class InMemoryIdempotencyRepository:
    _records: Dict[str, IdempotencyRecord] | None = None

    def __post_init__(self) -> None:
        if self._records is None:
            self._records = {}

    def get_by_key(self, key: str) -> IdempotencyRecord | None:
        return self._records.get(key)

    def save(self, record: IdempotencyRecord) -> IdempotencyRecord:
        self._records[record.key] = record
        return record


@dataclass
class InMemorySignalProfileRepository:
    _versions: Dict[str, list[SignalProfileRecord]] | None = None

    def __post_init__(self) -> None:
        if self._versions is None:
            self._versions = {}

    def save_version(self, profile: SignalProfileRecord) -> SignalProfileRecord:
        versions = self._versions.setdefault(profile.story_id, [])
        versions.append(profile)
        return profile

    def get_latest(self, story_id: str) -> SignalProfileRecord | None:
        versions = self._versions.get(story_id, [])
        if not versions:
            return None
        return versions[-1]

    def get_versions(self, story_id: str) -> list[SignalProfileRecord]:
        return list(self._versions.get(story_id, []))

