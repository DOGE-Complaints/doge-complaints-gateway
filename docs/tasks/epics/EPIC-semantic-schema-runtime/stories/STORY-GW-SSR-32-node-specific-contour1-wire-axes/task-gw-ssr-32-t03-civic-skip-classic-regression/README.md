# task-gw-ssr-32-t03-civic-skip-classic-regression

## Task: tests — civic skip-unmapped + classic 13 wire (T03)

## Meta
- **Story:** [STORY-GW-SSR-32](../STORY-GW-SSR-32-node-specific-contour1-wire-axes.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000089
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-09-04T13:07:36Z
- **Completed:** 2026-09-04T13:13:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md`

## Purpose
Unmapped-only axes: enrichment does not raise; unmapped absent from civic dimension map. Classic 13-axis wire still passes. Map not expanded.

## Code Facts
1. **As-of-Done:** Tests in `test_gw_ssr_32_contour1_wire_axes.py` — `test_civic_skip_unmapped_*`, `test_civic_mapped_axis_*`, `test_classic_thirteen_axis_wire_*`.
2. **As-of-Done:** Civic skip path unchanged in `story_labels.py` (~L185–188).
3. **Historical (pre-P3):** Risk that Contour1 unlock invents civic SignalDimension for unmapped axes.

## Gap
**Closed (P3):** skip + classic 13 regression green. **Historical:** «Need regression that unlock does not invent civic SignalDimension».

## Acceptance / DoD
- [x] Story with only unmapped axes: civic fill does not raise; unmapped absent from civic dimension map
- [x] Classic 13-axis wire samples still pass
- [x] No `_AXIS_TO_SIGNAL_DIMENSION` / vocabulary / ClusterLens expand
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_32_contour1_wire_axes.py`

## Out of scope
Expand civic map. Contour2. Docs SSR-33.
- Overlay bans (every task):
  - Contour1 only: open `normalize_axis` (strip/lower; no frozen membership).
  - **No** Contour2 loader / `resolver.py` taxonomy parse reopen (SSR-31).
  - **No** docs/README/manual rewrite (SSR-33).
  - **No** ClusterLens / vocabulary / civic axis→SignalDimension map expand.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not reopen SSR-01–31 product beyond tests required by Contour1 unlock.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_ssr_32_contour1_wire_axes.py
```
