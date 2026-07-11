"""REQ-39 Zone L: offline HTTP mock contract for SupabaseIssueProjectionStore."""

from __future__ import annotations

import json
from typing import Any

import pytest

from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseIssueProjectionStore
from core.projection.columnar_storage import COLUMNAR_ROW_SELECT
from core.projection.read_filters import parse_payload_json


def _columnar_mock_row() -> dict[str, object]:
    return {
        "issue_id": "issue-mock-1",
        "status": "PUBLISHED",
        "issue_type": "INCIDENT",
        "labels_json": ["infrastructure"],
        "title_json": {"en": "Mock"},
        "summary_json": {"en": "Summary"},
        "description_json": {"en": "Description"},
        "institution_json": None,
        "geo_json": {"district": "põhjatallinn", "settlement": "tallinn"},
        "original_locale_json": [],
        "arweave_txid": None,
        "image_txid": None,
        "image_hash": None,
        "created_at": "2026-05-01T12:00:00+00:00",
    }


def test_l_supa_list_projections_gets_doge_issues_with_expected_select(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def _mock_request(
        *,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        json_body: Any = None,
        prefer: str | None = None,
    ) -> list[dict[str, object]]:
        captured["method"] = method
        captured["path"] = path
        captured["params"] = dict(params or {})
        captured["prefer"] = prefer
        assert json_body is None
        return [_columnar_mock_row()]

    db = SupabaseDatabase(
        base_url="https://example.supabase.co",
        service_role_key="secret",
    )
    store = SupabaseIssueProjectionStore(db)
    monkeypatch.setattr(db, "_request", _mock_request)
    rows = store.list_projections(geo_district=["põhja-tallinn"])

    assert captured["method"] == "GET"
    assert captured["path"] == "/rest/v1/doge_issues"
    assert captured["params"]["select"] == COLUMNAR_ROW_SELECT
    assert captured["params"]["order"] == "created_at.desc"
    assert len(rows) == 1
    assert rows[0]["id"] == "issue-mock-1"
    geo = rows[0].get("geo")
    assert isinstance(geo, dict)


def test_l_supa_post_fetch_filter_applied_after_http_fetch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = SupabaseDatabase(
        base_url="https://example.supabase.co",
        service_role_key="secret",
    )
    store = SupabaseIssueProjectionStore(db)

    def _mock_request(
        *,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        json_body: Any = None,
        prefer: str | None = None,
    ) -> list[dict[str, object]]:
        assert method == "GET"
        assert path == "/rest/v1/doge_issues"
        return [
            {
                "issue_id": "match",
                "status": "PUBLISHED",
                "issue_type": "INCIDENT",
                "labels_json": [],
                "title_json": {"en": "t"},
                "summary_json": {"en": "s"},
                "description_json": {"en": "d"},
                "institution_json": None,
                "geo_json": {"country": "EE"},
                "original_locale_json": [],
                "arweave_txid": None,
                "image_txid": None,
                "image_hash": None,
                "created_at": "2026-05-01T00:00:00+00:00",
            },
            {
                "issue_id": "skip",
                "status": "PUBLISHED",
                "issue_type": "INCIDENT",
                "labels_json": [],
                "title_json": {"en": "t"},
                "summary_json": {"en": "s"},
                "description_json": {"en": "d"},
                "institution_json": None,
                "geo_json": {"country": "FI"},
                "original_locale_json": [],
                "arweave_txid": None,
                "image_txid": None,
                "image_hash": None,
                "created_at": "2026-05-01T00:00:00+00:00",
            },
        ]

    monkeypatch.setattr(db, "_request", _mock_request)
    rows = store.list_projections(geo_country=["ee"])
    ids = {str(r["id"]) for r in rows}
    assert ids == {"match"}


def test_l_supa_save_projection_writes_columnar_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def _mock_request(
        *,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        json_body: Any = None,
        prefer: str | None = None,
    ) -> list[dict[str, object]]:
        captured["method"] = method
        captured["path"] = path
        captured["json_body"] = json_body
        return []

    db = SupabaseDatabase(
        base_url="https://example.supabase.co",
        service_role_key="secret",
    )
    store = SupabaseIssueProjectionStore(db)
    monkeypatch.setattr(db, "_request", _mock_request)
    store.save_projection(
        issue_id="issue-save-1",
        status="PUBLISHED",
        payload={
            "type": "INCIDENT",
            "labels": ["infra"],
            "title": {"en": "Title"},
            "summary": {"en": "Summary"},
            "description": {"en": "Description"},
        },
        policy_version="test.policy.v1",
    )
    assert captured["method"] == "POST"
    row = captured["json_body"][0]
    assert "payload_json" not in row
    assert row["issue_type"] == "INCIDENT"
    assert row["labels_json"] == ["infra"]


def test_l_supa_parse_payload_json_string_shape() -> None:
    raw = json.dumps({"id": "x", "status": "PUBLISHED", "type": "INCIDENT", "labels": []})
    parsed = parse_payload_json(raw)
    assert parsed["id"] == "x"
