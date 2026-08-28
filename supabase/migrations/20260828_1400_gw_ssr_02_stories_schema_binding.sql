-- STORY-GW-SSR-02: schema/profile binding + structured_payload persist
-- Parent semantic schema_version → bound_schema_version (envelope stays schema_version).

alter table public.stories
    add column if not exists schema_id text,
    add column if not exists bound_schema_version text,
    add column if not exists profile_id text,
    add column if not exists profile_version text,
    add column if not exists structured_payload jsonb,
    add column if not exists payload_hash text;

comment on column public.stories.schema_id is
  'GW-SSR-02: semantic pack schema_id; civic rows stay NULL';
comment on column public.stories.bound_schema_version is
  'GW-SSR-02: semantic pack version; envelope remains stories.schema_version';
comment on column public.stories.structured_payload is
  'GW-SSR-02: canonical JSON payload for the bound schema';
comment on column public.stories.payload_hash is
  'GW-SSR-02: SHA-256 of canonical JSON; computed server-side, not client hash';
