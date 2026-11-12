# task-gw-ssr-28-t04-tests

## Task: tests — test_gw_ssr_28_taxonomy_seed.py (T04)

## Meta
- **Story:** [STORY-GW-SSR-28](../STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000085
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-09-01T13:31:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md`

## Purpose
Create `tests/test_gw_ssr_28_taxonomy_seed.py` with story matrix: manifest, 13 axes, required signals ⊆ map, inventory vs GPT §4, vocab subset, resolve_pack taxonomy non-None. Regression SSR-26 + SSR-01.

## Code Facts
1. **As-of-Done (SSR-28 pkg-000085):** [`tests/test_gw_ssr_28_taxonomy_seed.py`](../../../../../../../tests/test_gw_ssr_28_taxonomy_seed.py) — six story asserts + ClusterLens=10 (7 tests); helper under `tests/helpers/ssr28_gpt_taxonomy_extract.py`.
2. Story T04 matrix / AC-04 pattern — backlog SSR-28 §T04 (live green).
3. SSR-26 regress — orphan-without-manifest moved to tmp_path; tallinn loads taxonomy.
4. **Historical (pre-P3 / P1 scaffold):** `tests/test_gw_ssr_28_*` — **0 files**.

## Acceptance / DoD
- [x] File exists with six story assertions
- [x] ClusterLens==10 somewhere in path
- [x] Regression path documented for test_gw_ssr_26_* / test_gw_ssr_01_*
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_28_taxonomy_seed.py`

## Out of scope
live_integration proof.
- Overlay bans (every task):
  - **No invent** taxonomy vocabulary — extract only from GPT `story-label-taxonomy.md` §4/§5/§6 + axes/disposition lockstep.
  - **No ClusterLens** add/remove. Enum stays 10.
  - **No** legal/mobility `taxonomy_schema` / taxonomy.json seed.
  - **No** silent renames vs GPT §4.
  - **No** GPT UI materialize / GPT-SSR-05 copy in this pkg.
  - Orphan `taxonomy.json` without manifest = **not** Done.
  - Stay `semantic-schema-runtime`. Не переписывать bullrun §«Актуальная точка».
  - No SSR-06/07/12. Do not start SSR-29 product. Do not reopen 01–27.
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_ssr_28_*.py
```
