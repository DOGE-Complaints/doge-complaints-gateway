# task-gw-seed-01-t01

## Meta
- **Story:** [STORY-GW-SEED-01](../STORY-GW-SEED-01-loader-and-hosted-readiness.md)
- **Type:** ops
- **Status:** ⚪ Todo
- **Package:** pkg-000036
- **Skill declared:** python-pro

## Purpose
Чек-лист готовности hosted: `/ready` зелёный; `DB_BACKEND=supabase`; columnar-миграции RC-04 применены; `CLUSTER_CRON_ENABLED=true`.

## Code Facts
- `/ready` wiring — [`dependencies.py:73-74`](../../../../../../../src/core/api/dependencies.py#L73-L74)
- Columnar readiness — [`audit-gw-rc-04`](../../../../../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md); deploy order — [`deploy-order-columnar-migration.md`](../../../../EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t10-readiness-doge-issues-columnar-columns/deploy-order-columnar-migration.md)
- Migrations — [`20260619_1200_gw_rc_04_doge_issues_columnar_columns.sql`](../../../../../../../supabase/migrations/20260619_1200_gw_rc_04_doge_issues_columnar_columns.sql), [`1210`](../../../../../../../supabase/migrations/20260619_1210_gw_rc_04_issues_dashboard_columnar.sql), [`1220`](../../../../../../../supabase/migrations/20260619_1220_gw_rc_04_backfill_drop_payload_json.sql)
- `CLUSTER_CRON_ENABLED` default — [`schema.py:210-219`](../../../../../../../src/core/config/schema.py#L210-L219)
- Runbook pre-check — [`seed-demo-data-runbook-ru.md`](../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md) §2

## Acceptance / DoD
- Traces parent AC: `GET /ready` на hosted = `db_ready: true` до загрузки
- Traces parent AC: `CLUSTER_CRON_ENABLED=true` подтверждён на таргете
- Checklist artifact: `/ready` response saved (`db_ready`, `db_checks`)
- If `/ready` red: columnar migrations 1200/1210/1220 applied on hosted Supabase; re-check `/ready` green
- `DB_BACKEND=supabase` confirmed on Railway target
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Hosted Railway env (`CLUSTER_CRON_ENABLED`, `DB_BACKEND`) — operator ops
- Hosted Supabase SQL migrations — operator ops
- Task artifacts: readiness checklist + `/ready` JSON in this task folder

## Out of scope
- Application code changes
- Simulation loader runs (T02–T03)
- Dataset expansion (SEED-02)

## Verification commands
```bash
# From .env.test GATEWAY_URL
curl -sS "$GATEWAY_URL/ready" | jq '{db_ready, db_checks}'
# Expected: db_ready=true; db_checks.columns=true (supabase backend)
```
