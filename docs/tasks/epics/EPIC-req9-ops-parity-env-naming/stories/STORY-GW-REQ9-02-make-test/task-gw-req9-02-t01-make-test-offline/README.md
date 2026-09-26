# task-gw-req9-02-t01-make-test-offline

## Task: implement — Makefile `test` offline (T01)

## Meta
- **Story:** [STORY-GW-REQ9-02](../STORY-GW-REQ9-02-make-test.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000097
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-26T12:17:44Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-02-make-test.md`

## Purpose
Add `make test` target + PHONY entry; run pytest with `-m "not live_integration"`. Scope #1,#3 · AC-GW-REQ902-01/02. Operator lock C. Existing marker only — do not invent new markers or CI.

## Code Facts
1. **As-of-Done:** `.PHONY: serve dev simulate check-env test test-live` — `Makefile:1`.
2. **As-of-Done:** `test:` → `.venv/bin/python -m pytest -q -m "not live_integration"` — `Makefile:50–51`.
3. Marker `live_integration` declared — `pyproject.toml:34–35` (unchanged).
4. serve/dev/simulate/check-env bodies unchanged beyond PHONY/usage comments.

## Gap
**Closed (P3 2026-09-26T12:22:28Z).**

## Acceptance / DoD
- [x] `make test` exists and runs offline pytest with `-m "not live_integration"` (AC-GW-REQ902-01)
- [x] `.PHONY` includes `test` (AC-GW-REQ902-02)
- [x] Do not change serve/dev/simulate/check-env semantics beyond PHONY list
- [x] No new pytest markers; no invent CI
- [x] BULLRUN phases complete when closed

## Where to change
- `Makefile`

## Out of scope
`test-live` (T02); story gate (T03); SPA/env rename (REQ9-01); aibridge Makefile; invent CI; claim Railway verify from offline test; §Актуальная точка rewrite.
- Overlay bans:
  - Existing `live_integration` marker only.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000096; pointer is pkg-000097.

## Verification commands
```bash
rg -n '^\.PHONY:|^test:|not live_integration' doge-complaints-gateway/Makefile
make -n test
make test   # live: 10 live_integration deselected
```
