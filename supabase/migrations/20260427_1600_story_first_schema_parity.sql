-- TASK-SF-P0-01: Supabase schema/runtime parity for story-first fields.

alter table if exists public.stories
    add column if not exists narrative_language text,
    add column if not exists narrative_title_hint text,
    add column if not exists narrative_canonical_type text,
    add column if not exists narrative_canonical_labels_json text not null default '[]';

alter table if exists public.story_embeddings
    add column if not exists embedding_vector_json text;

alter table if exists public.spa_issue_projection_embeddings
    add column if not exists embedding_vector_json text;

create index if not exists idx_story_embeddings_story_id on public.story_embeddings(story_id);
create index if not exists idx_issue_embeddings_issue_id on public.spa_issue_projection_embeddings(issue_id);
