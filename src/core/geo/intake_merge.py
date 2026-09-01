"""SSR-23: pack geo_intake mode + merge client geo_detail with location_query resolve."""

from __future__ import annotations

from typing import Any

from core.domain import StoryGeoSnapshot
from core.intake.contracts import GeoDetail, GeoDetailAddress, geo_detail_has_values
from core.intake import IntakeValidationError
from core.schema.contracts import GeoIntakeBlock


def enforce_geo_intake_mode(
    *,
    geo_intake: GeoIntakeBlock,
    location_query: str,
    detail: GeoDetail | None,
) -> None:
    """Raise IntakeValidationError when pack mode is not satisfied."""
    has_query = bool(location_query.strip())
    has_detail = geo_detail_has_values(detail)
    mode = geo_intake.mode
    if mode == "optional":
        return
    if mode == "require_location_or_detail":
        if not has_query and not has_detail:
            raise IntakeValidationError(
                "geo_intake requires location_query or geo_detail."
            )
        return
    if mode == "require_detail":
        if not has_detail:
            raise IntakeValidationError("geo_intake requires geo_detail.")
        return
    raise IntakeValidationError(f"Unknown geo_intake.mode: {mode}.")


def merge_client_geo_detail(
    provider: StoryGeoSnapshot | None,
    detail: GeoDetail | None,
    *,
    merge: bool,
) -> StoryGeoSnapshot | None:
    """Overlay client detail when merge=True. No invented coords on address-only miss."""
    if not merge or not geo_detail_has_values(detail) or detail is None:
        return provider
    addr = detail.address
    if provider is None:
        if detail.latitude is None or detail.longitude is None:
            return None
        return StoryGeoSnapshot(
            normalized_label=detail.normalized_label or "client",
            latitude=detail.latitude,
            longitude=detail.longitude,
            confidence=detail.confidence if detail.confidence is not None else 1.0,
            provider=detail.provider or "client",
            admin_district=addr.district if addr is not None else None,
            admin_settlement=addr.settlement if addr is not None else None,
            admin_region=addr.region if addr is not None else None,
            admin_country=addr.country if addr is not None else None,
            street=addr.street if addr is not None else None,
            house=addr.house if addr is not None else None,
            house_range=addr.house_range if addr is not None else None,
            houses=addr.houses if addr is not None else (),
            address_line=_address_line(detail, addr, None),
            detail_level=detail.detail_level,
        )
    return StoryGeoSnapshot(
        normalized_label=detail.normalized_label or provider.normalized_label,
        latitude=detail.latitude if detail.latitude is not None else provider.latitude,
        longitude=(
            detail.longitude if detail.longitude is not None else provider.longitude
        ),
        confidence=(
            detail.confidence if detail.confidence is not None else provider.confidence
        ),
        provider=detail.provider or provider.provider,
        cluster_tags=provider.cluster_tags,
        admin_district=_overlay(addr.district if addr else None, provider.admin_district),
        admin_settlement=_overlay(
            addr.settlement if addr else None, provider.admin_settlement
        ),
        admin_region=_overlay(addr.region if addr else None, provider.admin_region),
        admin_country=_overlay(addr.country if addr else None, provider.admin_country),
        street=_overlay(addr.street if addr else None, provider.street),
        house=_overlay(addr.house if addr else None, provider.house),
        house_range=_overlay(addr.house_range if addr else None, provider.house_range),
        houses=addr.houses if addr is not None and addr.houses else provider.houses,
        address_line=_address_line(detail, addr, provider),
        detail_level=_overlay(detail.detail_level, provider.detail_level),
    )


def _overlay(client: str | None, provider: str | None) -> str | None:
    return client if client else provider


def _address_line(
    detail: GeoDetail,
    addr: GeoDetailAddress | None,
    provider: StoryGeoSnapshot | None,
) -> str | None:
    if detail.normalized_label:
        return detail.normalized_label
    parts: list[str] = []
    if addr is not None:
        if addr.street:
            parts.append(addr.street)
        if addr.house:
            parts.append(addr.house)
        elif addr.house_range:
            parts.append(addr.house_range)
        elif addr.houses:
            parts.append(", ".join(addr.houses))
    if parts:
        return ", ".join(parts)
    if provider is not None:
        return provider.address_line
    return None


def mirror_geo_to_payload(
    payload: dict[str, Any],
    *,
    geo: StoryGeoSnapshot | None,
    detail: GeoDetail | None,
) -> None:
    """Write geo.* leaves for exact-lenses. Mutates payload in place."""
    existing = payload.get("geo")
    geo_obj: dict[str, Any] = dict(existing) if isinstance(existing, dict) else {}
    if geo is not None:
        if geo.admin_district:
            geo_obj["district"] = geo.admin_district
        if geo.admin_settlement:
            geo_obj["settlement"] = geo.admin_settlement
        if geo.admin_region:
            geo_obj["region"] = geo.admin_region
        if geo.admin_country:
            geo_obj["country"] = geo.admin_country
        if geo.street:
            geo_obj["street"] = geo.street
        if geo.house:
            geo_obj["house"] = geo.house
        if geo.house_range:
            geo_obj["house_range"] = geo.house_range
        if geo.houses:
            geo_obj["houses"] = list(geo.houses)
        if geo.detail_level:
            geo_obj["detail_level"] = geo.detail_level
    addr = detail.address if detail is not None else None
    if addr is not None:
        if addr.district:
            geo_obj["district"] = addr.district
        if addr.settlement:
            geo_obj["settlement"] = addr.settlement
        if addr.region:
            geo_obj["region"] = addr.region
        if addr.country:
            geo_obj["country"] = addr.country
        if addr.street:
            geo_obj["street"] = addr.street
        if addr.house:
            geo_obj["house"] = addr.house
        if addr.house_range:
            geo_obj["house_range"] = addr.house_range
        if addr.houses:
            geo_obj["houses"] = list(addr.houses)
    if detail is not None and detail.detail_level:
        geo_obj["detail_level"] = detail.detail_level
    if geo_obj:
        payload["geo"] = geo_obj
