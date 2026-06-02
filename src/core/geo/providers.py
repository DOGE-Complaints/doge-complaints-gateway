from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from core.domain import StoryGeoSnapshot


class GeoProvider(Protocol):
    @property
    def provider_id(self) -> str: ...

    def resolve(self, original_query: str, *, canonical_key: str) -> StoryGeoSnapshot | None:
        """Return a snapshot or None if this provider cannot resolve."""


_PROVIDER_ID = "estonia_lookup_stub"


def _city_snapshot(
    *,
    label: str,
    latitude: float,
    longitude: float,
    settlement: str,
    region: str,
    tags: tuple[str, ...],
) -> StoryGeoSnapshot:
    return StoryGeoSnapshot(
        normalized_label=label,
        latitude=latitude,
        longitude=longitude,
        confidence=0.85,
        provider=_PROVIDER_ID,
        cluster_tags=tags,
        admin_settlement=settlement,
        admin_region=region,
        admin_country="EE",
    )


def _district_snapshot(
    *,
    label: str,
    latitude: float,
    longitude: float,
    district: str,
    tags: tuple[str, ...],
) -> StoryGeoSnapshot:
    return StoryGeoSnapshot(
        normalized_label=label,
        latitude=latitude,
        longitude=longitude,
        confidence=0.85,
        provider=_PROVIDER_ID,
        cluster_tags=tags,
        admin_district=district,
        admin_settlement="tallinn",
        admin_region="harju maakond",
        admin_country="EE",
    )


