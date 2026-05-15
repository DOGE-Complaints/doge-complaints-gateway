-- STORY-M2-02-06: GAP-02/03/06 narrative extensions (idempotent for hosted Supabase)

alter table if exists public.stories
    add column if not exists narrative_title_hint_et text,
    add column if not exists narrative_title_hint_ru text,
    add column if not exists narrative_title_hint_en text,
    add column if not exists narrative_summary_json text,
    add column if not exists narrative_consistency_notes text;
