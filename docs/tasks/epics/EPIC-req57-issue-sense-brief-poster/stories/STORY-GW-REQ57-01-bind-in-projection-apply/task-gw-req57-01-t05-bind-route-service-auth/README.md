# task-gw-req57-01-t05-bind-route-service-auth

## Task: implement — bind route + service-auth (T05)

## Meta
- **Story:** [STORY-GW-REQ57-01](../STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:13:59Z
- **Package:** pkg-000113
- **Skill declared:** python-pro · soft `fastapi-expert`
- **Depends on:** T03, T04
- **Scaffolded:** 2026-10-15T11:04:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md`
- **AC trace:** Scope #1/#5 · peer handoff §4

## Purpose
Expose `POST /v1/issue-sense-brief/bind` with gateway service-auth (`SERVICE_API_TOKEN`); reject channel Bearer / worker S2S as bind auth. Scope #1/#5.

## Code Facts
### As-of-Done (P3 2026-10-15T11:13:59Z)
1. POST /v1/issue-sense-brief/bind Present + require_public_content_service_auth.
2. Paths: `src/core/api/asgi_app.py`, `src/core/api/handlers.py`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:04:04Z
1. Service-auth Present — `src/core/api/asgi_app.py` `require_public_content_service_auth`; `src/core/api/security.py` `extract_service_token`.
2. `SERVICE_API_TOKEN` Present — `src/core/config/schema.py`.
3. Bind route Absent.

## Gap
**Closed P3 2026-10-15T11:13:59Z.**

## Acceptance / DoD
- [x] Route Present at `POST /v1/issue-sense-brief/bind`
- [x] Auth via `SERVICE_API_TOKEN` (peer `GATEWAY_SERVICE_API_TOKEN` same value)
- [x] Reject channel Bearer / worker S2S as bind auth
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-01-t05.md` signed (P3)

## Where to change
- `src/core/api/asgi_app.py` / `handlers.py` — new bind route + service-auth dependency

## Out of scope
Apply logic internals (T03/T04); tests (T07)

## Verification commands
```bash
rg -n "issue-sense-brief/bind|require_public_content_service_auth|SERVICE_API_TOKEN" doge-complaints-gateway/src/core/api --glob '*.py' | head -40
```
