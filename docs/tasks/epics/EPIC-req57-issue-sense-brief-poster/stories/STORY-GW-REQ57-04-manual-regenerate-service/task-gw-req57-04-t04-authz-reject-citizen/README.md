# task-gw-req57-04-t04-authz-reject-citizen

## Task: implement — authz reject citizen / missing token (T04)

## Meta
- **Story:** [STORY-GW-REQ57-04](../STORY-GW-REQ57-04-manual-regenerate-service.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:23:00Z
- **Package:** pkg-000116
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-10-15T12:17:03Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md`
- **AC trace:** AC-GW-REQ5704-02; AC-GW-REQ5704-03 · DP6

## Purpose
Citizen Bearer / missing token → rejected (no regenerate)

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:23:00Z
1. Route uses `require_public_content_service_auth` → `SERVICE_API_TOKEN` only.
2. Missing Authorization → 401; Bearer ≠ service token (citizen) → 401.

## Gap
**Closed P3 2026-10-15T12:23:00Z.**

## Acceptance / DoD
- [x] Without service auth → rejected (AC-5704-02)
- [x] Citizen Bearer cannot regenerate (AC-5704-03)
- [x] No invent AC; no citizen regenerate endpoint
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-04-t04.md` signed (P3)

## Where to change
- `asgi_app.py` regenerate dependencies (shared service-auth)

## Out of scope
Happy-path apply/nudge (T01/T03); tests file (T05); gate (T06)

## Verification commands
```bash
rg -n "issue-sense-brief/regenerate|require_public_content_service_auth" doge-complaints-gateway/src/core/api/asgi_app.py | head -20
```
