# task-gw-ssr-27-t01-types-geo-precision

## Task: implement — GeoModel + GptInstanceTerritory on SchemaContext (T01)

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-09-01T13:12:45Z
- **Completed:** 2026-09-01T13:21:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`

## Purpose
Add `GEO_PRECISION_LEVELS`, `GPT_INSTANCE_RULE_TYPES`; dataclasses `GeoModelBlock`, `GptInstanceTerritoryRule`, `GptInstanceTerritoryBlock`; optional `SchemaContext.geo_model` / `SchemaContext.gpt_instance_territory`.

## Code Facts
1. **As-of-Done (SSR-27 pkg-000084):** `GEO_PRECISION_LEVELS` / `GPT_INSTANCE_RULE_TYPES` / `GeoModelBlock` / `GptInstanceTerritory*` / `SchemaContext.geo_model` + `gpt_instance_territory` — [`contracts.py`](../../../../../../../src/core/schema/contracts.py).
2. `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py).
3. **Historical (pre-P3 / P1 scaffold):** `SchemaContext` had `taxonomy` (SSR-26) but **no** geo_model / gpt_instance_territory.

## Acceptance / DoD
- [x] Frozen sets + dataclasses importable
- [x] Optional SchemaContext fields default None / absent-safe
- [x] No ClusterLens change
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/contracts.py`

## Out of scope
Loader wire (→T02). Wire/persist (→T03).
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
cd doge-complaints-gateway
python3 -c "from core.schema.contracts import GEO_PRECISION_LEVELS, GeoModelBlock, GptInstanceTerritoryBlock, SchemaContext"
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```
