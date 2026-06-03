-- Full bootstrap for fresh Supabase initialization (story-first, hardened_plus).
-- This script consolidates migration deltas into one idempotent setup.

create extension if not exists vector;

-- Core tables
create table if not exists public.stories (
    story_id text primary key,
    schema_version text not null,
    narrative_original_text text not null,
    submitter_external_user_id text not null,
    submitter_identity_issuer text not null,
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
    add column if not exists narrative_canonical_type text,
    add column if not exists narrative_canonical_labels_json text not null default '[]';

-- GAP-07: geo columns expected by _STORY_SELECT_FIELDS / _story_geo_supabase_fields (db_supabase.py)
alter table if exists public.stories
    add column if not exists geo_normalized_label text,
    add column if not exists geo_latitude double precision,
    add column if not exists geo_longitude double precision,
    add column if not exists geo_confidence double precision,
    add column if not exists geo_provider text,
    add column if not exists geo_cluster_tags_json text not null default '[]';

-- REQ-35: structured admin levels for CLUSTER_GEO_FILTER / CLUSTER_GEO_SCOPE
alter table if exists public.stories
    add column if not exists geo_admin_district text,
    add column if not exists geo_admin_settlement text,
    add column if not exists geo_admin_region text,
    add column if not exists geo_admin_country text;

-- STORY-M2-02-06 §16: summary JSON, live_story consistency notes
alter table if exists public.stories
    add column if not exists narrative_summary_json text,
    add column if not exists narrative_consistency_notes text;

-- STORY-M2-02-07 / REQ-33: multilingual intake v2 narrative dict columns
alter table if exists public.stories
    add column if not exists narrative_title_json jsonb,
    add column if not exists narrative_description_json jsonb,
    add column if not exists narrative_session_language text;

-- STORY-M2-02-09 / REQ-43: optional institution i18n on stories
alter table if exists public.stories
    add column if not exists institution_json jsonb;

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

-- GAP-08 variant A: gateway persists embedding_vector_json only; pgvector column kept optional (nullable)
alter table if exists public.story_embeddings
    alter column embedding drop not null;

create index if not exists idx_story_embeddings_story_id on public.story_embeddings(story_id);

create table if not exists public.doge_issues (
    issue_id text primary key,
    status text not null,
    payload_json jsonb not null,
    policy_version text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.doge_issue_embeddings (
    embedding_id bigint generated always as identity primary key,
    issue_id text not null references public.doge_issues(issue_id) on delete cascade,
    model_name text not null,
    embedding vector(8) not null,
    source_checksum text not null,
    created_at timestamptz not null default now()
);

alter table if exists public.doge_issue_embeddings
    add column if not exists embedding_vector_json text,
    add column if not exists embedding_policy_version text not null default 'm3.doge_issue_embedding_policy.v1';

-- GAP-08 variant A (same as story_embeddings)
alter table if exists public.doge_issue_embeddings
    alter column embedding drop not null;

create index if not exists idx_issue_embeddings_issue_id on public.doge_issue_embeddings(issue_id);

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
create index if not exists idx_issue_story_links_story on public.issue_story_links(story_id);
create table if not exists public.story_signals (
    story_id text not null references public.stories(story_id) on delete cascade,
    extraction_policy text not null,
    signals_json jsonb not null,
    extracted_at timestamptz not null default now(),
    primary key (story_id, extraction_policy)
);
create index if not exists idx_story_signals_policy on public.story_signals(extraction_policy);

create table if not exists public.cluster_memberships (
    story_id text not null references public.stories(story_id) on delete cascade,
    lens text not null,
    cluster_id text not null,
    computed_at timestamptz not null default now(),
    primary key (story_id, lens)
);
create index if not exists idx_cluster_memberships_cluster on public.cluster_memberships(cluster_id);

-- Issues read model
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
from public.doge_issues p;

grant select on public.issues_dashboard to anon, authenticated;

-- Baseline RLS (existing tables)
alter table public.stories enable row level security;
alter table public.idempotency_keys enable row level security;
alter table public.story_embeddings enable row level security;
alter table public.doge_issues enable row level security;
alter table public.doge_issue_embeddings enable row level security;

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

drop policy if exists projections_service_role_all on public.doge_issues;
drop policy if exists doge_issues_service_role_all on public.doge_issues;
create policy doge_issues_service_role_all
on public.doge_issues
for all
to service_role
using (true)
with check (true);

drop policy if exists projection_embeddings_service_role_all on public.doge_issue_embeddings;
drop policy if exists doge_issue_embeddings_service_role_all on public.doge_issue_embeddings;
create policy doge_issue_embeddings_service_role_all
on public.doge_issue_embeddings
for all
to service_role
using (true)
with check (true);

-- Hardened_plus RLS for new story-first tables
alter table public.issue_candidates enable row level security;
alter table public.review_audit_log enable row level security;
alter table public.issue_story_links enable row level security;
alter table public.story_signals enable row level security;
alter table public.cluster_memberships enable row level security;

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

drop policy if exists story_signals_service_role_all on public.story_signals;
create policy story_signals_service_role_all
on public.story_signals
for all
to service_role
using (true)
with check (true);

drop policy if exists cluster_memberships_service_role_all on public.cluster_memberships;
create policy cluster_memberships_service_role_all
on public.cluster_memberships
for all
to service_role
using (true)
with check (true);
