# task-gw-ssr-32-t01-open-normalize-axis

## Task: implement — open Contour1 `normalize_axis` (T01)

## Meta
- **Story:** [STORY-GW-SSR-32](../STORY-GW-SSR-32-node-specific-contour1-wire-axes.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000089
- **Skill declared:** python-pro
- **Depends on:** soft SSR-31 Done
- **Scaffolded:** 2026-09-04T13:07:36Z
- **Completed:** 2026-09-04T13:13:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md`

## Purpose
Remove frozen membership check in `normalize_axis` (`Unsupported taxonomy axis`). Keep non-empty str → strip → lower. Update module comment: `TAXONOMY_AXIS_VALUES` = tallinn/civic **reference** set (D-SSR-11), not wire reject SSOT. Do **not** change Contour2 resolver.

## Code Facts
1. **As-of-Done (SSR-32 pkg-000089):** Contour1 unlock — `axes.py` `normalize_axis`: strip/lower only; no `TAXONOMY_AXIS_VALUES` membership.
2. **As-of-Done:** Wire entry — `story_labels.py` L206 calls `normalize_axis`.
3. Export — `taxonomy/__init__.py` re-exports unchanged.
4. `TAXONOMY_AXIS_VALUES` remains frozenset for tallinn/docs/SSR-28 helpers (reference).
5. **Historical (pre-P3):** Membership reject L23–29 `Unsupported taxonomy axis`.

## Gap
**Closed (P3):** custom axis ids accepted on wire Contour1. **Historical gap:** «Wire taxonomy with custom axis id rejected by Contour1».

## Acceptance / DoD
- [x] Membership check removed; non-empty / non-string reject remains
- [x] Module comment: reference set, not wire reject SSOT
- [x] No Contour2 / ClusterLens / vocabulary / docs edits
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/src/core/taxonomy/axes.py`

## Out of scope
Contour2 (SSR-31). Docs (SSR-33). `_AXIS_TO_SIGNAL_DIMENSION` / vocabulary expand. Disposition enum.
- Overlay bans (every task):
  - Contour1 only: open `normalize_axis` (strip/lower; no frozen membership).
  - **No** Contour2 loader / `resolver.py` taxonomy parse reopen (SSR-31).
  - **No** docs/README/manual rewrite (SSR-33).
  - **No** ClusterLens / vocabulary / civic axis→SignalDimension map expand.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not reopen SSR-01–31 product beyond tests required by Contour1 unlock.

## Verification commands
```bash
rg -n "Unsupported taxonomy axis|TAXONOMY_AXIS_VALUES" doge-complaints-gateway/src/core/taxonomy/axes.py
```
