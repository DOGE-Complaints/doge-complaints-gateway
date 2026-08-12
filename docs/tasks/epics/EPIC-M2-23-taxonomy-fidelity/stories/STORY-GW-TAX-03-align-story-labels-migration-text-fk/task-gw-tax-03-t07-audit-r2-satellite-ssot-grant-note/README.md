# task-gw-tax-03-t07-audit-r2-satellite-ssot-grant-note

## Meta
- **Story:** [STORY-GW-TAX-03](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000058 (parent Done); wave `run_mode=gw_tax_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-TAX-03
- **Depends on:** T06 (or parallel docs)
- **Audit ref:** [`audit-gw-tax-03-…`](../../../../../../analysis/audit-gw-tax-03-align-story-labels-migration-text-fk-2026-08-07.md) **R2** + **G1** (GRANT note folded)
- **Scaffolded:** 2026-08-07T10:21:47Z
- **Done:** 2026-08-07T10:29:30Z

## Purpose
Выровнять persistent satellite SSOT после TAX-03 Done: epic Problem Statement, runtime `story-persistence-model.md`, bootstrap comment на `000_full_init.sql` — past-tense / «pre-TAX-03». Добавить в migration явный note: GRANT aligned with proposed DRAFT-07; bootstrap historically RLS-only for `story_labels` (audit **G1**).

## Code Facts
- Epic «still UUID» — [`EPIC-M2-23-taxonomy-fidelity.md:14`](../../../EPIC-M2-23-taxonomy-fidelity.md)
- Runtime «UUID» — [`story-persistence-model.md:236`](../../../../../../runtime-docs/story-persistence-model.md)
- Bootstrap comment — [`000_full_init.sql:84-85`](../../../../../../supabase/bootstrap/000_full_init.sql)
- Migration GRANT — [`20260714_…story_labels.sql:31-32`](../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql); bootstrap `rg GRANT.*story_labels` empty
- Fact migration text — [`:11`](../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql)

## Acceptance / DoD
- [x] Epic + runtime-docs: past-tense / pre-TAX-03; no present «migration still UUID»
- [x] Bootstrap comment: migration file is text FK post-TAX-03 (or historical UUID labeled)
- [x] Migration SQL comment: GRANT = proposed DRAFT-07; bootstrap RLS-only historically (G1) — **no DDL change required**
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-03-t07.md`](./acceptance-verification-gw-tax-03-t07.md) signed (Date post P6 verify only)

## Where to change
- [`EPIC-M2-23-taxonomy-fidelity.md`](../../../EPIC-M2-23-taxonomy-fidelity.md)
- [`docs/runtime-docs/story-persistence-model.md`](../../../../../../runtime-docs/story-persistence-model.md)
- [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) (comment only)
- [`supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql`](../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) (GRANT note comment only)

## Out of scope
- Story body R1 (T06); elegance §4 / other `docs/analysis/*` (WAIVED working-doc); ALTER UUID hosts (TAX-04); DRAFT-07 audit §5.1 (R3 WAIVED working-doc); changing GRANT DDL / bootstrap GRANT sync

## Verification commands
```bash
rg -n 'still UUID|объявила `UUID`|used UUID' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-M2-23-taxonomy-fidelity.md \
  doge-complaints-gateway/docs/runtime-docs/story-persistence-model.md \
  doge-complaints-gateway/supabase/bootstrap/000_full_init.sql
# present-tense false claims should be gone or historical-labeled
rg -n 'GRANT|proposed DRAFT-07|RLS-only' doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
```
