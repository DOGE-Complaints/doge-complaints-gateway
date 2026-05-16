from __future__ import annotations

from core.domain import StoryGeoSnapshot

GEO_FILTER_LEVELS: frozenset[str] = frozenset(
    {"district", "settlement", "region", "country"}
)
GEO_SCOPE_LEVELS: frozenset[str] = GEO_FILTER_LEVELS


class GeoScopeMismatchError(ValueError):
    """Raised when story geo is outside CLUSTER_GEO_SCOPE for this node."""


def normalize_geo_token(value: str | None) -> str:
    if value is None:
        return ""
    return "".join(ch for ch in value.strip().lower() if ch.isalnum())


def parse_cluster_geo_scope(raw: str | None) -> tuple[str, str] | None:
    if raw is None or not str(raw).strip():
        return None
    text = str(raw).strip().lower()
    if ":" not in text:
        raise ValueError(
            "Invalid CLUSTER_GEO_SCOPE. Expected format <level>:<value> "
            "(e.g. settlement:tallinn)."
        )
    level, value = text.split(":", 1)
    level = level.strip()
    value = value.strip()
    if level not in GEO_SCOPE_LEVELS:
        raise ValueError(
            f"Invalid CLUSTER_GEO_SCOPE level '{level}'. "
            f"Expected one of: {', '.join(sorted(GEO_SCOPE_LEVELS))}."
        )
    if not value:
        raise ValueError("Invalid CLUSTER_GEO_SCOPE. Value after ':' must be non-empty.")
    return level, value


def parse_cluster_geo_filter(raw: str) -> str:
    level = raw.strip().lower()
    if level == "any":
        level = "country"
    if level not in GEO_FILTER_LEVELS:
        raise ValueError(
            f"Invalid CLUSTER_GEO_FILTER '{raw}'. "
            f"Expected one of: {', '.join(sorted(GEO_FILTER_LEVELS))} (or legacy 'any')."
        )
    return level


def admin_value_for_level(geo: StoryGeoSnapshot, level: str) -> str | None:
    if level == "district":
        return geo.admin_district
    if level == "settlement":
        return geo.admin_settlement
    if level == "region":
        return geo.admin_region
    if level == "country":
        return geo.admin_country
    return None


def geo_matches_scope(
    geo: StoryGeoSnapshot | None,
    *,
    level: str,
    expected_value: str,
) -> bool:
    if geo is None:
        return False
    actual = admin_value_for_level(geo, level)
    if actual is None or not str(actual).strip():
        return False
    return normalize_geo_token(actual) == normalize_geo_token(expected_value)


def assert_geo_in_scope(
    geo: StoryGeoSnapshot | None,
    *,
    level: str,
    expected_value: str,
) -> None:
    if geo_matches_scope(geo, level=level, expected_value=expected_value):
        return
    raise GeoScopeMismatchError(
        f"Story location is outside node geo scope {level}:{expected_value}."
    )


def geo_filter_bucket(geo: StoryGeoSnapshot | None, geo_filter: str) -> str:
    level = parse_cluster_geo_filter(geo_filter)
    if geo is None:
        return "geo:agnostic"
    token = normalize_geo_token(admin_value_for_level(geo, level))
    if not token:
        return "geo:unknown"
    return f"geo:{level}:{token}"
