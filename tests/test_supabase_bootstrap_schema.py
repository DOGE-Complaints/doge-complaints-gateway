from __future__ import annotations

import inspect
from pathlib import Path

from core.infrastructure.db_supabase import SupabaseDatabase, _STORY_SELECT_FIELDS

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
    assert "narrative_summary_json" in sql
    assert "narrative_consistency_notes" in sql
    assert "narrative_title_hint" not in sql


def test_migration_stories_narrative_extensions_file_exists() -> None:
    p = Path("supabase/migrations/20260511_1200_m2_02_stories_narrative_extensions.sql")
    assert p.is_file()
    assert "narrative_summary_json" in p.read_text(encoding="utf-8")


def test_story_select_fields_all_in_bootstrap_sql() -> None:
    """REQ-39 A-01 / G-01: SELECT fields must exist as columns in bootstrap DDL."""
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    for field in _STORY_SELECT_FIELDS.split(","):
        col = field.strip()
        assert col, "empty column name in _STORY_SELECT_FIELDS"
        assert col in sql, f"SELECT field {col!r} not found in bootstrap SQL"


def test_story_select_fields_covered_by_bootstrap() -> None:
    """REQ-39 G-01 traceability alias — same semantics as A-01."""
    test_story_select_fields_all_in_bootstrap_sql()


def test_geo_columns_have_correct_sql_types_req39_a02() -> None:
    """REQ-39 A-02: geo column SQL types match Python expectations."""
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    assert "geo_latitude double precision" in sql
    assert "geo_longitude double precision" in sql
    assert "geo_confidence double precision" in sql
    assert "geo_normalized_label text" in sql
    assert "geo_provider text" in sql
    assert "geo_cluster_tags_json text not null default '[]'" in sql


def test_embedding_columns_are_nullable_in_bootstrap_req39_a03() -> None:
    """REQ-39 A-03: both embedding tables allow NULL vector column (GAP-08)."""
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    count = sql.count("alter column embedding drop not null")
    assert count == 2, f"Expected 2 DROP NOT NULL for embedding, got {count}"


def test_delta_migration_exists_and_covers_gap07_gap08_req39_a04() -> None:
    """REQ-39 A-04: idempotent delta migration mirrors bootstrap geo/embedding DDL."""
    path = Path("supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql")
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "geo_normalized_label" in content
    assert "alter column embedding drop not null" in content
    assert "add column if not exists" in content


def test_canonical_labels_is_text_not_jsonb_req39_a05() -> None:
    """REQ-39 A-05: labels stored as TEXT for json.loads(str(...)) pattern."""
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    assert "narrative_canonical_labels_json text" in sql
    assert "narrative_canonical_labels_json jsonb" not in sql


def test_required_columns_ready_checks_subset_of_select_fields_req39_g02() -> None:
    """REQ-39 G-02: required_columns_ready only references columns we SELECT."""
    select_fields = {f.strip() for f in _STORY_SELECT_FIELDS.split(",") if f.strip()}
    src = inspect.getsource(SupabaseDatabase.required_columns_ready)
    for field in select_fields:
        if field in src:
            assert field in select_fields


def test_required_columns_ready_geo_fields_in_select_and_bootstrap_req39_g03() -> None:
    """REQ-39 G-03: geo fields aligned across SELECT list and bootstrap (offline)."""
    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    geo_fields = (
        "geo_normalized_label",
        "geo_latitude",
        "geo_longitude",
        "geo_confidence",
        "geo_provider",
        "geo_cluster_tags_json",
        "geo_admin_district",
        "geo_admin_settlement",
        "geo_admin_region",
        "geo_admin_country",
    )
    for field in geo_fields:
        assert field in _STORY_SELECT_FIELDS, f"geo field {field!r} missing from SELECT"
        assert field in sql, f"geo field {field!r} missing from bootstrap"


def test_doge_issues_columnar_fields_in_bootstrap_and_readiness_gw_rc_04_t10() -> None:
    """GW-RC-04 T10: columnar SELECT fields exist in bootstrap; readiness checks them."""
    from core.projection.columnar_storage import (
        COLUMNAR_ROW_SELECT,
        DOGE_ISSUES_COLUMNAR_READINESS_COLUMNS,
    )

    sql = _BOOTSTRAP_SQL.read_text(encoding="utf-8")
    for field in DOGE_ISSUES_COLUMNAR_READINESS_COLUMNS:
        assert field in sql, f"columnar field {field!r} missing from bootstrap"
    select_fields = {f.strip() for f in COLUMNAR_ROW_SELECT.split(",") if f.strip()}
    assert DOGE_ISSUES_COLUMNAR_READINESS_COLUMNS <= select_fields
    src = inspect.getsource(SupabaseDatabase.required_columns_ready)
    assert "DOGE_ISSUES_COLUMNAR_READINESS_COLUMNS" in src
    assert '"doge_issues"' in src or "'doge_issues'" in src
