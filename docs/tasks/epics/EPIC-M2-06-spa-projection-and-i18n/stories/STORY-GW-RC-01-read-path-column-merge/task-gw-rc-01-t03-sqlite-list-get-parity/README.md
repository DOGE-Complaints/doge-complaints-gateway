# task-gw-rc-01-t03

## Meta
- **Story:** [STORY-GW-RC-01](../STORY-GW-RC-01-read-path-column-merge.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** pkg-000030
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
SQLite read store parity с T02: `list_projections` / `get_projection` SELECT включает `issue_id`; 4-tuple + merge.

## Code Facts
- SQLite `SELECT status, payload_json, created_at` без `issue_id` — [`db_sqlite.py:616-636`](../../../../../../../src/core/infrastructure/db_sqlite.py#L616-L636)
- `get_projection` возвращает payload only — [`db_sqlite.py:656+`](../../../../../../../src/core/infrastructure/db_sqlite.py#L656)

## Acceptance / DoD
- Traces parent AC: поведение идентично Supabase path (SQLite)
- Traces parent AC: list/get с колоночным merge
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/infrastructure/db_sqlite.py` — `SqliteIssueProjectionStore.list_projections`, `get_projection`

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req24_tallinn_issues_read_api.py::test_req24_ac1_sqlite_doge_issues_table_exists -q
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_01_read_path_column_merge.py -q -k sqlite
```
