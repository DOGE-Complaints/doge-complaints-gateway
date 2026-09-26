# task-gw-req9-01-t01-example-env-keys

## Task: implement — example.env peer/own URL keys (T01)

## Meta
- **Story:** [STORY-GW-REQ9-01](../STORY-GW-REQ9-01-example-env-and-spa-base-url.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000096
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-26T12:02:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md`

## Purpose
Add `API_BASE_URL`, `IDENTITY_BASE_URL` (+ local `:8100` comment), `SPA_BASE_URL` to `example.env`; keep inbound `SERVICE_API_TOKEN`. Scope #1 · AC-GW-REQ901-01/02/04.

## Code Facts
1. **As-of-Done:** `example.env` has `API_BASE_URL=` `:104`, `IDENTITY_BASE_URL` + `:8100` comment `:107-108`, `SPA_BASE_URL=` `:112`, `SERVICE_API_TOKEN=` `:124`.
2. **As-of-Done:** Runtime loads `IDENTITY_BASE_URL` — `schema.py:129` / `:574–580` (documented in template).
3. **Historical (pre-P3):** `SERVICE_API_TOKEN=` present; smoke comment mentioned `API_BASE_URL` priority without `API_BASE_URL=` key; no `IDENTITY_BASE_URL` / `SPA_BASE_URL` keys.

## Gap
**Closed (P3 2026-09-26T12:06:30Z):** keys landed. **G1 SSOT As-of-Done (P6 2026-09-26T12:12:27Z).**

## Acceptance / DoD
- [x] `example.env` contains `IDENTITY_BASE_URL` + `:8100` comment (AC-GW-REQ901-01)
- [x] `example.env` contains `API_BASE_URL` (AC-GW-REQ901-02)
- [x] `example.env` documents `SPA_BASE_URL`; `SERVICE_API_TOKEN` retained (AC-GW-REQ901-04)
- [x] BULLRUN phases complete when closed

## Where to change
- `example.env`
- Do **not** invent Railway service ids / waitlist / nginx

## Out of scope
Schema/helpers rename (T02/T03); tests/docs align (T04); make test (REQ9-02); dual-read; §Актуальная точка rewrite.
- Overlay bans:
  - Hard cut docs name `SPA_BASE_URL` only — no dual-read.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000095; pointer is pkg-000096.

## Verification commands
```bash
rg -n 'API_BASE_URL|IDENTITY_BASE_URL|SPA_BASE_URL|SERVICE_API_TOKEN' doge-complaints-gateway/example.env
```
