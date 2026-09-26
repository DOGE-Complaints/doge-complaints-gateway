# task-gw-req9-01-t04-tests-docs-align

## Task: tests/docs — align SPA_BASE_URL naming (T04)

## Meta
- **Story:** [STORY-GW-REQ9-01](../STORY-GW-REQ9-01-example-env-and-spa-base-url.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000096
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-09-26T12:02:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md`

## Purpose
Update gateway tests/docs that still treat `SPA_VERIFY_BASE_URL` / `spa_verify_base_url` as primary. Scope #3 · AC-GW-REQ901-05. **No** dual-read. Same wave: rename local/Railway env var for SPA base (service id Open — do not invent).

## Code Facts
1. Tests set `SPA_VERIFY_BASE_URL` — e.g. `tests/test_gw_draft_02_story_draft_submit_contract.py:32`, `tests/test_gw_gauth_03_verification_gate_contract.py:21`.
2. Manual names `SPA_VERIFY_BASE_URL` — `docs/runtime-docs/manuals/server-env-quickstart.md:158`.
3. Broader grep at P3: `rg SPA_VERIFY|spa_verify` under `tests/` + `docs/runtime-docs/` (+ optional API_REFERENCE / `.env.test.example`).
4. Historical run-reports may keep old names (story projected — leave untouched if out of primary path).

## Gap
Primary config name in tests/docs still `SPA_VERIFY_*`.

## Acceptance / DoD
- [x] Gateway tests/docs do not treat `SPA_VERIFY_BASE_URL` as primary config name (AC-GW-REQ901-05)
- [x] No dual-read / alias fallback introduced
- [x] Live pytest recorded for touched suites (P3)
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/**` referencing `SPA_VERIFY_*` / `spa_verify_*`
- `docs/runtime-docs/manuals/server-env-quickstart.md` (+ optional API_REFERENCE / `.env.test.example`)
- Do **not** invent Railway service ids / waitlist / nginx

## Out of scope
make test rituals (REQ9-02); product APIs; aibridge/spa renames; §Актуальная точка rewrite.
- Overlay bans:
  - Hard cut only — **no** `SPA_VERIFY_*` dual-read.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000095; pointer is pkg-000096.

## Verification commands
```bash
rg -n 'SPA_VERIFY|spa_verify' doge-complaints-gateway/tests doge-complaints-gateway/docs/runtime-docs doge-complaints-gateway/src || true
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_gauth_03_verification_gate_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py --tb=short
```
