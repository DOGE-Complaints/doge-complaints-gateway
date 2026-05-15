from __future__ import annotations

from pathlib import Path

from core.infrastructure.db_supabase import _STORY_SELECT_FIELDS

# Roadmap: fuller cross-layer suite — docs/requirements/req-cross-layer-contract-testing.md (C-xx).


def test_story_select_field_names_exist_in_bootstrap_sql() -> None:
    """§5.6 MVP: every column in _STORY_SELECT_FIELDS appears in bootstrap DDL for public.stories."""
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text(encoding="utf-8")
    columns = [c.strip() for c in _STORY_SELECT_FIELDS.split(",") if c.strip()]
    assert columns
    for col in columns:
        assert col in sql, f"missing column name {col!r} in 000_full_init.sql (drift vs db_supabase._STORY_SELECT_FIELDS)"
