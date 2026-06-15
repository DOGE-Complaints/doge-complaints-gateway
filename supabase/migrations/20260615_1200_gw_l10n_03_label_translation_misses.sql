-- GW-L10N-03 / STORY-GW-L10N-03: anonymous label humanize-miss telemetry (aggregate)

create table if not exists public.label_translation_misses (
    label_key text not null,
    locale text not null check (locale in ('et', 'ru', 'en')),
    miss_count integer not null default 1 check (miss_count >= 1),
    last_seen_at timestamptz not null default now(),
    primary key (label_key, locale)
);

create index if not exists idx_label_translation_misses_locale_count
    on public.label_translation_misses (locale, miss_count desc, last_seen_at desc);

alter table public.label_translation_misses enable row level security;

drop policy if exists label_translation_misses_service_role_all on public.label_translation_misses;
create policy label_translation_misses_service_role_all
on public.label_translation_misses
for all
to service_role
using (true)
with check (true);
