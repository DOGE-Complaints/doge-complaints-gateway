from __future__ import annotations

from pathlib import Path


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
