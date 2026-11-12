# task-gw-ssr-27-t00-contract-readme

## Task: add — document geo_model + gpt_instance_territory + detail_level (T00)

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084
- **Skill declared:** python-pro
- **Depends on:** SSR-25 Done; SSR-26 Done (orthogonal)
- **Scaffolded:** 2026-09-01T13:12:45Z
- **Completed:** 2026-09-01T13:21:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`

## Purpose
Document `geo_model`, `gpt_instance_territory`, and `detail_level` (wire/snapshot/projection) in `schema-packs/README.md`. Clarify three-level geo: node `geo_scope` vs instance territory vs precision.

## Code Facts
1. **As-of-Done (SSR-27 pkg-000084):** README documents `geo_model` + `gpt_instance_territory` + three-level geo + `detail_level` — [`schema-packs/README.md`](../../../../../../../schema-packs/README.md).
2. Node scope as-built — tallinn `geo_scope=settlement:tallinn` (unchanged SSR-22).
3. **Historical (pre-P3 / P1 scaffold):** README had taxonomy keys but **no** `geo_model` / `gpt_instance_territory` / `detail_level` pack blocks.
4. Story T00 — backlog SSR-27.

## Acceptance / DoD
- [x] README documents `geo_model` + `gpt_instance_territory` + `detail_level` layers
- [x] Node vs instance vs precision separation explicit
- [x] Not frozen YAML dialect invent
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/README.md`

## Out of scope
Tallinn invent district/bbox seed. Full manual (→T06). Taxonomy SSR-28/29.
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
rg -n "geo_model|gpt_instance_territory|detail_level" doge-complaints-gateway/schema-packs/README.md
```
