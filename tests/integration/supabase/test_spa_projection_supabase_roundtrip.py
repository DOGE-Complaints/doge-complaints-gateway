from __future__ import annotations

import os
from uuid import uuid4

import pytest  # pyright: ignore[reportMissingImports]

from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseIssueProjectionStore


def _require_live_http_env() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_TEST_URL", "").strip()
    key = os.environ.get("SUPABASE_TEST_SERVICE_ROLE", "").strip()
    if not url or not key:
        pytest.skip("SUPABASE_TEST_URL/SUPABASE_TEST_SERVICE_ROLE are not configured.")
    return url, key


def test_spa_projection_roundtrip_via_dashboard_view() -> None:
    supabase_url, service_role_key = _require_live_http_env()
    db = SupabaseDatabase.from_http(
        supabase_url=supabase_url,
        service_role_key=service_role_key,
    )
    store = SupabaseIssueProjectionStore(db)
    issue_id = f"test-{uuid4()}"
    store.save_projection(
        issue_id=issue_id,
        status="promoted",
        policy_version="m2.spa_issue_derivation.v1",
        payload={
            "type": "improvement",
            "title": {"en": "Road light issue", "et": "Teevalgusti mure", "ru": "Проблема с освещением"},
            "summary": {"en": "Street light broken", "et": "Valgusti katki", "ru": "Фонарь сломан"},
            "description": {"en": "Broken light on district road", "et": "Katkine valgusti", "ru": "Сломан фонарь"},
            "labels": ["infrastructure"],
        },
    )

    rows = db._request(
        method="GET",
        path="/rest/v1/issues_dashboard",
        params={
            "select": "issue_id,status,type,title_en",
            "issue_id": db._eq_filter(issue_id),
            "limit": "1",
        },
    )

    assert rows
    row = rows[0]
    assert row["issue_id"] == issue_id
    assert row["status"] == "promoted"
    assert row["type"] == "improvement"
    assert row["title_en"] == "Road light issue"
