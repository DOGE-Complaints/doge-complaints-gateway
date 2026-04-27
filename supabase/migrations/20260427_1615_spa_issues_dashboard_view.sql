-- TASK-SF-P0-04: SPA-friendly direct-read view for issue projections.

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
