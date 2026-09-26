# task-gw-req9-01-t02-schema-spa-base-hard-cut

## Task: implement — schema SPA_BASE_URL hard cut (T02)

## Meta
- **Story:** [STORY-GW-REQ9-01](../STORY-GW-REQ9-01-example-env-and-spa-base-url.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000096
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-26T12:02:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md`

## Purpose
EnvSpec/AppConfig/load: `SPA_BASE_URL` + `spa_base_url`; remove primary `SPA_VERIFY_*` / `spa_verify_*`. Scope #2 · AC-GW-REQ901-03. **No** alias dual-read.

## Code Facts
1. **As-of-Done:** Field `spa_base_url: str | None` — `src/core/config/schema.py:53`.
2. **As-of-Done:** Load via `_get_value(source, "SPA_BASE_URL")` — `schema.py:583–589`; ctor `:649`. No dual-read of `SPA_VERIFY_*`.
3. **As-of-Done:** `IDENTITY_BASE_URL` EnvSpec — `schema.py:129` (unchanged).
4. **Historical (pre-P3):** field `spa_verify_base_url`; load `SPA_VERIFY_BASE_URL` via ad-hoc `_get_value` (no EnvSpec name hit).

## Gap
**Closed (P3 2026-09-26T12:06:30Z):** hard cut to `SPA_BASE_URL` / `spa_base_url`. **G1 SSOT As-of-Done (P6 2026-09-26T12:12:27Z).**

## Acceptance / DoD
- [x] Configured env name is `SPA_BASE_URL`; field `spa_base_url` (AC-GW-REQ901-03)
- [x] No primary `SPA_VERIFY_*` / `spa_verify_*` in schema load/field (no dual-read)
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/config/schema.py`
- Call sites that read `config.spa_base_url` (wired in T03)

## Out of scope
Helper rename details (T03); tests/docs (T04); make test; invent Railway ids; dual-read feature flag.
- Overlay bans:
  - Hard cut only — **no** `SPA_VERIFY_*` dual-read.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000095; pointer is pkg-000096.

## Verification commands
```bash
rg -n 'SPA_VERIFY|spa_verify|SPA_BASE_URL|spa_base_url' doge-complaints-gateway/src/core/config/schema.py
```
