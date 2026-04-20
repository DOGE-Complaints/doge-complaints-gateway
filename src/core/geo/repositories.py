from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Protocol

from core.domain import StoryGeoSnapshot


@dataclass(frozen=True)
class GeoCacheEntry:
    snapshot: StoryGeoSnapshot
    stored_at: datetime


class GeoCacheRepository(Protocol):
    def get(self, canonical_key: str) -> GeoCacheEntry | None:
        """Return cached entry by canonical key."""

    def put(self, canonical_key: str, snapshot: StoryGeoSnapshot, *, stored_at: datetime) -> None:
        """Upsert cache row."""


@dataclass
class InMemoryGeoCacheRepository:
    _rows: Dict[str, GeoCacheEntry] = field(default_factory=dict)

    def get(self, canonical_key: str) -> GeoCacheEntry | None:
        return self._rows.get(canonical_key)

    def put(self, canonical_key: str, snapshot: StoryGeoSnapshot, *, stored_at: datetime) -> None:
        self._rows[canonical_key] = GeoCacheEntry(snapshot=snapshot, stored_at=stored_at)
