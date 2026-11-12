# task-gw-ssr-32-t02-tests-custom-and-empty-wire

## Task: tests — custom axis accepted; empty/non-str fail (T02)

## Meta
- **Story:** [STORY-GW-SSR-32](../STORY-GW-SSR-32-node-specific-contour1-wire-axes.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000089
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-04T13:07:36Z
- **Completed:** 2026-09-04T13:13:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md`

## Purpose
`tests/test_gw_ssr_32_contour1_wire_axes.py`: custom axis (e.g. `signal_type`) accepted via `parse_taxonomy_payload` / `normalize_axis`; `""` / `None` / non-string still fail. Adapted `test_gw_tax_01_taxonomy.py` Contour1 reject → accept (required by unlock).

## Code Facts
1. **As-of-Done:** Module — `tests/test_gw_ssr_32_contour1_wire_axes.py` (custom + empty/non-str + intake).
2. **As-of-Done:** Regression adapt — `tests/test_gw_tax_01_taxonomy.py` `test_intake_accepts_custom_axis`.
3. **Historical (pre-P3):** tax_01 `test_intake_rejects_invalid_axis` expected Contour1 membership reject.

## Gap
**Closed (P3):** Contour1 unlock covered. **Historical:** «No dedicated Contour1 unlock coverage».

## Acceptance / DoD
- [x] Custom axis not in `TAXONOMY_AXIS_VALUES` parses; labels persist with that axis string
- [x] Empty / non-string axis → ValueError / IntakeValidationError
- [x] No Contour2 / ClusterLens / docs edits
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_32_contour1_wire_axes.py`
- `doge-complaints-gateway/tests/test_gw_tax_01_taxonomy.py` (Contour1 adapt only)

## Out of scope
Civic skip regression (T03). Docs SSR-33. Vocabulary expand.
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
