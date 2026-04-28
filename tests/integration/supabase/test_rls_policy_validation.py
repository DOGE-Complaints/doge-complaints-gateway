from __future__ import annotations

import os

import pytest  # pyright: ignore[reportMissingImports]

from core.infrastructure.db_supabase import SupabaseDatabase


def _require_live_http_env() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_TEST_URL", "").strip()
    key = os.environ.get("SUPABASE_TEST_SERVICE_ROLE", "").strip()
    if not url or not key:
        pytest.skip("SUPABASE_TEST_URL/SUPABASE_TEST_SERVICE_ROLE are not configured.")
    return url, key


def test_service_role_policy_probe() -> None:
    supabase_url, service_role_key = _require_live_http_env()
    db = SupabaseDatabase.from_http(
        supabase_url=supabase_url,
        service_role_key=service_role_key,
    )
    assert db.service_role_policy_probe() is True