def _build_geo_lookup() -> dict[str, StoryGeoSnapshot]:
    lookup: dict[str, StoryGeoSnapshot] = {}

    def _aliases(snapshot: StoryGeoSnapshot, *keywords: str) -> None:
        for keyword in keywords:
            lookup[keyword] = snapshot

    _aliases(
        _city_snapshot(
            label="Tallinn, EE",
            latitude=59.437,
            longitude=24.7536,
            settlement="tallinn",
            region="harju maakond",
            tags=("place:tallinn", "country:ee"),
        ),
        "tallinn",
        "таллин",
        "таллинн",
    )
    _aliases(
        _city_snapshot(
            label="Tartu, EE",
            latitude=58.378,
            longitude=26.729,
            settlement="tartu",
            region="tartu maakond",
            tags=("place:tartu", "country:ee"),
        ),
        "tartu",
        "тарту",
    )
    _aliases(
        _city_snapshot(
            label="Narva, EE",
            latitude=59.3793,
            longitude=28.1791,
            settlement="narva",
            region="ida-viru maakond",
            tags=("place:narva", "country:ee"),
        ),
        "narva",
        "нарва",
    )
    _aliases(
        _city_snapshot(
            label="Pärnu, EE",
            latitude=58.385,
            longitude=24.497,
            settlement="pärnu",
            region="pärnu maakond",
            tags=("place:parnu", "country:ee"),
        ),
        "pärnu",
        "parnu",
        "пярну",
    )
    _aliases(
        _city_snapshot(
            label="Kohtla-Järve, EE",
            latitude=59.398,
            longitude=27.273,
            settlement="kohtla-järve",
            region="ida-viru maakond",
            tags=("place:kohtla-jarve", "country:ee"),
        ),
        "kohtla-järve",
        "kohtla-jarve",
        "кохтла-ярве",
    )
    _aliases(
        _city_snapshot(
            label="Viljandi, EE",
            latitude=58.364,
            longitude=25.591,
            settlement="viljandi",
            region="viljandi maakond",
            tags=("place:viljandi", "country:ee"),
        ),
        "viljandi",
        "вильянди",
    )
    _aliases(
        _city_snapshot(
            label="Rakvere, EE",
            latitude=59.346,
            longitude=26.356,
            settlement="rakvere",
            region="lääne-viru maakond",
            tags=("place:rakvere", "country:ee"),
        ),
        "rakvere",
        "раквере",
    )
    _aliases(
        _city_snapshot(
            label="Maardu, EE",
            latitude=59.476,
            longitude=25.021,
            settlement="maardu",
            region="harju maakond",
            tags=("place:maardu", "country:ee"),
        ),
        "maardu",
        "маарду",
    )
    _aliases(
        _city_snapshot(
            label="Sillamäe, EE",
            latitude=59.399,
            longitude=27.763,
            settlement="sillamäe",
            region="ida-viru maakond",
            tags=("place:sillamae", "country:ee"),
        ),
        "sillamäe",
        "sillamae",
        "силламяэ",
    )
    _aliases(
        _city_snapshot(
            label="Võru, EE",
            latitude=57.834,
            longitude=27.019,
            settlement="võru",
            region="võru maakond",
            tags=("place:voru", "country:ee"),
        ),
        "võru",
        "voru",
        "выру",
    )

    _aliases(
        _district_snapshot(
            label="Kalamaja, Tallinn, EE",
            latitude=59.448,
            longitude=24.738,
            district="kalamaja",
            tags=("place:kalamaja", "place:tallinn", "country:ee"),
        ),
        "kalamaja",
        "каламая",
    )
    _aliases(
        _district_snapshot(
            label="Mustamäe, Tallinn, EE",
            latitude=59.408,
            longitude=24.685,
            district="mustamäe",
            tags=("place:mustamae", "place:tallinn", "country:ee"),
        ),
        "mustamäe",
        "mustamae",
        "мустамяэ",
    )
    _aliases(
        _district_snapshot(
            label="Lasnamäe, Tallinn, EE",
            latitude=59.437,
            longitude=24.858,
            district="lasnamäe",
            tags=("place:lasnamae", "place:tallinn", "country:ee"),
        ),
        "lasnamäe",
        "lasnamae",
        "ласнамяэ",
    )
    _aliases(
        _district_snapshot(
            label="Kristiine, Tallinn, EE",
            latitude=59.426,
            longitude=24.719,
            district="kristiine",
            tags=("place:kristiine", "place:tallinn", "country:ee"),
        ),
        "kristiine",
        "кристийне",
    )
    _aliases(
        _district_snapshot(
            label="Põhja-Tallinn, EE",
            latitude=59.454,
            longitude=24.698,
            district="põhja-tallinn",
            tags=("place:pohja-tallinn", "place:tallinn", "country:ee"),
        ),
        "põhja-tallinn",
        "pohja-tallinn",
        "пыхья-таллин",
    )
    _aliases(
        _district_snapshot(
            label="Haabersti, Tallinn, EE",
            latitude=59.428,
            longitude=24.649,
            district="haabersti",
            tags=("place:haabersti", "place:tallinn", "country:ee"),
        ),
        "haabersti",
        "хааберсти",
    )
    _aliases(
        _district_snapshot(
            label="Pirita, Tallinn, EE",
            latitude=59.469,
            longitude=24.834,
            district="pirita",
            tags=("place:pirita", "place:tallinn", "country:ee"),
        ),
        "pirita",
        "пирита",
    )
    _aliases(
        _district_snapshot(
            label="Nõmme, Tallinn, EE",
            latitude=59.377,
            longitude=24.684,
            district="nõmme",
            tags=("place:nomme", "place:tallinn", "country:ee"),
        ),
        "nõmme",
        "nomme",
        "нымме",
    )
    _aliases(
        _district_snapshot(
            label="Kesklinn, Tallinn, EE",
            latitude=59.437,
            longitude=24.7536,
            district="kesklinn",
            tags=("place:kesklinn", "place:tallinn", "country:ee"),
        ),
        "kesklinn",
        "кесклинн",
    )

    return lookup


_GEO_LOOKUP: dict[str, StoryGeoSnapshot] = _build_geo_lookup()
_GEO_LOOKUP_ORDER: tuple[str, ...] = tuple(
    sorted(_GEO_LOOKUP.keys(), key=len, reverse=True)
)


@dataclass(frozen=True)
class _EstoniaGeoLookup:
    """Demo stub: Estonia cities and Tallinn districts via alias dict (EN/ET/RU)."""

    provider_id: str = _PROVIDER_ID

    def resolve(self, original_query: str, *, canonical_key: str) -> StoryGeoSnapshot | None:
        del original_query
        for keyword in _GEO_LOOKUP_ORDER:
            if keyword in canonical_key:
                return _GEO_LOOKUP[keyword]
        return None


def default_provider_chain() -> tuple[GeoProvider, ...]:
    return (_EstoniaGeoLookup(),)
