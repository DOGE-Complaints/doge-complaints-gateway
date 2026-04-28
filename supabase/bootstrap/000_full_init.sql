-- Full bootstrap for fresh Supabase initialization (story-first, hardened_plus).
-- This script consolidates migration deltas into one idempotent setup.

create extension if not exists vector;

-- Core tables
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

alter table if exists public.stories
    add column if not exists narrative_language text,
    add column if not exists narrative_title_hint text,
    add column if not exists narrative_canonical_type text,
    add column if not exists narrative_canonical_labels_json text not null default '[]';

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

alter table if exists public.story_embeddings
    add column if not exists embedding_vector_json text,
    add column if not exists embedding_policy_version text not null default 'm2.story_embedding_policy.v1';

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

alter table if exists public.spa_issue_projection_embeddings
    add column if not exists embedding_vector_json text,
    add column if not exists embedding_policy_version text not null default 'm2.issue_embedding_policy.v1';

create index if not exists idx_issue_embeddings_issue_id on public.spa_issue_projection_embeddings(issue_id);

-- Story-first process/linkage tables
create table if not exists public.issue_candidates (
    candidate_id text primary key,
    status text not null,
    cluster_id text not null,
    story_ids_json jsonb not null,
    readiness_score integer not null check (readiness_score >= 0 and readiness_score <= 100),
    title text not null,
    updated_at timestamptz not null default now()
);

create table if not exists public.review_audit_log (
    audit_id bigserial primary key,
    candidate_id text not null,
    actor text not null,
    decision text not null,
    rationale text not null,
    related_cluster_id text not null,
    related_story_ids_json jsonb not null,
    created_at timestamptz not null default now()
);
create index if not exists idx_review_audit_candidate on public.review_audit_log(candidate_id);

create table if not exists public.issue_story_links (
    issue_id text not null,
    cluster_id text not null,
    story_id text not null,
    created_at timestamptz not null default now(),
    primary key (issue_id, story_id)
);
create index if not exists idx_issue_story_links_issue on public.issue_story_links(issue_id);

-- SPA read model
create or replace view public.issues_dashboard as
select
    p.issue_id,
    p.status,
    p.policy_version,
    p.updated_at,
    p.payload_json->>'type' as type,
    p.payload_json->'title'->>'en' as title_en,
    p.payload_json->'title'->>'et' as title_et,
    p.payload_json->'title'->>'ru' as title_ru,
    p.payload_json->'summary'->>'en' as summary_en,
    p.payload_json->'summary'->>'et' as summary_et,
    p.payload_json->'summary'->>'ru' as summary_ru,
    p.payload_json->'description'->>'en' as description_en,
    p.payload_json->'description'->>'et' as description_et,
    p.payload_json->'description'->>'ru' as description_ru,
    p.payload_json->'labels' as labels_json,
    p.payload_json as payload_json
from public.spa_issue_projections p;

grant select on public.issues_dashboard to anon, authenticated;

-- Baseline RLS (existing tables)
alter table public.stories enable row level security;
alter table public.idempotency_keys enable row level security;
alter table public.story_embeddings enable row level security;
alter table public.spa_issue_projections enable row level security;
alter table public.spa_issue_projection_embeddings enable row level security;

drop policy if exists stories_service_role_all on public.stories;
create policy stories_service_role_all
on public.stories
for all
to service_role
using (true)
with check (true);

drop policy if exists idempotency_service_role_all on public.idempotency_keys;
create policy idempotency_service_role_all
on public.idempotency_keys
for all
to service_role
using (true)
with check (true);

drop policy if exists story_embeddings_service_role_all on public.story_embeddings;
create policy story_embeddings_service_role_all
on public.story_embeddings
for all
to service_role
using (true)
with check (true);

drop policy if exists projections_service_role_all on public.spa_issue_projections;
create policy projections_service_role_all
on public.spa_issue_projections
for all
to service_role
using (true)
with check (true);

drop policy if exists projection_embeddings_service_role_all on public.spa_issue_projection_embeddings;
create policy projection_embeddings_service_role_all
on public.spa_issue_projection_embeddings
for all
to service_role
using (true)
with check (true);

-- Hardened_plus RLS for new story-first tables
alter table public.issue_candidates enable row level security;
alter table public.review_audit_log enable row level security;
alter table public.issue_story_links enable row level security;

drop policy if exists issue_candidates_service_role_all on public.issue_candidates;
create policy issue_candidates_service_role_all
on public.issue_candidates
for all
to service_role
using (true)
with check (true);

drop policy if exists review_audit_log_service_role_all on public.review_audit_log;
create policy review_audit_log_service_role_all
on public.review_audit_log
for all
to service_role
using (true)
with check (true);

drop policy if exists issue_story_links_service_role_all on public.issue_story_links;
create policy issue_story_links_service_role_all
on public.issue_story_links
for all
to service_role
using (true)
with check (true);
