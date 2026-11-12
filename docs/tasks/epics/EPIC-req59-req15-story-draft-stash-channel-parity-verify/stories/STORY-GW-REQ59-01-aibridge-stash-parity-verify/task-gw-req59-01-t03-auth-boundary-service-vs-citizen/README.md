# task-gw-req59-01-t03-auth-boundary-service-vs-citizen

## Task: verify — auth boundary service vs citizen (T03)

## Meta
- **Story:** [STORY-GW-REQ59-01](../STORY-GW-REQ59-01-aibridge-stash-parity-verify.md)
- **Type:** verify
- **Status:** 🔵 Done
- **Package:** pkg-000117
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-11-05T12:01:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md`
- **AC trace:** AC-GW-59-04

## Purpose
POST service-only; GET/submit citizen; wrong/missing service → 401; citizen Bearer must not stash

## Code Facts
### Live (As-of-Done P3 / P6 SSOT) — 2026-11-05T12:20:04Z
1. POST uses `_STORY_DRAFT_WRITE_DEPS` / `require_public_content_service_auth` — Present.
2. GET `require_story_draft_read_user`; submit `require_story_draft_submit_user` — Present.
3. Missing/wrong service → 401 — Present (`test_gw_draft_01_*`); evidence matrix cited.

## Gap
**Closed P3** (auth boundary asserted) · P6 SSOT align G4.

## Acceptance / DoD
- [x] POST = service-only; GET/submit = citizen (+ submit verify gate)
- [x] Wrong/missing service → 401; citizen Bearer must not stash (cited)
- [x] No invent AC; no new auth modes
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req59-01-t03.md` signed (P3)

## Where to change
- Evidence / existing tests citation; product only if hard break → T05 gap

## Out of scope
New auth modes; SPA UI; aibridge FSM

## Verification commands
```bash
rg -n "_STORY_DRAFT|require_public_content_service_auth|require_story_draft_read_user|require_story_draft_submit_user" doge-complaints-gateway/src/core/api/asgi_app.py | head -40
```
