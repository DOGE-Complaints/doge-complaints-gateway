# task-gw-ssr-31-t02-adapt-ssr26-taxonomy-tests

## Task: tests — adapt SSR-26 Contour2 loader tests (T02)

## Meta
- **Story:** [STORY-GW-SSR-31](../STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000088
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-04T12:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md`

## Purpose
Replace «unknown axis vs frozen set» expectations in `test_gw_ssr_26_taxonomy_loader.py` with: (a) multi-axis / uus-shaped pack loads; (b) map key ∉ axes still fails; (c) duplicate axis still fails.

## Code Facts
1. **As-of-Done:** `test_gw_ssr_26_taxonomy_loader.py` — structural rejects + `test_node_defined_axes_not_equal_thirteen_loads`; no frozen-set Contour2 reject.
2. tmp_path nested pack pattern — existing SSR-26 helpers.
3. **Historical (pre-P3):** tests assumed lock (`unknown axis` vs `TAXONOMY_AXIS_VALUES`).

## Gap
**Closed (P3):** suite adapted; Contour2 lockstep no longer encoded. **Historical:** «tests encode Contour2 lockstep to 13 and will fail after T01».

## Acceptance / DoD
- [x] No test requires Contour2 reject solely because axes ∉ `TAXONOMY_AXIS_VALUES`
- [x] Multi-axis / ≠13 structurally valid pack loads (or deferred to T04 if split)
- [x] Key in `canonical_keys` / maps not in `axes[]` → error; duplicate axis → error
- [x] Targeted pytest green
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_26_taxonomy_loader.py`

## Out of scope
SSR-28 seed content asserts (→T03). New preferred module (→T04). Docs SSR-33.
- Overlay bans (every task):
  - Contour2 only: drop membership + set-equality lockstep; keep structural validation.
  - **No** Contour1 `normalize_axis` (SSR-32).
  - **No** docs/README/manual rewrite (SSR-33).
  - **No** ClusterLens expand; **no** uus pack.json product edit; **no** GPT-SSR-15.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not reopen 01–30 product beyond test adaptations required by Contour2 unlock.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_ssr_26_taxonomy_loader.py --tb=short
```
