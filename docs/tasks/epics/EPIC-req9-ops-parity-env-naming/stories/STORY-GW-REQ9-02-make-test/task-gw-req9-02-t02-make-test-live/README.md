# task-gw-req9-02-t02-make-test-live

## Task: implement — Makefile `test-live` (T02)

## Meta
- **Story:** [STORY-GW-REQ9-02](../STORY-GW-REQ9-02-make-test.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000097
- **Skill declared:** python-pro
- **Depends on:** T01 (PHONY style; same Makefile edit wave)
- **Scaffolded:** 2026-09-26T12:17:44Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-02-make-test.md`

## Purpose
Add `make test-live` target + PHONY entry; run pytest with `-m live_integration`. Scope #2,#3 · AC-GW-REQ902-03. Operator lock C hygiene. Existing marker only — do not invent new markers or CI.

## Code Facts
1. **As-of-Done:** `.PHONY` includes `test-live` — `Makefile:1`.
2. **As-of-Done:** `test-live:` → `.venv/bin/python -m pytest -q -m live_integration` — `Makefile:53–54`.
3. Marker `live_integration` declared — `pyproject.toml:34–35` (unchanged).
4. Collect-only: 10/918 tests selected by marker.

## Gap
**Closed (P3 2026-09-26T12:22:28Z).**

## Acceptance / DoD
- [x] `make test-live` exists for live_integration suite (AC-GW-REQ902-03)
- [x] `.PHONY` includes `test-live`
- [x] Do not change serve/dev/simulate/check-env semantics beyond PHONY list
- [x] No new pytest markers; no invent CI
- [x] Honesty: offline `make test` ≠ Railway/hosted verify
- [x] BULLRUN phases complete when closed

## Where to change
- `Makefile`

## Out of scope
Offline `test` target details (T01); story gate (T03); SPA/env rename; invent CI; §Актуальная точка rewrite.
- Overlay bans:
  - Existing `live_integration` marker only.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000096; pointer is pkg-000097.

## Verification commands
```bash
rg -n '^\.PHONY:|^test-live:|live_integration' doge-complaints-gateway/Makefile
make -n test-live
.venv/bin/python -m pytest -q -m live_integration --collect-only
```
