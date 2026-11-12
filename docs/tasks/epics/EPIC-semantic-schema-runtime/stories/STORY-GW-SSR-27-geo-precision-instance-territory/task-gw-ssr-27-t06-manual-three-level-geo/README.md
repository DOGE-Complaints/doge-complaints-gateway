# task-gw-ssr-27-t06-manual-three-level-geo

## Task: docs — three-level geo in node-data-model manual (T06)

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084
- **Skill declared:** python-pro
- **Depends on:** T00–T05
- **Scaffolded:** 2026-09-01T13:12:45Z
- **Completed:** 2026-09-01T13:21:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`

## Purpose
Update `schema-packs-node-data-model-ru.md`: §three-level geo (node / instance / precision); cross-link GPT-SSR-08 and GPT-SSR-06 §6. Coordinate with SSR-29 if same manual pass later.

## Code Facts
- Manual has geo_detail / geo_intake (SSR-25) — [`schema-packs-node-data-model-ru.md`](../../../../../../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md)
- No three-level instance/precision section this scaffold

## Acceptance / DoD
- [x] Manual §three-level geo present
- [x] Cross-links GPT-SSR-08 / GPT-SSR-06 §6
- [x] No conflicting taxonomy layout invent (SSR-29 owns taxonomy §)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`

## Out of scope
GPT instruction edits. Taxonomy SSR-29 full section invent.
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
rg -n "gpt_instance_territory|detail_level|three-level|три уровня" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
