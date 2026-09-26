# task-gw-req9-01-t03-verify-url-helpers

## Task: implement — verify_url helpers rename (T03)

## Meta
- **Story:** [STORY-GW-REQ9-01](../STORY-GW-REQ9-01-example-env-and-spa-base-url.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000096
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-09-26T12:02:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md`

## Purpose
Rename helpers/exports to `spa_base_url` naming (`resolve_spa_base_url` etc.); wire `build_verify_url` to new AppConfig field. Scope #2 · AC-GW-REQ901-03. **No** dual-read.

## Code Facts
1. **As-of-Done:** `DEFAULT_SPA_BASE_URL` + `resolve_spa_base_url` + `build_verify_url` — `src/core/identity/verify_url.py:7–23`.
2. **As-of-Done:** Reads `config.spa_base_url` — `:11`.
3. **As-of-Done:** Export `resolve_spa_base_url` from `src/core/identity/__init__.py`.
4. **As-of-Done:** Default localhost base `http://localhost:3000` retained (`DEFAULT_SPA_BASE_URL`).
5. **Historical (pre-P3):** `DEFAULT_SPA_VERIFY_BASE_URL` / `resolve_spa_verify_base_url` / `config.spa_verify_base_url`.

## Gap
**Closed (P3 2026-09-26T12:06:30Z):** helpers renamed. **G1 SSOT As-of-Done (P6 2026-09-26T12:12:27Z).**

## Acceptance / DoD
- [x] Helpers/exports use `spa_base_url` naming; `build_verify_url` wired to new field (AC-GW-REQ901-03)
- [x] No primary `spa_verify_*` helper exports for allow/config path
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/identity/verify_url.py`
- `src/core/identity/__init__.py`
- Import call sites of `resolve_spa_base_url`

## Out of scope
example.env (T01); schema field (T02); tests/docs mass rename (T04); dual-read; invent Railway ids.
- Overlay bans:
  - Hard cut only — **no** `SPA_VERIFY_*` dual-read.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000095; pointer is pkg-000096.

## Verification commands
```bash
rg -n 'spa_verify|SPA_VERIFY|spa_base_url|SPA_BASE_URL|resolve_spa_' doge-complaints-gateway/src/core/identity
```
