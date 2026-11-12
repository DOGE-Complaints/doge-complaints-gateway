# task-gw-ssr-26-t04-tests-file

## Task: tests — create test_gw_ssr_26_taxonomy_loader.py (T04)

## Meta
- **Story:** [STORY-GW-SSR-26](../STORY-GW-SSR-26-taxonomy-json-pack-contract.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000083
- **Skill declared:** python-pro
- **Depends on:** T02–T03
- **Scaffolded:** 2026-09-01T12:55:39Z
- **Completed:** 2026-09-01T13:00:37Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md`

## Purpose
Создать `tests/test_gw_ssr_26_taxonomy_loader.py` со story-listed tests: `test_clusterlens_baseline_unchanged` (len==10); `test_legal_and_mobility_load_without_taxonomy`; `test_missing_taxonomy_file_when_declared_fails`; `test_invalid_axis_in_taxonomy_file_fails`. Tallinn load-when-declared → SSR-28.

## Code Facts
1. **As-of-Done (SSR-26 pkg-000083):** [`tests/test_gw_ssr_26_taxonomy_loader.py`](../../../../../../../tests/test_gw_ssr_26_taxonomy_loader.py) exists — 6 tests (story T04 four + duplicate-key + happy-path load).
2. `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py).
3. Loader error type — `UnsupportedVersionError`.
4. **Historical (pre-P3 / P1 scaffold):** `tests/test_gw_ssr_26_*` — **0 files**.

## Acceptance / DoD
- [x] File `tests/test_gw_ssr_26_taxonomy_loader.py` exists with four named tests (story T04)
- [x] ClusterLens regression anchor len==10
- [x] No tallinn official seed assertion as Done for SSR-26
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_26_taxonomy_loader.py`

## Out of scope
Post-SSR-28 `test_tallinn_loads_taxonomy_when_manifest_declares_schema`.
- Overlay bans (every task):
  - **No tallinn seed** (SSR-28 owns official `taxonomy.json` + manifest key).
  - **No ClusterLens** add/remove. Enum stays 10 (`types.py:10–22`).
  - **No wire taxonomy** — `parse_taxonomy_payload` / GW-TAX-01 / `story_labels` untouched.
  - **No** replace `vocabulary.py` with pack read.
  - Orphan on-disk `taxonomy.json` **without** `taxonomy_schema` must **not** auto-load.
  - Loader optional at introduction; legal/mobility stay without taxonomy.
  - **Нет `GET /schema-active`.** Нет invent HTTP geo-filter. Нет IDX / `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет new SQL.
  - **Нет SSR-06/07/12.** Не reopen 01–25 product. Не стартовать 27/28/29 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_26_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```
