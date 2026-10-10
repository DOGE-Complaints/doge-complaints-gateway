# task-gw-req56-01-t03-asgi-handler-search-wire

## Task: implement — ASGI/handler search wire (T03)

## Meta
- **Story:** [STORY-GW-REQ56-01](../STORY-GW-REQ56-01-issues-list-search-filter.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000111
- **Skill declared:** python-pro
- **Depends on:** soft T02
- **Scaffolded:** 2026-10-10T15:52:08Z
- **Done:** 2026-10-10T16:01:13Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md`

## Purpose
Query param **`search`** on `GET /node/issues` → `handle_issues_list` → list path; envelope unchanged; DP1. Scope #1 · **AC-GW-REQ5601-04**.

## Code Facts
### As-of-Done (P3 2026-10-10T16:01:13Z)
1. Optional Query param `search` on `GET /node/issues` — `asgi_app.issues_list`.
2. Handler → `list_projections(..., search=)` — `handle_issues_list`.
3. Envelope `data.issues` unchanged; no separate search route.

### Historical (pre-P3 / scaffold)
1. List params without text; param `search` Absent on ASGI/handler.

## Gap
**G1 residual closed by T07:** Code Facts flipped As-of-Done vs Historical (`search` wired).

## Acceptance / DoD
- [x] Optional query param name exactly `search`
- [x] Wired into handler → filter path
- [x] No new search route; envelope shape unchanged
- [x] No comments corpus
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-01-t03.md` signed (P3)

## Where to change
- `src/core/api/asgi_app.py` `issues_list`
- `src/core/api/handlers.py` `handle_issues_list`

## Out of scope
Unit/ASGI tests (T04/T05); OpenAPI (REQ56-02); invent alternate param names.

## Verification commands
```bash
rg -n "def issues_list|handle_issues_list|Query" doge-complaints-gateway/src/core/api/asgi_app.py doge-complaints-gateway/src/core/api/handlers.py | head -40
```
