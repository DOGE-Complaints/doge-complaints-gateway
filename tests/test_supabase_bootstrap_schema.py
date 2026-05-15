from __future__ import annotations

from pathlib import Path

_BOOTSTRAP_SQL = Path("supabase/bootstrap/000_full_init.sql")
_MIGRATION_GEO_EMB = Path(
    "supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql"
)


def test_supabase_bootstrap_contains_cluster_persistence_tables() -> None:
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text(encoding="utf-8")
    assert "create table if not exists public.story_signals" in sql
    assert "create table if not exists public.cluster_memberships" in sql
    assert "idx_story_signals_policy" in sql
    assert "idx_cluster_memberships_cluster" in sql


def test_supabase_bootstrap_contains_cluster_persistence_rls_policies() -> None:
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text(encoding="utf-8")
    assert "alter table public.story_signals enable row level security;" in sql
    assert "alter table public.cluster_memberships enable row level security;" in sql
    assert "create policy story_signals_service_role_all" in sql
    assert "create policy cluster_memberships_service_role_all" in sql


def test_supabase_bootstrap_contains_stories_geo_columns_gap07() -> None:
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    assert "geo_normalized_label" in sql
    assert "geo_latitude" in sql
    assert "geo_longitude" in sql
    assert "geo_confidence" in sql
    assert "geo_provider" in sql
    assert "geo_cluster_tags_json" in sql


def test_supabase_bootstrap_embedding_columns_nullable_gap08_variant_a() -> None:
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    assert "public.story_embeddings" in sql
    assert "public.doge_issue_embeddings" in sql
    assert "alter column embedding drop not null" in sql


def test_supabase_bootstrap_stories_geo_column_types_gap07_ddl() -> None:
    """§5.1 implementation-report: types + cluster_tags column definition (not only names)."""
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    assert "geo_latitude double precision" in sql
    assert "geo_longitude double precision" in sql
    assert "geo_confidence double precision" in sql
    assert "geo_cluster_tags_json text not null default '[]'" in sql


def test_migration_bootstrap_geo_embedding_file_present_gap07_gap08() -> None:
    assert _MIGRATION_GEO_EMB.is_file()
    mig = _MIGRATION_GEO_EMB.read_text(encoding="utf-8")
    assert "geo_normalized_label" in mig
    assert "alter column embedding drop not null" in mig


def test_bootstrap_stories_narrative_extension_columns_m2_02_06() -> None:
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    assert "narrative_title_hint_et" in sql
    assert "narrative_consistency_notes" in sql


def test_migration_stories_narrative_extensions_file_exists() -> None:
    p = Path("supabase/migrations/20260511_1200_m2_02_stories_narrative_extensions.sql")
    assert p.is_file()
    assert "narrative_summary_json" in p.read_text(encoding="utf-8")
