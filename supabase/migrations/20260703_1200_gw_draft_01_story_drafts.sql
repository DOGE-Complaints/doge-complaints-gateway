-- GW-DRAFT-01 / STORY-GW-DRAFT-01: ephemeral story intake draft stash (GPT → browser handoff)

create table if not exists public.story_drafts (
    draft_id text primary key,
    payload_json jsonb not null,
    created_at timestamptz not null default now(),
    expires_at timestamptz not null
);

create index if not exists idx_story_drafts_expires_at
    on public.story_drafts (expires_at);

alter table public.story_drafts enable row level security;

drop policy if exists story_drafts_service_role_all on public.story_drafts;
create policy story_drafts_service_role_all
on public.story_drafts
for all
to service_role
using (true)
with check (true);
