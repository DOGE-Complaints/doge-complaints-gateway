-- GW-CAB-02: draft↔owner association + updated_at on story_drafts

alter table public.story_drafts
    add column if not exists updated_at timestamptz;

update public.story_drafts
    set updated_at = created_at
    where updated_at is null;

alter table public.story_drafts
    alter column updated_at set not null;

create table if not exists public.draft_owner (
    draft_id text primary key references public.story_drafts (draft_id) on delete cascade,
    submitter_external_user_id text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_draft_owner_submitter
    on public.draft_owner (submitter_external_user_id);

alter table public.draft_owner enable row level security;

drop policy if exists draft_owner_service_role_all on public.draft_owner;
create policy draft_owner_service_role_all
on public.draft_owner
for all
to service_role
using (true)
with check (true);
