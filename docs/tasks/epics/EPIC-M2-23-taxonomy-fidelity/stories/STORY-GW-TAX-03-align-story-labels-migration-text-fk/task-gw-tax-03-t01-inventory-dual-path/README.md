# task-gw-tax-03-t01-inventory-dual-path

## Meta
- **Story:** [STORY-GW-TAX-03](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- **Type:** verify
- **Status:** 🟢 Done
- **Package:** pkg-000058
- **Skill declared:** python-pro
- **Depends on:** —
- **Audit / decision_ref:** backlog TAX-03 §«Что наблюдаю»; elegance G1; execution G1

## Purpose
Зафиксировать dual-path inventory: repo migration UUID vs bootstrap / sqlite / peer / hosted text — таблица as-is из backlog (без правок DDL).

## Code Facts
- Migration UUID — [`20260714_1200_gw_tax_01_story_labels.sql:3`](../../../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql)
- Bootstrap text — [`000_full_init.sql:86-94`](../../../../../../../../supabase/bootstrap/000_full_init.sql)
- SQLite TEXT — [`db_sqlite.py:385-391`](../../../../../../../../src/core/infrastructure/db_sqlite.py)
- Peer text — [`20260523_1200_req42_story_signals.sql:4`](../../../../../../../../supabase/migrations/20260523_1200_req42_story_signals.sql)
- Hosted text (post DRAFT-07) — audits 2026-08-07 (no live re-apply required for this task)

## Acceptance / DoD
- [x] Traces parent context: dual-path table documented in acceptance artifact
- [x] Confirms migration still UUID and bootstrap/sqlite/peer text (rg evidence)
- [x] Notes hosted already text; DRAFT-07 not reopened
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-03-t01.md`](./acceptance-verification-gw-tax-03-t01.md) signed (Date post P3 verify only)

## Where to change
- This task folder only (acceptance artifact); **no** `src/` / migration edits

## Out of scope
- Editing migration (T02); RLS (T03); INDEX Done text (T04); gate (T05)

## Verification commands
```bash
rg -n 'story_id UUID|story_id text' doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
rg -n 'story_labels' doge-complaints-gateway/supabase/bootstrap/000_full_init.sql | head
rg -n 'CREATE TABLE.*story_labels|story_id' doge-complaints-gateway/src/core/infrastructure/db_sqlite.py | head
```
