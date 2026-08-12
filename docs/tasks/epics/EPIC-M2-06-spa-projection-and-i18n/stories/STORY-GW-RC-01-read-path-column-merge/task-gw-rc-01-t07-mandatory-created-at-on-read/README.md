# task-gw-rc-01-t07

## Meta
- **Story:** [STORY-GW-RC-01](../STORY-GW-RC-01-read-path-column-merge.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** — (audit override, вне pkg-000030)
- **Skill declared:** python-pro
- **Depends on:** T01–T06
- **Wave:** audit override (`run_mode=gw_rc_01_audit_followup`)
- **Decision Ref:** [`audit-gw-rc-01-read-path-column-merge-2026-06-19.md`](../../../../../../analysis/audit-gw-rc-01-read-path-column-merge-2026-06-19.md) §3 G3

## Purpose
Закрыть audit G3: `created_at` **обязателен** в каждом issue на read-path (column-as-truth). Write-path уже фиксирует время на всех бэкендах; read-merge не должен опускать поле при пустой колонке.

## Code Facts
- `merge_projection_columns` ставит `created_at` только если значение truthy — [`read_filters.py:199-200`](../../../../../../../src/core/projection/read_filters.py#L199-L200)
- InMemory read fallback: `str(created_at or row.get("updated_at", ""))` может дать `""` — [`repositories.py:204-208`](../../../../../../../src/core/infrastructure/repositories.py#L204-L208)
- SQLite/Supabase: `created_at NOT NULL` + `save_projection` пишет `now()` — [`db_sqlite.py:214`](../../../../../../../src/core/infrastructure/db_sqlite.py#L214), [`db_supabase.py:625-637`](../../../../../../../src/core/infrastructure/db_supabase.py#L625-L637)
- GW-RC-01 acceptance уже проверяет `created_at` на нормальном save — [`test_gw_rc_01_read_path_column_merge.py`](../../../../../../../tests/test_gw_rc_01_read_path_column_merge.py)

## Acceptance / DoD
- (P0) `merge_projection_columns` **всегда** выставляет `created_at` в ответе (убрать `if created_at:` guard)
- (P0) InMemory list/get: fallback `created_at` ← `updated_at` если колонка пуста
- (P0) Тест: row без `created_at` / с пустой колонкой → list/get возвращают валидный ISO `created_at`
- (P1) Существующие GW-RC-01 тесты без регрессий
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/projection/read_filters.py` — `merge_projection_columns`
- `src/core/infrastructure/repositories.py` — `created_at_text` fallback в list/get
- `tests/test_gw_rc_01_read_path_column_merge.py` — edge-case test

## Out of scope
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- Канонизация `type` (GW-RC-02)
- Legacy institution/geo (GW-RC-03)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_01_read_path_column_merge.py -q
cd doge-complaints-gateway && python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
