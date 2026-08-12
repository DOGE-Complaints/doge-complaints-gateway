# task-gw-rc-04-t07

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** data
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** T02 schema, T03–T05 runtime columnar paths

## Purpose
Data-миграция: backfill existing rows from `payload_json` into new columns; затем DROP `payload_json`.

## Code Facts
- Legacy blob column — [`000_full_init.sql:87`](../../../../../../../supabase/bootstrap/000_full_init.sql#L87)
- E2E reads payload_json — [`test_db_backed_pipeline_e2e.py:200`](../../../../../../../tests/test_db_backed_pipeline_e2e.py#L200)

## Acceptance / DoD
- Traces parent AC#3: `payload_json` removed; data migrated without loss
- Migration script + rollback notes in task artifact
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `supabase/migrations/` (data migration + DROP column)
- `supabase/bootstrap/000_full_init.sql`
- `src/core/infrastructure/db_sqlite.py` (schema)

## Out of scope
- Contract test updates (T08)
- ADR (T01)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_db_backed_pipeline_e2e.py -q
# post-migration: assert no payload_json column in schema grep
```
