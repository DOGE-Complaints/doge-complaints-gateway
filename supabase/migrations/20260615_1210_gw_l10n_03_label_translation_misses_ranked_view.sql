-- GW-L10N-03 T04: operator visibility — top untranslated label keys per locale

create or replace view public.label_translation_misses_ranked as
select
    locale,
    label_key,
    miss_count,
    last_seen_at
from public.label_translation_misses
order by locale asc, miss_count desc, last_seen_at desc;

grant select on public.label_translation_misses_ranked to service_role;
