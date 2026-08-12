# task-gw-tax-03-t08-audit-g3-migration-text-assert

## Meta
- **Story:** [STORY-GW-TAX-03](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000058 (parent Done); wave `run_mode=gw_tax_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-TAX-03
- **Depends on:** T02 Done (migration text on disk)
- **Audit ref:** [`audit-gw-tax-03-…`](../../../../../../analysis/audit-gw-tax-03-align-story-labels-migration-text-fk-2026-08-07.md) **G3**
- **Scaffolded:** 2026-08-07T10:21:47Z
- **Done:** 2026-08-07T10:30:10Z

## Purpose
Точечный unit assert: файл миграции `20260714_1200_gw_tax_01_story_labels.sql` объявляет `story_id text` (не UUID) — защита от рецидива «вернуть UUID в SQL» без review-only.

## Code Facts
- Migration text FK — [`20260714_1200_gw_tax_01_story_labels.sql:11`](../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql)
- Analog — DRAFT-07 G4 assert [`tests/test_gw_draft_07_required_story_labels.py`](../../../../../../tests/test_gw_draft_07_required_story_labels.py)
- No existing migration-string assert (audit G3)

## Acceptance / DoD
- [x] Unit test reads migration file (repo-relative) and asserts `story_id text` present for `story_labels` CREATE
- [x] Assert absence of `story_id UUID` (or equivalent) in that migration file
- [x] Test under `doge-complaints-gateway/tests/` (`test_gw_tax_03_*` naming)
- [x] `pytest` for that file green offline
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-03-t08.md`](./acceptance-verification-gw-tax-03-t08.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/tests/` (new unit test)
- **No** change to migration DDL itself (unless test discovers regression — then stop and report)

## Out of scope
- Hosted ALTER / UUID hosts (TAX-04); REQUIRED_READINESS_TABLES; DRAFT-07 reopen; docs R1/R2

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_03_migration_story_labels_text_fk.py -m "not live_integration"
# or path chosen in implementation
rg -n 'story_id UUID' supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql || test $? -eq 1
rg -n 'story_id text' supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
```
