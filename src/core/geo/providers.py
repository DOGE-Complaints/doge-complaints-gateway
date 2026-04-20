from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from core.domain import StoryGeoSnapshot


class GeoProvider(Protocol):
    @property
    def provider_id(self) -> str: ...

    def resolve(self, original_query: str, *, canonical_key: str) -> StoryGeoSnapshot | None:
        """Return a snapshot or None if this provider cannot resolve."""


@dataclass(frozen=True)
class _TallinnOpenCageStub:
    """First in chain: resolves Tallinn only."""

    provider_id: str = "opencage_stub"

    def resolve(self, original_query: str, *, canonical_key: str) -> StoryGeoSnapshot | None:
        if "tallinn" in canonical_key:
            return StoryGeoSnapshot(
                normalized_label="Tallinn, EE",
                latitude=59.437,
                longitude=24.7536,
                confidence=0.88,
                provider=self.provider_id,
                cluster_tags=("place:tallinn", "country:ee"),
            )
        return None


@dataclass(frozen=True)
class _NarvaNominatimStub:
    """Second in chain: resolves Narva (fallback demo)."""

    provider_id: str = "nominatim_stub"

    def resolve(self, original_query: str, *, canonical_key: str) -> StoryGeoSnapshot | None:
        if "narva" in canonical_key:
            return StoryGeoSnapshot(
                normalized_label="Narva, EE",
                latitude=59.3793,
                longitude=28.1791,
                confidence=0.82,
                provider=self.provider_id,
                cluster_tags=("place:narva", "country:ee"),
            )
        return None


def default_provider_chain() -> tuple[GeoProvider, ...]:
    return (_TallinnOpenCageStub(), _NarvaNominatimStub())
