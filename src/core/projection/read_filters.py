from __future__ import annotations

import json
from typing import Any

from core.geo.scope import normalize_geo_token


def _clean_str_list(values: list[str] | None) -> list[str] | None:
    if values is None:
        return None
    cleaned = [item.strip() for item in values if item and item.strip()]
    return cleaned or None


def any_geo_filter_active(
    *,
    geo_lat_min: float | None = None,
    geo_lat_max: float | None = None,
    geo_lon_min: float | None = None,
    geo_lon_max: float | None = None,
    geo_district: list[str] | None = None,
    geo_settlement: list[str] | None = None,
    geo_region: list[str] | None = None,
    geo_country: list[str] | None = None,
    geo_postal_code: list[str] | None = None,
) -> bool:
    if any(
        value is not None
        for value in (
            geo_lat_min,
            geo_lat_max,
            geo_lon_min,
            geo_lon_max,
        )
    ):
        return True
    return any(
        _clean_str_list(values)
        for values in (
            geo_district,
            geo_settlement,
            geo_region,
            geo_country,
            geo_postal_code,
        )
    )


def _payload_geo(payload: dict[str, object]) -> dict[str, object] | None:
    geo = payload.get("geo")
    return geo if isinstance(geo, dict) else None


def _matches_geo_filters(
    payload: dict[str, object],
    *,
    geo_lat_min: float | None,
    geo_lat_max: float | None,
    geo_lon_min: float | None,
    geo_lon_max: float | None,
    geo_district: list[str] | None,
    geo_settlement: list[str] | None,
    geo_region: list[str] | None,
    geo_country: list[str] | None,
    geo_postal_code: list[str] | None,
) -> bool:
    geo = _payload_geo(payload)
    if geo is None:
        return not any_geo_filter_active(
            geo_lat_min=geo_lat_min,
            geo_lat_max=geo_lat_max,
            geo_lon_min=geo_lon_min,
            geo_lon_max=geo_lon_max,
            geo_district=geo_district,
            geo_settlement=geo_settlement,
            geo_region=geo_region,
            geo_country=geo_country,
            geo_postal_code=geo_postal_code,
        )

    lat = geo.get("lat")
    lon = geo.get("lon")
    if geo_lat_min is not None or geo_lat_max is not None or geo_lon_min is not None or geo_lon_max is not None:
        try:
            lat_f = float(lat) if lat is not None else None
            lon_f = float(lon) if lon is not None else None
        except (TypeError, ValueError):
            return False
        if lat_f is None or lon_f is None:
            return False
        if geo_lat_min is not None and lat_f < geo_lat_min:
            return False
        if geo_lat_max is not None and lat_f > geo_lat_max:
            return False
        if geo_lon_min is not None and lon_f < geo_lon_min:
            return False
        if geo_lon_max is not None and lon_f > geo_lon_max:
            return False

    district_values = _clean_str_list(geo_district)
    if district_values:
        token = normalize_geo_token(str(geo.get("district", "")))
        if not any(normalize_geo_token(value) == token for value in district_values):
            return False

    settlement_values = _clean_str_list(geo_settlement)
    if settlement_values:
        token = normalize_geo_token(str(geo.get("settlement", "")))
        if not any(normalize_geo_token(value) == token for value in settlement_values):
            return False

    region_values = _clean_str_list(geo_region)
    if region_values:
        token = normalize_geo_token(str(geo.get("region", "")))
        if not any(normalize_geo_token(value) == token for value in region_values):
            return False

    country_values = _clean_str_list(geo_country)
    if country_values:
        token = normalize_geo_token(str(geo.get("country", "")))
        if not any(normalize_geo_token(value) == token for value in country_values):
            return False

    postal_values = _clean_str_list(geo_postal_code)
    if postal_values:
        token = normalize_geo_token(str(geo.get("postal_code", "")))
        if not token or not any(normalize_geo_token(value) == token for value in postal_values):
            return False

    return True


