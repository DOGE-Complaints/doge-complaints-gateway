# task-gw-rc-04-t06

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** T01 ADR (view decision)

## Purpose
Переписать view `issues_dashboard` (backlog: `spa_issues_dashboard_view`) на колонки/jsonb вместо `payload_json->>`.

## Code Facts
- Current view — [`20260427_1615_spa_issues_dashboard_view.sql`](../../../../../../../supabase/migrations/20260427_1615_spa_issues_dashboard_view.sql) — `issues_dashboard` on `spa_issue_projections`
- Uses `payload_json->>'type'`, i18n paths, `labels_json`

## Acceptance / DoD
- Traces D-RC-5 view fate per T01 ADR
- View selects from columnar/jsonb fields (or dropped if ADR says obsolete)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `supabase/migrations/` (new migration replacing or altering view)
- Possibly `supabase/bootstrap/000_full_init.sql` if view defined there

## Out of scope
- `doge_issues` table migration (T02/T07)
- Gateway Python read-path (T04)

## Verification commands
```bash
# After migration: psql/supabase db lint or documented SQL smoke in task artifact
grep -n issues_dashboard doge-complaints-gateway/supabase/migrations/*.sql
```
