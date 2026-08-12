# task-gw-rc-04-t04

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** T03 write-path

## Purpose
Read-path + `read_filters`: сборка public issue dict из колонок/jsonb; фильтры по колонкам/jsonb вместо monolithic payload.

## Code Facts
- Interim column merge (RC-01) — [`read_filters.py:231+`](../../../../../../../src/core/projection/read_filters.py#L231)
- `parse_payload_json` — [`read_filters.py:305`](../../../../../../../src/core/projection/read_filters.py#L305)
- Supabase list/get SELECT — [`db_supabase.py:665-723`](../../../../../../../src/core/infrastructure/db_supabase.py#L665-L723)
- SQLite list/get — [`db_sqlite.py:614-675`](../../../../../../../src/core/infrastructure/db_sqlite.py#L614-L675)

## Acceptance / DoD
- Traces D-RC-5 read-path + parent AC#4 filters on columns/jsonb
- External API issue shape unchanged vs [`dto.py`](../../../../../../../src/core/projection/dto.py)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/projection/read_filters.py`
- Store list/get assembly (coordinate with T05)

## Out of scope
- Schema migration (T02)
- View rewrite (T06)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_01_read_path_column_merge.py tests/test_gw_rc_03_contract_guarantee.py -q
cd doge-complaints-gateway && python3 -m pytest tests/test_filter_projection_rows_contract.py -q
```
