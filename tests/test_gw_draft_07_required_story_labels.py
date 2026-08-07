"""GW-DRAFT-07 T09 — story_labels must stay in REQUIRED_READINESS_TABLES."""

from __future__ import annotations

from core.infrastructure.db_supabase import REQUIRED_READINESS_TABLES


def test_required_readiness_tables_includes_story_labels() -> None:
    assert "story_labels" in REQUIRED_READINESS_TABLES
