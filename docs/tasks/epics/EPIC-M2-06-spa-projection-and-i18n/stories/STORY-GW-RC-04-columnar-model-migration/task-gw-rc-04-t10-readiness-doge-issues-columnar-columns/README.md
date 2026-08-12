# task-gw-rc-04-t10

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** — (audit override, вне pkg-000033)
- **Skill declared:** python-pro
- **Depends on:** T01–T09 (columnar migration Done)
- **Wave:** audit override (`run_mode=gw_rc_04_audit_followup`)
- **Decision Ref:** [`audit-gw-rc-04-columnar-model-migration-2026-06-20.md`](../../../../../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md) §3 G1

## Purpose
Закрыть audit G1: после дропа `payload_json` Supabase read-path SELECT'ит columnar-колонки (`COLUMNAR_ROW_SELECT`), но `/ready` не проверяет их наличие на hosted DB. Добавить readiness-guard для `doge_issues` columnar-колонок, чтобы pre-migration состояние флагалось до деплоя кода.

## Code Facts
- Read SELECT columnar — [`columnar_storage.py:9-13`](../../../../../../../src/core/projection/columnar_storage.py#L9-L13): `COLUMNAR_ROW_SELECT`
- Supabase list/get — [`db_supabase.py:665-690`](../../../../../../../src/core/infrastructure/db_supabase.py#L665-L690)
- `required_columns_ready` без `doge_issues` — [`db_supabase.py:327-358`](../../../../../../../src/core/infrastructure/db_supabase.py#L327-L358)
- Geo admin pattern — [`db_supabase.py:305-318`](../../../../../../../src/core/infrastructure/db_supabase.py#L305-L318): `required_stories_geo_admin_columns_ready`
- `/ready` wiring — [`dependencies.py:73-74`](../../../../../../../src/core/api/dependencies.py#L73-L74)
- Offline test pattern — [`test_supabase_bootstrap_schema.py:125-131`](../../../../../../../tests/test_supabase_bootstrap_schema.py#L125-L131)

## Acceptance / DoD
- (P0) Readiness проверяет columnar-колонки `doge_issues` (набор = поля `COLUMNAR_ROW_SELECT` минус `issue_id,status,created_at`)
- (P0) Offline unit test: columnar fields в readiness aligned с `COLUMNAR_ROW_SELECT` / bootstrap
- (P1) Deploy-order note в task artifact: migration `20260619_1200` + `20260619_1220` **до** deploy кода
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/infrastructure/db_supabase.py` — extend `required_columns_ready` and/or dedicated method
- опционально `src/core/api/dependencies.py` — `/ready` flag
- `tests/test_supabase_bootstrap_schema.py` — offline alignment test
- `deploy-order-columnar-migration.md` (new, task folder) — краткая ops note

## Out of scope
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- Hosted Supabase apply (operator)
- G2 columnar tests (T11)
- Doc R1 backlog status

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_supabase_bootstrap_schema.py -q -k columnar
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
# live (optional): tests/integration/supabase/test_supabase_required_columns_ready_live.py
```
