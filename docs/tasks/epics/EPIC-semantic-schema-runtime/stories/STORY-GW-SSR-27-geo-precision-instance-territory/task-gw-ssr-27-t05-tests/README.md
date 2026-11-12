# task-gw-ssr-27-t05-tests

## Task: tests — test_gw_ssr_27_geo_precision.py (T05)

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084
- **Skill declared:** python-pro
- **Depends on:** T02–T04
- **Scaffolded:** 2026-09-01T13:12:45Z
- **Completed:** 2026-09-01T13:21:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`

## Purpose
Create `tests/test_gw_ssr_27_geo_precision.py` covering loader tallinn/legal, invalid geo_model, parse detail_level, sqlite roundtrip, projection without coords, projection input propagate, payload schema property.

## Code Facts
1. **As-of-Done (SSR-27 pkg-000084):** [`tests/test_gw_ssr_27_geo_precision.py`](../../../../../../../tests/test_gw_ssr_27_geo_precision.py) — **10** tests (loader / parse / sqlite / projection / schema / migration).
2. Story T05 matrix — backlog SSR-27 §T05.
3. **Historical (pre-P3 / P1 scaffold):** `tests/test_gw_ssr_27_*` — **0 files**.

## Acceptance / DoD
- [x] File exists with story matrix cases
- [x] ClusterLens==10 regression somewhere in suite path
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_27_geo_precision.py`

## Out of scope
live_integration proof.
- Overlay bans (every task):
  - **No ClusterLens** add/remove. Enum stays 10 (`types.py:10–22`).
  - Civic `geo_filter_bucket` stays `admin_*` only.
  - **Do not** merge node `geo_scope` with `gpt_instance_territory` semantics.
  - **No** invent HTTP geo-filter / `GET /schema-active` / IDX / `story_dimensions`.
  - **No** street/house on Issue projection (REQ-51 §3).
  - **No** invented coords `(0.0,0.0)` for address-only (SSR-24 rule).
  - SSR-24 migration test keeps SSR-24-only column set — split `geo_detail_level` assertions.
  - Tallinn instance seed Option A omit / Option B demo settlement tallinn — **OP at P3**; no invent district/bbox.
  - **Нет GPT UI** materialize here. Parallel-safe vs taxonomy 26/28/29.
  - **Нет SSR-06/07/12.** Не reopen 01–26 product. Не стартовать 28/29 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_ssr_27_*.py
```
