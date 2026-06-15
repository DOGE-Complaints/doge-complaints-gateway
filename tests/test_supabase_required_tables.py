"""Regression guards for Supabase readiness table set (GW-L10N-03 T08)."""

from __future__ import annotations

from core.infrastructure.db_supabase import REQUIRED_READINESS_TABLES


def test_label_translation_misses_not_in_required_readiness_tables() -> None:
    assert "label_translation_misses" not in REQUIRED_READINESS_TABLES


def test_required_readiness_tables_includes_core_intake_tables() -> None:
    assert {"stories", "idempotency_keys", "issue_story_links"}.issubset(
        REQUIRED_READINESS_TABLES
    )
