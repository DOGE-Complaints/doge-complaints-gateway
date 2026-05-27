-- Repair hosted Supabase when stories lacks geo_admin_* (PGRST204 on intake save).
-- Source: supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql
-- Run in Supabase SQL Editor (project linked from .env SUPABASE_URL).

alter table if exists public.stories
    add column if not exists geo_admin_district text,
    add column if not exists geo_admin_settlement text,
    add column if not exists geo_admin_region text,
    add column if not exists geo_admin_country text;
