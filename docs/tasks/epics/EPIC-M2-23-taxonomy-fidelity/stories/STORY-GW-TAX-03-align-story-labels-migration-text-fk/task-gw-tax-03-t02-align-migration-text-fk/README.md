# task-gw-tax-03-t02-align-migration-text-fk

## Meta
- **Story:** [STORY-GW-TAX-03](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000058
- **Skill declared:** python-pro
- **Depends on:** T01
- **P1 path decision:** edit in-place (not additive successor)

## Purpose
Выровнять [`20260714_1200_gw_tax_01_story_labels.sql`](../../../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql): `story_id text … REFERENCES stories(story_id)` + indexes + SQL guard-комментарий (UUID несовместим с text `stories.story_id`).

## Code Facts
- Current UUID DDL — migration `:3`
- Target shape — bootstrap [`000_full_init.sql:86-94`](../../../../../../../../supabase/bootstrap/000_full_init.sql)
- Peer pattern — [`20260523_1200_req42_story_signals.sql`](../../../../../../../../supabase/migrations/20260523_1200_req42_story_signals.sql)
- Hosted already text via DRAFT-07 — do not re-apply Public Node in this task

## Acceptance / DoD
- [x] Traces parent AC-1: migration uses **text** FK, not UUID
- [x] Traces parent AC-2: indexes `idx_story_labels_story` / `idx_story_labels_axis` present
- [x] Traces parent AC-3: guard comment in SQL about UUID vs text hosts
- [x] File edited in-place (no new successor migration unless T01 proves applied UUID host — default: edit)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-03-t02.md`](./acceptance-verification-gw-tax-03-t02.md) signed (Date post P3 verify only)

## Where to change
- [`supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql`](../../../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql)

## Out of scope
- RLS/GRANT (T03); docs INDEX (T04); `REQUIRED_READINESS_TABLES`; hosted apply; DRAFT-07 reopen

## Verification commands
```bash
rg -n 'UUID' doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql || test $? -eq 1
rg -n 'story_id text|REFERENCES.*stories|idx_story_labels_story|idx_story_labels_axis|guard|incompatible' doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
```