def _institution_payload_matches(payload_institution: object, filter_value: str) -> bool:
    """Match list filter string against i18n dict or legacy scalar payload."""
    if isinstance(payload_institution, dict):
        normalized = filter_value.strip()
        return any(
            str(payload_institution.get(lang, "")).strip() == normalized
            for lang in ("et", "ru", "en")
        )
    return payload_institution == filter_value


def _matches_post_fetch_filters(
    payload: dict[str, object],
    *,
    issue_type: str | None,
    labels: list[str] | None,
    institution: str | None,
    geo_lat_min: float | None,
    geo_lat_max: float | None,
    geo_lon_min: float | None,
    geo_lon_max: float | None,
    geo_district: list[str] | None,
    geo_settlement: list[str] | None,
    geo_region: list[str] | None,
    geo_country: list[str] | None,
    geo_postal_code: list[str] | None,
) -> bool:
    if issue_type is not None and payload.get("type") != issue_type:
        return False
    label_values = _clean_str_list(labels)
    if label_values:
        payload_labels = payload.get("labels")
        if not isinstance(payload_labels, list):
            return False
        if not any(label in payload_labels for label in label_values):
            return False
    if institution is not None and not _institution_payload_matches(
        payload.get("institution"), institution
    ):
        return False
    return _matches_geo_filters(
        payload,
        geo_lat_min=geo_lat_min,
        geo_lat_max=geo_lat_max,
        geo_lon_min=geo_lon_min,
        geo_lon_max=geo_lon_max,
        geo_district=geo_district,
        geo_settlement=geo_settlement,
        geo_region=geo_region,
        geo_country=geo_country,
        geo_postal_code=geo_postal_code,
    )


def merge_projection_columns(
    *,
    issue_id: str,
    row_status: str,
    payload: dict[str, object],
    created_at: str | None = None,
) -> dict[str, object]:
    """Column-as-truth merge: DB columns override payload_json for id/status/created_at."""
    out = dict(payload)
    out["id"] = issue_id
    out["status"] = row_status
    out["created_at"] = created_at or ""
    return out


def filter_projection_rows(
    rows: list[tuple[str, str, dict[str, object], str]],
    *,
    status: list[str] | None = None,
    issue_type: str | None = None,
    labels: list[str] | None = None,
    institution: str | None = None,
    created_after: str | None = None,
    created_before: str | None = None,
    geo_lat_min: float | None = None,
    geo_lat_max: float | None = None,
    geo_lon_min: float | None = None,
    geo_lon_max: float | None = None,
    geo_district: list[str] | None = None,
    geo_settlement: list[str] | None = None,
    geo_region: list[str] | None = None,
    geo_country: list[str] | None = None,
    geo_postal_code: list[str] | None = None,
) -> list[dict[str, object]]:
    status_values = _clean_str_list(status)
    result: list[dict[str, object]] = []
    for issue_id, row_status, payload, created_at in rows:
        if status_values and row_status not in status_values:
            continue
        if created_after and created_at < created_after:
            continue
        if created_before and created_at > created_before:
            continue
        if not _matches_post_fetch_filters(
            payload,
            issue_type=issue_type,
            labels=labels,
            institution=institution,
            geo_lat_min=geo_lat_min,
            geo_lat_max=geo_lat_max,
            geo_lon_min=geo_lon_min,
            geo_lon_max=geo_lon_max,
            geo_district=geo_district,
            geo_settlement=geo_settlement,
            geo_region=geo_region,
            geo_country=geo_country,
            geo_postal_code=geo_postal_code,
        ):
            continue
        result.append(
            merge_projection_columns(
                issue_id=issue_id,
                row_status=row_status,
                payload=payload,
                created_at=created_at,
            )
        )
    return result


def parse_payload_json(raw: object) -> dict[str, object]:
    if isinstance(raw, dict):
        return dict(raw)
    if isinstance(raw, str):
        loaded = json.loads(raw)
        if isinstance(loaded, dict):
            return dict(loaded)
    raise ValueError("payload_json must decode to an object.")
