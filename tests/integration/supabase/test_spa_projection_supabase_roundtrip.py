from __future__ import annotations

import os
from uuid import uuid4

import pytest  # pyright: ignore[reportMissingImports]

from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseIssueProjectionStore


def _require_live_dsn() -> str:
    dsn = os.environ.get("SUPABASE_TEST_DATABASE_URL", "").strip()
    if not dsn:
        pytest.skip("SUPABASE_TEST_DATABASE_URL is not configured for live integration.")
    return dsn


def test_spa_projection_roundtrip_via_dashboard_view() -> None:
    db = SupabaseDatabase.from_url(_require_live_dsn())
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

    with db._connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT issue_id, status, type, title_en
            FROM public.issues_dashboard
            WHERE issue_id = %(issue_id)s
            """,
            {"issue_id": issue_id},
        )
        row = cur.fetchone()

    assert row is not None
    assert row["issue_id"] == issue_id
    assert row["status"] == "promoted"
    assert row["type"] == "improvement"
    assert row["title_en"] == "Road light issue"
