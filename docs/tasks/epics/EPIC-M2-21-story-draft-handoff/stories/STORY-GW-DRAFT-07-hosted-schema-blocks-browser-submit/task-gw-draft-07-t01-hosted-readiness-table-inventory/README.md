# task-gw-draft-07-t01-hosted-readiness-table-inventory

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** verify / ops
- **Status:** 🟢 Done
- **Package:** pkg-000056
- **Skill declared:** python-pro
- **Depends on:** GW-DRAFT-02 Done; TAX-01 code Done

## Purpose
Backlog T01: inventory Public Node vs `REQUIRED_READINESS_TABLES` — confirm that **only** `story_labels` is missing (all other required table probes OK).

## Code Facts
- Required set — [`db_supabase.py:29-43`](../../../../../../../../src/core/infrastructure/db_supabase.py) includes `story_labels`
- Probe — [`db_supabase.py:293-303`](../../../../../../../../src/core/infrastructure/db_supabase.py) `required_tables_ready()` → `GET /rest/v1/{table}?select=*&limit=1`
- Schema → db_ready — [`dependencies.py:75-83`](../../../../../../../../src/core/api/dependencies.py)
- Live pin — [`pin-STORY-SPA-BUG-01-root-cause-2026-08-06.md`](../../../../../../../../spa-app/docs/analysis/pin-STORY-SPA-BUG-01-root-cause-2026-08-06.md) §Mechanism (inventory claim)

## Acceptance / DoD
- [x] Traces story Scope T01: inventory recorded for all members of `REQUIRED_READINESS_TABLES`
- [x] Confirmed missing **only** `story_labels` (or deviations documented with evidence)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t01.md`](./acceptance-verification-gw-draft-07-t01.md) signed (Date post P3 verify only)

## Where to change
- Evidence note under `doge-complaints-gateway/docs/analysis/` (or acceptance file) — **no** `src/` changes
- Hosted Supabase Public Node `lvfrdtglpksmaywqlohj` (read-only inventory)

## Out of scope
- Applying DDL (T02); redeploy (T03); `/ready` post-fix (T04); browser submit (T05)
- Changing `REQUIRED_READINESS_TABLES` to drop `story_labels`

## Verification commands
```bash
# From workspace: confirm code set includes story_labels
cd doge-complaints-gateway && rg -n 'story_labels' src/core/infrastructure/db_supabase.py
# Hosted: PostgREST probe each REQUIRED_READINESS_TABLES member (operator / service_role)
# Document result in acceptance-verification-gw-draft-07-t01.md
```
