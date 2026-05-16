-- STORY-M2-02-05 / GAP-07, GAP-08 (variant A): align live DB with bootstrap 000_full_init.sql
-- Idempotent; safe to apply after older migrations.

alter table if exists public.stories
    add column if not exists geo_normalized_label text,
    add column if not exists geo_latitude double precision,
    add column if not exists geo_longitude double precision,
    add column if not exists geo_confidence double precision,
    add column if not exists geo_provider text,
    add column if not exists geo_cluster_tags_json text not null default '[]',
    add column if not exists geo_admin_district text,
    add column if not exists geo_admin_settlement text,
    add column if not exists geo_admin_region text,
    add column if not exists geo_admin_country text;

alter table if exists public.story_embeddings
    alter column embedding drop not null;

alter table if exists public.doge_issue_embeddings
    alter column embedding drop not null;
