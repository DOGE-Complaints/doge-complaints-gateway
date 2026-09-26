# task-gw-thr-01-t04-tests-pack-shell-required

## Task: tests — Tests pack shell required (T04)

## Meta
- **Story:** [STORY-GW-THR-01](../STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000093
- **Skill declared:** python-pro
- **Depends on:** prior T* in pkg order; loadable NODE_SCHEMA_* pack
- **Scaffolded:** 2026-09-21T20:17:40Z
- **Completed:** 2026-09-21T20:29:51Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md`

## Purpose
Pytest: complete pack with mandatory capabilities resolves; incomplete pack fails closed. Prefer tests/test_gw_thr_01_*.py.

## Code Facts
1. Preferred tests/test_gw_thr_01_*.py.
2. tmp_path pack fixtures OK; do not require live Volume.
3. Do not invent key strings beyond operator-locked names in implement wave.

## Gap
**Closed (P3 2026-09-21T20:29:51Z):** implemented.

## Acceptance / DoD
- [x] Complete pack resolves SUCCESS
- [x] Incomplete pack → fail-closed ConfigError-class
- [x] No silent defaults asserted
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/test_gw_thr_01_*.py`

## Out of scope
THR-02/03; REQ8; invent ThreadContext route; invent pack JSON key strings; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **Do not invent** pack JSON key strings (Open until operator lock).
  - **Do not invent** public ThreadContext route.
  - Fail-closed only — no silent defaults inventing policy.
  - Mandatory migration — no backward-compat “old pack without knobs OK”.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000061…092; pointer is pkg-000093.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_thr_01_*.py
```
