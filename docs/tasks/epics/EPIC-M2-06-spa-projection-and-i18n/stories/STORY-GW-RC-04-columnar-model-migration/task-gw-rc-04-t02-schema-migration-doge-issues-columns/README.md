# task-gw-rc-04-t02

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** T01 ADR
- **Gated:** requires signed T01 ADR

## Purpose
Миграция схемы `doge_issues`: новые scalar + jsonb колонки по ADR; mirror в bootstrap.

## Code Facts
- Current schema — [`000_full_init.sql:84-91`](../../../../../../../supabase/bootstrap/000_full_init.sql#L84-L91)
- SQLite mirror — [`db_sqlite.py:212`](../../../../../../../src/core/infrastructure/db_sqlite.py#L212) (`payload_json TEXT`)

## Acceptance / DoD
- Traces D-RC-5: contract fields have column homes per ADR
- Supabase migration + bootstrap sync
- SQLite schema updated for dev parity
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `supabase/migrations/` (new migration)
- `supabase/bootstrap/000_full_init.sql`
- `src/core/infrastructure/db_sqlite.py` (CREATE TABLE)

## Out of scope
- Dropping `payload_json` (T07)
- Runtime read/write (T03–T05)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_db_backed_pipeline_e2e.py -q -k sqlite --co 2>/dev/null | head -5
# schema review: grep new columns in migration + bootstrap
```
