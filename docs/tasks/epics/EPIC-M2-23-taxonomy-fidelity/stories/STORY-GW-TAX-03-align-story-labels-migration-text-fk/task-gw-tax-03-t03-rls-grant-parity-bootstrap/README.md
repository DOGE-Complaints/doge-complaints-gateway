# task-gw-tax-03-t03-rls-grant-parity-bootstrap

## Meta
- **Story:** [STORY-GW-TAX-03](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000058
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Добавить в ту же migration RLS + policy `story_labels_service_role_all` + GRANT parity с bootstrap / proposed DRAFT-07 SQL (цель backlog §2).

## Code Facts
- Bootstrap RLS — [`000_full_init.sql:281`](../../../../../../../../supabase/bootstrap/000_full_init.sql); policy `:325-331`
- Proposed parity — [`proposed-migration-DRAFT-07-story-labels-text-fk.sql`](../../../../../../backlog-stories/story-draft-handoff/proposed-migration-DRAFT-07-story-labels-text-fk.sql) (ENABLE RLS + policy + GRANT)
- Current migration has **no** RLS/GRANT (pre-T03)

## Acceptance / DoD
- [x] Traces parent цель 2: RLS + `service_role` policy + GRANT in migration (or explicit documented deferral with owner — prefer implement parity)
- [x] Matches bootstrap/proposed policy name `story_labels_service_role_all`
- [x] No hosted Public Node re-apply required for this task
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-03-t03.md`](./acceptance-verification-gw-tax-03-t03.md) signed (Date post P3 verify only)

## Where to change
- [`supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql`](../../../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) (append RLS/GRANT after T02 text DDL)

## Out of scope
- Changing bootstrap; hosted apply; `REQUIRED_READINESS_TABLES`; SPA/GPT

## Verification commands
```bash
rg -n 'ROW LEVEL SECURITY|story_labels_service_role_all|GRANT' doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
rg -n 'story_labels_service_role_all' doge-complaints-gateway/supabase/bootstrap/000_full_init.sql
```
