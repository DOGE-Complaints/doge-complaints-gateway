-- TASK-DB-SCHEMA-01 baseline migration
-- Target: stories + embeddings + SPA projections + projection embeddings.

create extension if not exists vector;

create table if not exists public.stories (
    story_id text primary key,
    schema_version text not null,
    narrative_original_text text not null,
    submitter_external_user_id text not null,
    submitter_identity_issuer text,
    lifecycle_status text not null,
    created_at timestamptz not null,
    updated_at timestamptz not null,
    origin_source text,
    origin_conversation_id text,
    origin_tool_call_id text,
    privacy_contains_pii boolean not null default false,
    privacy_redaction_requested boolean not null default false
);

create table if not exists public.idempotency_keys (
    key text primary key,
    story_id text not null references public.stories(story_id) on delete cascade,
    created_at timestamptz not null
);

create table if not exists public.story_embeddings (
    embedding_id bigint generated always as identity primary key,
    story_id text not null references public.stories(story_id) on delete cascade,
    model_name text not null,
    embedding vector(8) not null,
    source_checksum text not null,
    created_at timestamptz not null default now()
);
create index if not exists idx_story_embeddings_story_id on public.story_embeddings(story_id);

create table if not exists public.spa_issue_projections (
    issue_id text primary key,
    status text not null,
    payload_json jsonb not null,
    policy_version text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.spa_issue_projection_embeddings (
    embedding_id bigint generated always as identity primary key,
    issue_id text not null references public.spa_issue_projections(issue_id) on delete cascade,
    model_name text not null,
    embedding vector(8) not null,
    source_checksum text not null,
    created_at timestamptz not null default now()
);
create index if not exists idx_issue_embeddings_issue_id on public.spa_issue_projection_embeddings(issue_id);
