# task-gw-tax-03-t06-audit-r1-story-present-tense

## Meta
- **Story:** [STORY-GW-TAX-03](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000058 (parent Done); wave `run_mode=gw_tax_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-TAX-03
- **Depends on:** T01–T05 Done
- **Audit ref:** [`audit-gw-tax-03-align-story-labels-migration-text-fk-2026-08-07.md`](../../../../../../analysis/audit-gw-tax-03-align-story-labels-migration-text-fk-2026-08-07.md) **R1**
- **Scaffolded:** 2026-08-07T10:21:47Z
- **Done:** 2026-08-07T10:28:37Z

## Purpose
Убрать present-tense UUID claims в backlog + pipeline при Status Done: §«Зачем» и таблица «Что наблюдаю» всё ещё пишут migration = UUID. Пометить pre-T02 UAT как historical; добавить «Текущее состояние (post-Done)» с text FK + RLS.

## Code Facts
- Backlog §Зачем / таблица UUID — [`STORY-GW-TAX-03-…md:16`](../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md), [`:22`](../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- Pipeline same — [`STORY-GW-TAX-03-….md:20`](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md), [`:26`](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- Fact post-T02 — migration [`:11`](../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) `story_id text`
- Status Done — Meta gate PASS 2026-08-07T09:59:37Z

## Acceptance / DoD
- [x] Backlog + pipeline: pre-T02 UAT labeled historical; no present-tense «migration всё ещё UUID»
- [x] «Текущее состояние (post-Done)» / equivalent: text FK + RLS; ref migration `:11` (not stale `:3` as UUID DDL)
- [x] Depends/Зачем не утверждают UUID as current
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-03-t06.md`](./acceptance-verification-gw-tax-03-t06.md) signed (Date post P6 verify only)

## Where to change
- [`backlog-stories/taxonomy-fidelity/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md`](../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- [`STORY-GW-TAX-03-align-story-labels-migration-text-fk.md`](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md) (pipeline)

## Out of scope
- Satellite epic/runtime/bootstrap (T07); migration DDL rewrite; DRAFT-07 reopen; `docs/analysis/*` elegance body (WAIVED working-doc)

## Verification commands
```bash
rg -n 'всё ещё объявляет `story_id UUID`|\*\*UUID\*\* FK' \
  doge-complaints-gateway/docs/tasks/backlog-stories/taxonomy-fidelity/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-03-align-story-labels-migration-text-fk/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md
# present-tense UUID claims should be absent or only under historical/pre-T02 label
rg -n 'story_id text' doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
```
