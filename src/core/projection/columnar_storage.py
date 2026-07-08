"""D-RC-5 columnar storage mapping for doge_issues projection rows."""

from __future__ import annotations

import json

from core.projection.read_filters import canonicalize_issue_type_on_read, parse_payload_json

COLUMNAR_ROW_SELECT = (
    "issue_id,status,created_at,issue_type,labels_json,title_json,summary_json,"
    "description_json,institution_json,geo_json,original_locale_json,"
    "arweave_txid,image_txid,image_hash"
)

_IDENTITY_ROW_FIELDS = frozenset({"issue_id", "status", "created_at"})

DOGE_ISSUES_COLUMNAR_READINESS_COLUMNS = frozenset(
    field.strip()
    for field in COLUMNAR_ROW_SELECT.split(",")
    if field.strip() and field.strip() not in _IDENTITY_ROW_FIELDS
)

_OPTIONAL_SCALARS = ("arweave_txid", "image_txid", "image_hash")


def _parse_json_field(raw: object, *, default: object) -> object:
    if raw is None:
        return default
    if isinstance(raw, (dict, list)):
        return raw
    if isinstance(raw, str):
        if not raw.strip():
            return default
        loaded = json.loads(raw)
        return loaded if loaded is not None else default
    return default


def _is_columnar_row_populated(row: dict[str, object]) -> bool:
    issue_type = row.get("issue_type")
    if isinstance(issue_type, str) and issue_type.strip():
        return True
    title = _parse_json_field(row.get("title_json"), default={})
    return bool(title)


def payload_to_storage_fields(payload: dict[str, object]) -> dict[str, object]:
    """Extract typed column values from a public issue dict (excludes id/status/created_at)."""
    institution = payload.get("institution")
    geo = payload.get("geo")
    original_locale = payload.get("original_locale")
    labels = payload.get("labels")
    fields: dict[str, object] = {
        "issue_type": str(payload.get("type", "IMPROVEMENT")),
        "labels_json": list(labels) if isinstance(labels, list) else [],
        "title_json": dict(payload["title"]) if isinstance(payload.get("title"), dict) else {},
        "summary_json": dict(payload["summary"]) if isinstance(payload.get("summary"), dict) else {},
        "description_json": (
            dict(payload["description"]) if isinstance(payload.get("description"), dict) else {}
        ),
        "institution_json": dict(institution) if isinstance(institution, dict) else None,
        "geo_json": dict(geo) if isinstance(geo, dict) else None,
        "original_locale_json": (
            list(original_locale) if isinstance(original_locale, list) else []
        ),
    }
    for scalar in _OPTIONAL_SCALARS:
        value = payload.get(scalar)
        fields[scalar] = str(value) if value is not None and str(value).strip() else None
    return fields


def storage_fields_to_sqlite_values(fields: dict[str, object]) -> dict[str, object]:
    """Serialize json columns to TEXT for SQLite binds."""
    out = dict(fields)
    for key in (
        "labels_json",
        "title_json",
        "summary_json",
        "description_json",
        "institution_json",
        "geo_json",
        "original_locale_json",
    ):
        value = out.get(key)
        if value is None:
            out[key] = None
        else:
            out[key] = json.dumps(value)
    return out


def payload_body_from_storage_row(
    row: dict[str, object],
    *,
    legacy_payload_json: object | None = None,
) -> dict[str, object]:
    """Build payload dict (without id/status/created_at) from columnar row or legacy blob."""
    if _is_columnar_row_populated(row):
        out: dict[str, object] = {
            "type": row.get("issue_type") or "IMPROVEMENT",
            "labels": _parse_json_field(row.get("labels_json"), default=[]),
            "title": _parse_json_field(row.get("title_json"), default={}),
            "summary": _parse_json_field(row.get("summary_json"), default={}),
            "description": _parse_json_field(row.get("description_json"), default={}),
        }
        institution = _parse_json_field(row.get("institution_json"), default=None)
        if isinstance(institution, dict) and institution:
            out["institution"] = institution
        geo = _parse_json_field(row.get("geo_json"), default=None)
        if isinstance(geo, dict) and geo:
            out["geo"] = geo
        original_locale = _parse_json_field(row.get("original_locale_json"), default=[])
        if isinstance(original_locale, list) and original_locale:
            out["original_locale"] = original_locale
        for scalar in _OPTIONAL_SCALARS:
            value = row.get(scalar)
            if value is not None and str(value).strip():
                out[scalar] = str(value)
        return out
    if legacy_payload_json is not None:
        legacy = parse_payload_json(legacy_payload_json)
        return {
            key: value
            for key, value in legacy.items()
            if key not in ("id", "status", "created_at")
        }
    return {}


def assemble_public_issue_from_storage_row(
    row: dict[str, object],
    *,
    legacy_payload_json: object | None = None,
) -> dict[str, object]:
    """Assemble full public issue dict from a DB row."""
    issue_id = str(row["issue_id"])
    row_status = str(row["status"])
    created_at = str(row.get("created_at") or "")
    payload = payload_body_from_storage_row(
        row,
        legacy_payload_json=legacy_payload_json,
    )
    payload["id"] = issue_id
    payload["status"] = row_status
    payload["created_at"] = created_at
    payload["type"] = canonicalize_issue_type_on_read(
        payload.get("type"),
        issue_id=issue_id,
    )
    return payload


def sqlite_row_to_dict(
    *,
    issue_id: str,
    row_status: str,
    created_at: str,
    issue_type: object,
    labels_json: object,
    title_json: object,
    summary_json: object,
    description_json: object,
    institution_json: object,
    geo_json: object,
    original_locale_json: object,
    arweave_txid: object,
    image_txid: object,
    image_hash: object,
) -> dict[str, object]:
    return {
        "issue_id": issue_id,
        "status": row_status,
        "created_at": created_at,
        "issue_type": issue_type,
        "labels_json": labels_json,
        "title_json": title_json,
        "summary_json": summary_json,
        "description_json": description_json,
        "institution_json": institution_json,
        "geo_json": geo_json,
        "original_locale_json": original_locale_json,
        "arweave_txid": arweave_txid,
        "image_txid": image_txid,
        "image_hash": image_hash,
    }
