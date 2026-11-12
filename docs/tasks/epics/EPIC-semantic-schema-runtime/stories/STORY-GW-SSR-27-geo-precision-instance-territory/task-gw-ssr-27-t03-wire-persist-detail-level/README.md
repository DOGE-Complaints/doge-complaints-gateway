# task-gw-ssr-27-t03-wire-persist-detail-level

## Task: implement — detail_level wire + persist + migration (T03)

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-09-01T13:12:45Z
- **Completed:** 2026-09-01T13:21:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`

## Purpose
Intake `detail_level` on GeoDetail; `StoryGeoSnapshot.detail_level`; SQLite/Supabase column + migration omit-probe (SSR-24 pattern); tallinn `payload.schema.json` enum; keep no invented lat/lon when provider None.

## Code Facts
1. **As-of-Done (SSR-27 pkg-000084):** `detail_level` in `GEO_DETAIL_ALLOWED_KEYS` / `GeoDetail` — [`intake/contracts.py`](../../../../../../../src/core/intake/contracts.py); `StoryGeoSnapshot.detail_level` — [`domain/contracts.py`](../../../../../../../src/core/domain/contracts.py); sqlite/supabase `geo_detail_level` + migration `20260901_1315_gw_ssr_27_stories_geo_detail_level.sql` (omit-probe; SSR-24 column set unchanged).
2. SSR-24 migration pattern retained — `supabase/migrations/20260830_2100_gw_ssr_24_stories_geo_detail.sql`.
3. Regression anchors: `test_gw_ssr_23_*`, `test_gw_ssr_24_*`, `test_gw_ssr_25_*`.
4. **Historical (pre-P3 / P1 scaffold):** no `detail_level` on GeoDetail / snapshot.

## Acceptance / DoD
- [x] Parse validates ∈ GEO_PRECISION_LEVELS; `geo_detail_has_values` treats detail_level
- [x] Snapshot + DB column + adapters; omit-probe; not in required_columns_ready
- [x] payload.schema.json optional enum
- [x] SSR-24 migration test still SSR-24-only columns
- [x] No invented 0.0 coords
- [x] BULLRUN phases complete

## Where to change
- intake/domain/geo merge; db_sqlite/db_supabase; migration; tallinn payload.schema.json

## Out of scope
Projection UC-G03 (→T04). Full region-only snapshot without coords policy invent.
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
rg -n "detail_level|geo_detail_level" doge-complaints-gateway/src/core/intake/contracts.py doge-complaints-gateway/src/core/domain/contracts.py doge-complaints-gateway/src/core/infrastructure/
```
