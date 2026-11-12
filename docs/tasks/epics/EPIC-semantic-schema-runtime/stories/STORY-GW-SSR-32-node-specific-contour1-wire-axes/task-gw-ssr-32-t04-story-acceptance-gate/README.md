# task-gw-ssr-32-t04-story-acceptance-gate

## Task: analyze — story acceptance + G32 (T04)

## Meta
- **Story:** [STORY-GW-SSR-32](../STORY-GW-SSR-32-node-specific-contour1-wire-axes.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000089
- **Skill declared:** python-pro
- **Depends on:** T01–T03 Done
- **Scaffolded:** 2026-09-04T13:07:36Z
- **Completed:** 2026-09-04T13:13:31Z
- **Gate Date:** 2026-09-04T13:13:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md`

## Purpose
Story acceptance gate G32. PASS iff AC-GW-SSR32-01…04. Contour1 unlock proven; ClusterLens=10; no Contour2 reopen / docs / vocabulary expand; no §Актуальная точка rewrite.

## Code Facts
- Gate — [`story-acceptance-gate-STORY-GW-SSR-32.md`](./story-acceptance-gate-STORY-GW-SSR-32.md) PASS
- Verification — [`acceptance-verification-gw-ssr-32-t04.md`](./acceptance-verification-gw-ssr-32-t04.md)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-32.md` PASS/FAIL + evidence (P3)
- [x] `acceptance-verification-gw-ssr-32-t04.md` signed (Date post P3 live verify)
- [x] AC-GW-SSR32-01…04 covered
- [x] Live `--project gateway --verify` recorded
- [x] `normalize_axis` membership reject gone; ClusterLens=10
- [x] Do **not** rewrite §«Актуальная точка»
- [x] BULLRUN phases complete

## Where to change
- This folder gate artifacts (P3)

## Out of scope
P3 invent Contour2/docs; ClusterLens / vocabulary expand.
- Overlay bans (every task):
  - Contour1 only: open `normalize_axis` (strip/lower; no frozen membership).
  - **No** Contour2 loader / `resolver.py` taxonomy parse reopen (SSR-31).
  - **No** docs/README/manual rewrite (SSR-33).
  - **No** ClusterLens / vocabulary / civic axis→SignalDimension map expand.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not reopen SSR-01–31 product beyond tests required by Contour1 unlock.

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_ssr_32_contour1_wire_axes.py
rg -n "Unsupported taxonomy axis" src/core/taxonomy/axes.py || true
```
