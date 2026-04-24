from __future__ import annotations

import os

import pytest  # pyright: ignore[reportMissingImports]

from core.infrastructure.db_supabase import SupabaseDatabase


def _require_live_dsn() -> str:
    dsn = os.environ.get("SUPABASE_TEST_DATABASE_URL", "").strip()
    if not dsn:
        pytest.skip("SUPABASE_TEST_DATABASE_URL is not configured for live integration.")
    return dsn


def test_supabase_connectivity_and_schema() -> None:
    db = SupabaseDatabase.from_url(_require_live_dsn())
    assert db.healthcheck() is True
    assert db.required_tables_ready() is True
