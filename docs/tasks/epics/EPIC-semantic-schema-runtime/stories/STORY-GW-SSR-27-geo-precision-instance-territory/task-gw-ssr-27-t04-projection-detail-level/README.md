# task-gw-ssr-27-t04-projection-detail-level

## Task: implement — Issue.geo detail_level + UC-G03 without coords (T04)

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084
- **Skill declared:** python-pro
- **Depends on:** T03
- **Scaffolded:** 2026-09-01T13:12:45Z
- **Completed:** 2026-09-01T13:21:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`

## Purpose
`ProjectionInput.geo_detail_level`; propagate from draft; mapper: include `detail_level` with lat+lon; when no lat/lon but detail_level and/or admin — partial geo dict (UC-G03). No street/house on Issue.

## Code Facts
1. **As-of-Done (SSR-27 pkg-000084):** `ProjectionInput.geo_detail_level` — [`input.py`](../../../../../../../src/core/projection/input.py); propagate — [`extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py); UC-G03 partial geo without lat/lon — [`mapper.py`](../../../../../../../src/core/projection/mapper.py).
2. **Historical (pre-P3 / P1 scaffold):** mapper built geo primarily when lat+lon; ProjectionInput had **no** `geo_detail_level`.

## Acceptance / DoD
- [x] ProjectionInput + build_projection_input_from_draft propagate
- [x] UC-G03: geo dict without lat/lon when detail_level/admin present
- [x] No street/house on Issue
- [x] BULLRUN phases complete

## Where to change
- `projection/input.py`, `extraction_policy.py`, `mapper.py`

## Out of scope
SPA map UX. Invent coords.
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
rg -n "geo_detail_level|detail_level" doge-complaints-gateway/src/core/projection/
```
