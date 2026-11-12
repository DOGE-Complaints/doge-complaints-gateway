# task-gw-ssr-27-t02-loader-geo-blocks

## Task: implement — parse geo_model + gpt_instance_territory (T02)

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-01T13:12:45Z
- **Completed:** 2026-09-01T13:21:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`

## Purpose
`_parse_geo_model(manifest)` and `_parse_gpt_instance_territory(manifest)` — optional absent; validate precision levels and rule types (`admin_id`/`admin_token`/`bbox`). Wire in `load_pack()` parallel to taxonomy.

## Code Facts
1. **As-of-Done (SSR-27 pkg-000084):** `_parse_geo_model` / `_parse_gpt_instance_territory` + `load_pack` wire — [`resolver.py`](../../../../../../../src/core/schema/resolver.py).
2. Gateway MVP: **parse only** for instance territory; enforce deferred to GPT.
3. **Historical (pre-P3 / P1 scaffold):** `load_pack` wired taxonomy (SSR-26) only; **no** geo_model / gpt_instance_territory parse.

## Acceptance / DoD
- [x] Absent keys → None / default; legal/mobility unchanged
- [x] Invalid precision level / rule → `UnsupportedVersionError`
- [x] Rule types admin_id, admin_token, bbox validated
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/resolver.py`

## Out of scope
Gateway intake bbox enforce. Tallinn invent seed without OP.
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
rg -n "_parse_geo_model|_parse_gpt_instance_territory|geo_model=" doge-complaints-gateway/src/core/schema/resolver.py
```
