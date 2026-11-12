# task-gw-ssr-25-t03-manual-geo-intake

## Task: add — manual chapter geo_detail / geo_intake / cluster (T03)

## Meta
- **Story:** [STORY-GW-SSR-25](../STORY-GW-SSR-25-geo-detail-clustering-docs.md)
- **Type:** docs
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:31:59Z
- **Package:** pkg-000082
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-08-30T21:20:50Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-25-geo-detail-clustering-docs.md` T03

## Purpose
Глава в мануале: `geo_detail`, `geo_intake` modes, mirror, два пути cluster (civic vs exact). Не invent `GET /schema-active`.

## Code Facts
1. **As-of-Done (SSR-25 pkg-000082):** глава `geo_detail` / `geo_intake` / civic vs exact — [`schema-packs-node-data-model-ru.md`](../../../../../../../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md) §geo_detail.
2. README already documents SSR-23 sidecar — [`schema-packs/README.md:31`](../../../../../../../schema-packs/README.md), [`:81–102`](../../../../../../../schema-packs/README.md).
3. Civic vs pack paths — [`engine.py`](../../../../../../../src/core/cluster/engine.py) vs [`pack_engine.py:57`](../../../../../../../src/core/schema/pack_engine.py).
4. **Historical (P1 scaffold):** manual **без** `geo_intake` / `geo_detail`.

## Acceptance / DoD
- [x] Мануал: modes, mirror, civic vs exact
- [x] Нет `GET /schema-active` / HTTP geo-filter
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`

## Out of scope
- README/matrix (T04). Runtime cluster code (T01/T02). Gate (T05).
- Overlay bans (every task):
  - Civic/pack cluster regression; manuals `geo_intake`; README/matrix; tests `test_gw_ssr_25_*`.
  - G25 = **full** offline pytest (`-m "not live_integration"`) + `test_clustering_engine.py` + `test_gw_ssr_25_*`.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет invent HTTP geo-filter API. Нет IDX / QRY / `story_dimensions`. Нет GPT UI / instruction pack. Нет SPA map overlay.
  - Civic `geo_filter_bucket` остаётся `admin_*`. Не dual-source env+pack для geo knobs (D-SSR-9).
  - **Нет SSR-06/07/12.** Не reopen 01–24 product. Не стартовать 26.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "geo_intake|geo_detail" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
