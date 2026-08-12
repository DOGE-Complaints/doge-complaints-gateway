# task-gw-rc-01-t02

## Meta
- **Story:** [STORY-GW-RC-01](../STORY-GW-RC-01-read-path-column-merge.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** pkg-000030
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Supabase read store: SELECT `issue_id, status, payload_json, created_at` в `list_projections` и `get_projection`; передача 4-tuple в `filter_projection_rows` / merge на get.

## Code Facts
- `list_projections` SELECT без `issue_id` — [`db_supabase.py:667-679`](../../../../../../../src/core/infrastructure/db_supabase.py#L667-L679)
- `get_projection` SELECT только `payload_json` — [`db_supabase.py:703-714`](../../../../../../../src/core/infrastructure/db_supabase.py#L703-L714)
- Merge helper из T01 — `read_filters.merge_projection_columns`

## Acceptance / DoD
- Traces parent AC: `GET /tallinn/issues` и `/{id}` — `id`, `status`, `created_at` из колонок (Supabase path)
- Traces parent AC: неполный `payload_json` + колонки → валидный ответ
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/infrastructure/db_supabase.py` — `SupabaseIssueProjectionStore.list_projections`, `get_projection`

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/ -q -k supabase --ignore=tests/smoke --ignore=tests/integration
# после T05:
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_01_read_path_column_merge.py -q
```
