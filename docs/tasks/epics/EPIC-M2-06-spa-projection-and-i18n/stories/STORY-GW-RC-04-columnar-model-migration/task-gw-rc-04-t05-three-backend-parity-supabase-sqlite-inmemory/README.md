# task-gw-rc-04-t05

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** fix
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** T03, T04

## Purpose
Согласовать columnar read/write across Supabase, SQLite, InMemory — parity checklist и fixes.

## Code Facts
- Supabase store — [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- SQLite store — [`db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- InMemory — [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py)
- Contract tests — [`test_supabase_issue_projection_store_contract.py`](../../../../../../../tests/test_supabase_issue_projection_store_contract.py)

## Acceptance / DoD
- Traces parent AC#4: 3 backends aligned on columnar model
- List/get/filter behavior equivalent across backends
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/infrastructure/db_supabase.py`
- `src/core/infrastructure/db_sqlite.py`
- `src/core/infrastructure/repositories.py`

## Out of scope
- SQL view (T06)
- Data migration (T07)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_supabase_issue_projection_store_contract.py tests/test_db_backed_pipeline_e2e.py -q
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_03_contract_guarantee.py -q
```
