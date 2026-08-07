"""GW-TAX-03 T08 — story_labels migration must declare story_id text (not UUID)."""

from __future__ import annotations

import re
from pathlib import Path

_MIGRATION = (
    Path(__file__).resolve().parents[1]
    / "supabase"
    / "migrations"
    / "20260714_1200_gw_tax_01_story_labels.sql"
)


def test_story_labels_migration_uses_text_fk_not_uuid() -> None:
    assert _MIGRATION.is_file(), f"missing migration: {_MIGRATION}"
    sql = _MIGRATION.read_text(encoding="utf-8")
    assert re.search(
        r"CREATE TABLE IF NOT EXISTS story_labels\s*\(",
        sql,
        re.IGNORECASE,
    ), "story_labels CREATE TABLE missing"
    assert re.search(
        r"story_id\s+text\s+NOT NULL\s+REFERENCES\s+stories\(story_id\)",
        sql,
        re.IGNORECASE,
    ), "expected story_id text FK to stories(story_id)"
    assert not re.search(
        r"story_id\s+UUID\b",
        sql,
        re.IGNORECASE,
    ), "story_id UUID must not appear in story_labels migration DDL"
