# task-gw-req57-01-t01-generation-fields-persist

## Task: implement — generation fields persist (T01)

## Meta
- **Story:** [STORY-GW-REQ57-01](../STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:13:59Z
- **Package:** pkg-000113
- **Skill declared:** python-pro · soft `fastapi-expert`
- **Depends on:** —
- **Scaffolded:** 2026-10-15T11:04:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md`
- **AC trace:** Scope #4 · DP5 · enables AC-03/04

## Purpose
Persist Issue generation fields: `generation_status`, `generation_version`, `poster_url`, optional `generation_reason_class`; SQLite migrate + store R/W across InMemory/SQLite/Supabase. Scope #4 fields + DP5 (no job table). Enables AC-GW-REQ5701-03/04.

## Code Facts
### As-of-Done (P3 2026-10-15T11:13:59Z)
1. Generation fields persist Present — columnar + SQLite migrate + InMemory/Supabase round-trip.
2. Paths: `src/core/projection/columnar_storage.py`, `src/core/infrastructure/db_sqlite.py`, `src/core/infrastructure/repositories.py`, `supabase/migrations/20261015_1104_gw_req57_01_generation_fields.sql`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:04:04Z
1. Bind receiver `/v1/issue-sense-brief/bind` Absent (story Verified current state).
2. Issue create public payload Present — `src/core/application/issue_create.py` `_to_public_payload`.
3. `generation_status` / `poster_url` product fields Absent in `src/` (rg 2026-10-15 PLAN_APPLY).

## Gap
**Closed P3 2026-10-15T11:13:59Z.**

## Acceptance / DoD
- [x] Fields readable/writable on Issue projection store (InMemory + SQLite + Supabase paths)
- [x] SQLite migrate present for new columns; default status supports `pending`
- [x] No separate job table (DP5)
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-01-t01.md` signed (P3)

## Where to change
- Issue projection store / repositories / SQLite schema under `src/core/infrastructure/` (and related)

## Out of scope
Public payload serialize (T02); bind apply (T03/T04); route (T05); brief-wins (T06); tests (T07); gate (T08)

## Verification commands
```bash
rg -n "generation_status|poster_url|generation_version" doge-complaints-gateway/src --glob '*.py' | head -40
```
