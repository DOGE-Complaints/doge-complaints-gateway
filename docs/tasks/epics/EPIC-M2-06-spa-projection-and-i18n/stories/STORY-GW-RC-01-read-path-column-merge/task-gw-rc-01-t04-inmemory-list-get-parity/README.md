# task-gw-rc-01-t04

## Meta
- **Story:** [STORY-GW-RC-01](../STORY-GW-RC-01-read-path-column-merge.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** pkg-000030
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
InMemory read store parity: `list_projections` / `get_projection` передают `issue_id` + merge через `merge_projection_columns`.

## Code Facts
- InMemory list tuple без `issue_id` — [`repositories.py:198-208`](../../../../../../../src/core/infrastructure/repositories.py#L198-L208)
- `get_projection` возвращает payload only — [`repositories.py:229-235`](../../../../../../../src/core/infrastructure/repositories.py#L229-L235)

## Acceptance / DoD
- Traces parent AC: поведение идентично на InMemory
- Traces parent AC: list/get с колоночным merge
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/infrastructure/repositories.py` — `InMemoryIssueProjectionStore.list_projections`, `get_projection`

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_01_read_path_column_merge.py -q -k in_memory
cd doge-complaints-gateway && python3 -m pytest tests/test_req24_tallinn_issues_read_api.py -q
```
