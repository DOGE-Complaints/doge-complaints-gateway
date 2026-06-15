from __future__ import annotations

from dataclasses import dataclass

from core.projection.i18n import I18nText


@dataclass(frozen=True)
class ProjectionInput:
    """Domain-side payload consumed by the projection engine before SPA mapping."""

    issue_id: str
    status: str
    issue_type: str
    labels: tuple[str, ...]
    title: I18nText
    summary: I18nText | None
    description: I18nText
    institution: dict[str, str] | None = None
    created_at: str | None = None
    arweave_txid: str | None = None
    image_txid: str | None = None
    image_hash: str | None = None
    geo_lat: float | None = None
    geo_lon: float | None = None
    geo_normalized_label: str | None = None
    geo_admin_district: str | None = None
    geo_admin_settlement: str | None = None
    geo_admin_region: str | None = None
    geo_admin_country: str | None = None
    original_locale: tuple[str, ...] = ()
