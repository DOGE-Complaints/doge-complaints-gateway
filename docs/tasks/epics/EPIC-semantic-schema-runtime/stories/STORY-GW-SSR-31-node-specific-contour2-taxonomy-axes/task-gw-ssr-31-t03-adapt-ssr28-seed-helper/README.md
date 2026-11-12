# task-gw-ssr-31-t03-adapt-ssr28-seed-helper

## Task: tests — adapt SSR-28 seed + extract helper (T03)

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
Keep tallinn seed asserting **file/content** has 13 / equals reference set as **seed invariant**, not «loader rejects other sets». Adjust `ssr28_gpt_taxonomy_extract.py` so `TAXONOMY_AXIS_VALUES` is tallinn extract expected set only, not reject for arbitrary inventory.

## Code Facts
1. **As-of-Done:** tallinn seed asserts **content** 13 (`test_taxonomy_axes_seed_content_thirteen`); resolve still SUCCESS.
2. **As-of-Done:** helper docstring — `TAXONOMY_AXIS_VALUES` = tallinn extract expected set, not Contour2 reject SSOT.
3. **Historical (pre-P3):** seed/helper wording risked implying loader lockstep for all packs.

## Gap
**Closed (P3):** tallinn content invariant vs loader unlock clarified. **Historical:** «Seed/helper wording may imply loader lockstep for all packs».

## Acceptance / DoD
- [x] Tallinn official seed still loads; content asserts 13 as data lockstep
- [x] Helper does not treat `TAXONOMY_AXIS_VALUES` as Contour2 reject SSOT for arbitrary packs
- [x] No claim that loader rejects ≠13
- [x] Targeted pytest green
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_28_taxonomy_seed.py`
- `doge-complaints-gateway/tests/helpers/ssr28_gpt_taxonomy_extract.py` (if needed)

## Out of scope
uus-shaped SUCCESS home preferred in T04. Docs SSR-33. Contour1.
- Overlay bans (every task):
  - Contour2 only: drop membership + set-equality lockstep; keep structural validation.
  - **No** Contour1 `normalize_axis` (SSR-32).
  - **No** docs/README/manual rewrite (SSR-33).
  - **No** ClusterLens expand; **no** uus pack.json product edit; **no** GPT-SSR-15.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not reopen 01–30 product beyond test adaptations required by Contour2 unlock.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_ssr_28_taxonomy_seed.py --tb=short
```
