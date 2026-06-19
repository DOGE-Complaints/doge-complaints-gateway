"""REQ-39 Zone L: offline HTTP mock contract for SupabaseIssueProjectionStore."""

from __future__ import annotations

import json
from typing import Any

import pytest

from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseIssueProjectionStore
from core.projection.read_filters import parse_payload_json


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
        return [
            {
                "issue_id": "issue-mock-1",
                "status": "PUBLISHED",
                "payload_json": {
                    "id": "issue-mock-1",
                    "status": "PUBLISHED",
                    "type": "INCIDENT",
                    "labels": ["infrastructure"],
                    "title": {"en": "Mock"},
                    "summary": {"en": "Summary"},
                    "description": {"en": "Description"},
                    "geo": {"district": "põhjatallinn", "settlement": "tallinn"},
                },
                "created_at": "2026-05-01T12:00:00+00:00",
            }
        ]

    db = SupabaseDatabase(
        base_url="https://example.supabase.co",
        service_role_key="secret",
    )
    store = SupabaseIssueProjectionStore(db)
    monkeypatch.setattr(db, "_request", _mock_request)
    rows = store.list_projections(geo_district=["põhja-tallinn"])

    assert captured["method"] == "GET"
    assert captured["path"] == "/rest/v1/doge_issues"
    assert captured["params"]["select"] == "issue_id,status,payload_json,created_at"
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
                "payload_json": {
                    "type": "INCIDENT",
                    "labels": [],
                    "geo": {"country": "EE"},
                },
                "created_at": "2026-05-01T00:00:00+00:00",
            },
            {
                "issue_id": "skip",
                "status": "PUBLISHED",
                "payload_json": {
                    "type": "INCIDENT",
                    "labels": [],
                    "geo": {"country": "FI"},
                },
                "created_at": "2026-05-01T00:00:00+00:00",
            },
        ]

    monkeypatch.setattr(db, "_request", _mock_request)
    rows = store.list_projections(geo_country=["ee"])
    ids = {str(r["id"]) for r in rows}
    assert ids == {"match"}


def test_l_supa_parse_payload_json_string_shape() -> None:
    raw = json.dumps({"id": "x", "status": "PUBLISHED", "type": "INCIDENT", "labels": []})
    parsed = parse_payload_json(raw)
    assert parsed["id"] == "x"
