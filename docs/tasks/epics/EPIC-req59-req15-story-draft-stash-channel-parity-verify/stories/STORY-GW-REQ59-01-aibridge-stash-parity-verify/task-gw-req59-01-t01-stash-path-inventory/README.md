# task-gw-req59-01-t01-stash-path-inventory

## Task: verify — stash path inventory (T01)

## Meta
- **Story:** [STORY-GW-REQ59-01](../STORY-GW-REQ59-01-aibridge-stash-parity-verify.md)
- **Type:** verify
- **Status:** 🔵 Done
- **Package:** pkg-000117
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-11-05T12:01:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md`
- **AC trace:** AC-GW-59-01/02 · GW-DRAFT-01

## Purpose
Inventory Present: route deps, handler 201/`draft_id`, repo save, TTL config

## Code Facts
### Live (As-of-Done P3 / P6 SSOT) — 2026-11-05T12:20:04Z
1. `POST /story-drafts` + `_STORY_DRAFT_WRITE_DEPS` / `require_public_content_service_auth` — Present (`asgi_app.py:375` / `:685`).
2. `handle_story_draft_create` → 201 + `draft_id` — Present (`handlers.py:790–829`).
3. Repo save + TTL — Present (`handlers.py:817` · `config.story_draft_ttl_seconds` / `STORY_DRAFT_TTL_SECONDS`).

## Gap
**Closed P3** (inventory cited) · P6 SSOT align G4.

## Acceptance / DoD
- [x] Cited inventory: route deps, handler 201/`draft_id`, repo save, TTL config
- [x] No invent AC; no redesign intake
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req59-01-t01.md` signed (P3)

## Where to change
- Claims/evidence only unless hard break (then gap via T05) — Prefer: analysis notes / task evidence

## Out of scope
Aibridge client rewrite (T02); auth matrix (T03); stash≠Story assert (T04); evidence file (T05); gate (T06)

## Verification commands
```bash
rg -n "story-drafts|handle_story_draft_create|_STORY_DRAFT_WRITE_DEPS" doge-complaints-gateway/src/core/api/asgi_app.py doge-complaints-gateway/src/core/api/handlers.py | head -40
```
