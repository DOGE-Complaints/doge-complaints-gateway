# task-gw-req56-01-t02-post-fetch-filter-compose

## Task: implement — post-fetch filter compose (T02)

## Meta
- **Story:** [STORY-GW-REQ56-01](../STORY-GW-REQ56-01-issues-list-search-filter.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000111
- **Skill declared:** python-pro
- **Depends on:** soft T01
- **Scaffolded:** 2026-10-10T15:52:08Z
- **Done:** 2026-10-10T16:01:13Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md`

## Purpose
Встроить D-S1 match в post-fetch (`filter_projection_rows` или helper); compose AND со structural/geo; hybrid v1 in-memory; TECH-ARCH §3.1–3.2. Scope #2–4 · **AC-GW-REQ5601-02/03**.

## Code Facts
### As-of-Done (P3 2026-10-10T16:01:13Z)
1. Post-fetch Present — `filter_projection_rows(..., search=)` in `read_filters.py` after structural/geo (AND).
2. Empty/absent/whitespace → no text restrict.
3. Stores thread `search=` (InMemory/SQLite/Supabase).

### Historical (pre-P3 / scaffold)
1. Text filter not Present in post-fetch path.

## Gap
**G1 residual closed by T07:** Code Facts flipped As-of-Done vs Historical (search compose Present).

## Acceptance / DoD
- [x] Non-empty trimmed `search` restricts rows via D-S1
- [x] Compose AND with ≥1 structural/geo filter
- [x] Adding `search` does not widen exposure vs same params without search (DP3)
- [x] Empty/absent/whitespace → no text restriction
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-01-t02.md` signed (P3)

## Where to change
- `src/core/projection/read_filters.py` (+ T01 helper)
- store `list_projections` only if text must thread through

## Out of scope
ASGI wire (T03); unit/ASGI tests (T04/T05); invent DRAFT status; SQL/FTS DDL.

## Verification commands
```bash
rg -n "def filter_projection_rows|status" doge-complaints-gateway/src/core/projection/read_filters.py | head -30
```
