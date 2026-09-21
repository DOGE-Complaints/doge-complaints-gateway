# task-gw-thr-02-t02-service-auth-read-wire

## Task: implement — Service-auth read wire (T02)

## Meta
- **Story:** [STORY-GW-THR-02](../STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000094
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-21T20:43:05Z
- **Completed:** 2026-09-21T20:48:13Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md`

## Purpose
Wire a **service-auth** read that returns the T01 settings payload for threads. Reuse `require_public_content_service_auth` precedent. **No new public** ThreadContext / browser route. HTTP path string remains Open (choose at P3; do not write into REQ).

## Code Facts
1. `require_public_content_service_auth` — `src/core/api/asgi_app.py` (~338).
2. Precedent write route: `@app.post("/node/issues", …)` — `asgi_app.py` (~576).
3. Public Issue get has **no** service-auth dep — `asgi_app.py` `@app.get("/node/issues/{issue_id}")` (~545).
4. **As-of-Done (P3):** `GET /node/shell-settings` + `require_public_content_service_auth` — [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py) (~560–573); not in `PUBLIC_ROUTES`.
5. **Historical (pre-P3):** «No settings-pull / ThreadContext route under `src/` (absent)» — gap closed at P3.

## Gap
**Closed (P3 2026-09-21T20:48:13Z):** `GET /node/shell-settings` + `require_public_content_service_auth`; not in PUBLIC_ROUTES. **G1 SSOT As-of-Done (P6 2026-09-21T20:54:56Z).**


## Acceptance / DoD
- [x] Service-auth read returns pack-derived settings for active pair (AC-GW-THR02-01)
- [x] Auth class = existing service-auth precedent (not public browser class) (AC-GW-THR02-02)
- [x] No new **public** ThreadContext route (AC-GW-THR02-02)
- [x] Path string not written into REQ (Open)
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/api/asgi_app.py` / handlers / dependencies — service-auth read wire (**path Open**)
- Handler that returns T01 DTO

## Out of scope
THR-03; REQ8; invent public ThreadContext route; invent path into REQ; change Issue get civic class; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **Do not invent** public ThreadContext route.
  - Path/JSON field names **Open** — choose at P3; do not write into REQ.
  - No Story narrative bodies in settings (D19).
  - Fail-closed — no silent empty policy.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000093; pointer is pkg-000094.

## Verification commands
```bash
rg -n 'require_public_content_service_auth' doge-complaints-gateway/src/core/api/asgi_app.py
```
