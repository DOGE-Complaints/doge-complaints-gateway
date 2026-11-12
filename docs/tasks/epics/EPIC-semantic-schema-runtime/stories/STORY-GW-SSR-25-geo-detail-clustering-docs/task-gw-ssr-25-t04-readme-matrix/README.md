# task-gw-ssr-25-t04-readme-matrix

## Task: add — README сверка + test-matrix (T04)

## Meta
- **Story:** [STORY-GW-SSR-25](../STORY-GW-SSR-25-geo-detail-clustering-docs.md)
- **Type:** docs
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:31:59Z
- **Package:** pkg-000082
- **Skill declared:** python-pro
- **Depends on:** T03
- **Scaffolded:** 2026-08-30T21:20:50Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-25-geo-detail-clustering-docs.md` T04

## Purpose
Сверка [`schema-packs/README.md`](../../../../../../../schema-packs/README.md) с мануалом; одна правка smoke / [test-matrix](../../../../../../../docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md). Не переписывать T-wave G3.

## Code Facts
1. **As-of-Done (SSR-25 pkg-000082):** README сверка civic `admin_*` vs pack `geo.*` — [`schema-packs/README.md`](../../../../../../../schema-packs/README.md) §geo_intake.
2. **As-of-Done:** test-matrix row `test_gw_ssr_25_*.py` — [`test-matrix-by-type-layer-mocks.md`](../../../../../../../docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md).
3. T-wave G3 historical **не** переписан — [`orchestrator-t-wave-runbook.md:271`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md).
4. **Historical (P1 scaffold):** test-matrix **без** SSR-25.

## Acceptance / DoD
- [x] README сверка с мануалом (без противоречий)
- [x] test-matrix одна правка (story tests / geo_intake)
- [x] T-wave G3 `:271` **не** переписан
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/README.md` (сверка, не rewrite)
- `doge-complaints-gateway/docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md`

## Out of scope
- Manual chapter body (T03). Gate (T05). T-wave G3 rewrite.
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
rg -n "geo_intake|geo_detail" doge-complaints-gateway/schema-packs/README.md
rg -n "test_gw_ssr_25|geo_intake" doge-complaints-gateway/docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md
sed -n '271p' doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```
