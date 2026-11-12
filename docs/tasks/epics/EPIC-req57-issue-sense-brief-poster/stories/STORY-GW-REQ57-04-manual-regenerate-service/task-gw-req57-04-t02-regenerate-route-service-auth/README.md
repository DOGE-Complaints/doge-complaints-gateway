# task-gw-req57-04-t02-regenerate-route-service-auth

## Task: implement — regenerate route + service-auth (T02)

## Meta
- **Story:** [STORY-GW-REQ57-04](../STORY-GW-REQ57-04-manual-regenerate-service.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:23:00Z
- **Package:** pkg-000116
- **Skill declared:** python-pro · soft fastapi-expert
- **Depends on:** T01
- **Scaffolded:** 2026-10-15T12:17:03Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md`
- **AC trace:** DP6; locked path `POST /v1/issue-sense-brief/regenerate`

## Purpose
`POST /v1/issue-sense-brief/regenerate` + service-auth (`SERVICE_API_TOKEN`)

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:23:00Z
1. Route Present — `asgi_app.py` `@app.post("/v1/issue-sense-brief/regenerate")` + `Depends(require_public_content_service_auth)`.
2. Handler Present — `handle_issue_sense_brief_regenerate` in `handlers.py`.

## Gap
**Closed P3 2026-10-15T12:23:00Z.**

## Acceptance / DoD
- [x] Route `POST /v1/issue-sense-brief/regenerate` Present
- [x] Auth via `SERVICE_API_TOKEN` (same family as bind)
- [x] Invokes regenerate apply (T01)
- [x] No invent path/AC; no citizen regenerate
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-04-t02.md` signed (P3)

## Where to change
- `src/core/api/asgi_app.py` · `src/core/api/handlers.py`

## Out of scope
Nudge (T03); authz negative cases detail (T04); tests (T05); gate (T06)

## Verification commands
```bash
rg -n "issue-sense-brief/regenerate|handle_issue_sense_brief_regenerate" doge-complaints-gateway/src/core/api/asgi_app.py doge-complaints-gateway/src/core/api/handlers.py | head -40
```
