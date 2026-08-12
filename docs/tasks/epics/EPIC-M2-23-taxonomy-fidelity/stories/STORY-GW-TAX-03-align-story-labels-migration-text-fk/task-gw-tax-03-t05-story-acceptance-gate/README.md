# task-gw-tax-03-t05-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-TAX-03](../STORY-GW-TAX-03-align-story-labels-migration-text-fk.md)
- **Type:** gate
- **Status:** 🟢 Done
- **Package:** pkg-000058
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Story acceptance gate: all AC-1..AC-5 PASS with evidence; confirm DRAFT-07 not reopened and `REQUIRED_READINESS_TABLES` / FE / `/ready` unchanged for this story.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Parent AC verbatim — pipeline / backlog §Acceptance Criteria
- pkg — `pkg-000058-20260807-gw-tax-03-align-story-labels-migration-text-fk.yaml`
- REQUIRED set (must remain untouched) — [`db_supabase.py:29-43`](../../../../../../../../src/core/infrastructure/db_supabase.py)

## Acceptance / DoD
- [x] All AC-1..AC-5 PASS in [`story-acceptance-gate-STORY-GW-TAX-03.md`](./story-acceptance-gate-STORY-GW-TAX-03.md) with evidence
- [x] Traces AC-5: no DRAFT-07 reopen; no `REQUIRED_READINESS_TABLES` / FE / `/ready` gate changes
- [x] `--verify --check-dates` ok for pkg-000058
- [x] BULLRUN phases complete; story row Done
- [x] [`acceptance-verification-gw-tax-03-t05.md`](./acceptance-verification-gw-tax-03-t05.md) signed (Date post P3 verify only)

## Where to change
- [`story-acceptance-gate-STORY-GW-TAX-03.md`](./story-acceptance-gate-STORY-GW-TAX-03.md)
- [`bullrun-launch-index.md`](../../../../bullrun-launch-index.md) — story/task Done

## Out of scope
- New runtime features; hosted re-DDL; SPA/GPT

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
rg -n 'story_id text|UUID' doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
rg -n 'story_labels' doge-complaints-gateway/src/core/infrastructure/db_supabase.py | head
```
