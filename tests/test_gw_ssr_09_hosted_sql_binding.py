"""GW-SSR-09 T01: hosted SQL artifact matches ``_STORIES_BINDING_COLUMNS``.

Live Railway apply is operator/deploy, not overnight proof (runbook §6.2 / G9).
"""

from __future__ import annotations

import inspect
import re
from pathlib import Path

from core.infrastructure.db_supabase import REQUIRED_READINESS_TABLES, SupabaseDatabase

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (
    GATEWAY_ROOT
    / "supabase"
    / "migrations"
    / "20260828_1400_gw_ssr_02_stories_schema_binding.sql"
)
_BINDING = frozenset(SupabaseDatabase._STORIES_BINDING_COLUMNS)


def test_binding_migration_file_exists() -> None:
    assert MIGRATION.is_file()


def test_sql_six_add_column_names_match_binding_frozenset() -> None:
    text = MIGRATION.read_text(encoding="utf-8")
    added = set(re.findall(r"add column if not exists (\w+)", text, flags=re.IGNORECASE))
    assert added == set(_BINDING)
    assert "drop table" not in text.lower()
    assert "drop column" not in text.lower()


def test_required_columns_ready_source_omits_binding_names() -> None:
    source = inspect.getsource(SupabaseDatabase.required_columns_ready)
    for name in _BINDING:
        assert name not in source
    assert "story_dimensions" not in REQUIRED_READINESS_TABLES
