-- TASK-DB-RLS-01 baseline RLS policies.

alter table public.stories enable row level security;
alter table public.idempotency_keys enable row level security;
alter table public.story_embeddings enable row level security;
alter table public.spa_issue_projections enable row level security;
alter table public.spa_issue_projection_embeddings enable row level security;

-- Server-side/service-role access policy.
create policy if not exists stories_service_role_all
on public.stories
for all
to service_role
using (true)
with check (true);

create policy if not exists idempotency_service_role_all
on public.idempotency_keys
for all
to service_role
using (true)
with check (true);

create policy if not exists story_embeddings_service_role_all
on public.story_embeddings
for all
to service_role
using (true)
with check (true);

create policy if not exists projections_service_role_all
on public.spa_issue_projections
for all
to service_role
using (true)
with check (true);

create policy if not exists projection_embeddings_service_role_all
on public.spa_issue_projection_embeddings
for all
to service_role
using (true)
with check (true);
