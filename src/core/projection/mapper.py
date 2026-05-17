from __future__ import annotations

from core.projection.dto import DOGEIssue
from core.projection.i18n import I18nText
from core.projection.input import ProjectionInput
from core.projection.validation import validate_governed_enums, validate_optional_tx_fields


def apply_summary_fallback(title: I18nText, summary: I18nText | None) -> I18nText:
    """If a locale in summary is empty, use title for that locale (requirements/09)."""
    if summary is None:
        return title
    return I18nText(
        et=summary.et.strip() or title.et,
        ru=summary.ru.strip() or title.ru,
        en=summary.en.strip() or title.en,
    )


def project_distinct_issue(data: ProjectionInput) -> DOGEIssue:
    """Map governed domain input to SPA Issue projection."""
    validate_governed_enums(status=data.status, issue_type=data.issue_type, labels=data.labels)
    validate_optional_tx_fields(arweave_txid=data.arweave_txid, image_txid=data.image_txid)

    summary = apply_summary_fallback(data.title, data.summary)

    geo: dict[str, object] | None = None
    if data.geo_lat is not None and data.geo_lon is not None:
        geo = {
            "lat": data.geo_lat,
            "lon": data.geo_lon,
        }
        if data.geo_normalized_label:
            geo["label"] = data.geo_normalized_label
        if data.geo_admin_district:
            geo["district"] = data.geo_admin_district
        if data.geo_admin_settlement:
            geo["settlement"] = data.geo_admin_settlement
        if data.geo_admin_region:
            geo["region"] = data.geo_admin_region
        if data.geo_admin_country:
            geo["country"] = data.geo_admin_country

    return DOGEIssue(
        id=data.issue_id,
        status=data.status,
        type=data.issue_type,
        labels=tuple(data.labels),
        title=data.title.as_dict(),
        summary=summary.as_dict(),
        description=data.description.as_dict(),
        institution=data.institution,
        created_at=data.created_at,
        arweave_txid=data.arweave_txid,
        image_txid=data.image_txid,
        image_hash=data.image_hash,
        geo=geo,
    )
