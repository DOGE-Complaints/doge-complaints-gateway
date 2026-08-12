# task-gw-draft-07-t04-verify-ready-schema-db-ready

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** verify
- **Status:** 🟢 Done
- **Package:** pkg-000056
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Backlog T04 + story AC1: verify `GET https://dogestonia-tallinn.up.railway.app/ready` → `db.ready: true`, `checks.schema: true`.

## Code Facts
- Ready handler — [`handlers.py:83-95`](../../../../../../../../src/core/api/handlers.py) exposes `db.ready` from `dependencies.db_ready`
- Schema check — [`dependencies.py:75-83`](../../../../../../../../src/core/api/dependencies.py) `db_checks["schema"] = health_db.required_tables_ready()`
- Required includes `story_labels` — [`db_supabase.py:29-43`](../../../../../../../../src/core/infrastructure/db_supabase.py)

## Acceptance / DoD
- [x] Traces parent AC #1: `/ready` → `db.ready: true`, `checks.schema: true`
- [x] Sanitized ready JSON captured for evidence (T05 artifact / this acceptance)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t04.md`](./acceptance-verification-gw-draft-07-t04.md) signed (Date post P3 verify only)

## Where to change
- No code — live HTTP verify against Railway gateway URL

## Out of scope
- Browser submit smoke (T05); SPA UI; changing readiness table set

## Verification commands
```bash
curl -sS https://dogestonia-tallinn.up.railway.app/ready | python3 -m json.tool
# Expect: data.db.ready == true AND checks.schema == true (per envelope shape as-built)
```
