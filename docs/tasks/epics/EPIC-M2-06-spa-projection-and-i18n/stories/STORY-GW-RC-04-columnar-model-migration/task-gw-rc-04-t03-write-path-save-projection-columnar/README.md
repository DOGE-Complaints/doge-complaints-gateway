# task-gw-rc-04-t03

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** T02 schema

## Purpose
Write-path: `save_projection` пишет scalar + jsonb колонки; не пишет общий `payload_json` blob.

## Code Facts
- Supabase upsert — [`db_supabase.py:617-638`](../../../../../../../src/core/infrastructure/db_supabase.py#L617-L638)
- SQLite insert — [`db_sqlite.py:583-587`](../../../../../../../src/core/infrastructure/db_sqlite.py#L583-L587)
- InMemory store — [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py)
- Payload source — [`dto.py:to_public_dict`](../../../../../../../src/core/projection/dto.py#L26-L50)

## Acceptance / DoD
- Traces D-RC-5 write-path: no duplicate id/status/created_at in blob
- All three stores persist columnar shape per ADR
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/infrastructure/db_supabase.py` — `save_projection`
- `src/core/infrastructure/db_sqlite.py` — `save_projection`
- `src/core/infrastructure/repositories.py` — InMemory store

## Out of scope
- Read-path (T04)
- Data backfill (T07)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_supabase_issue_projection_store_contract.py tests/test_db_backed_pipeline_e2e.py -q -k save
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
