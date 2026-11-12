# task-gw-ssr-21-t01-manual-two-contours

## Task: docs — глава двух контуров + how-to knobs (T01)

## Meta
- **Story:** [STORY-GW-SSR-21](../STORY-GW-SSR-21-node-clustering-docs.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000078
- **Skill declared:** python-pro
- **Depends on:** SSR-20 Done (G20)
- **Scaffolded:** 2026-08-30T19:50:48Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md` T01

## Purpose
Глубокая глава в `schema-packs-node-data-model-ru.md`: склад vs рабочая `NODE_SCHEMA_*`; **два контура** (`exact_lenses` vs `node_clustering.civic`); как сменить пороги/линзы/geo **без** `.env` (правка активного pack + рестарт); dual; unbound legacy; cron = процесс.

## Code Facts
- Мануал: склад / `NODE_SCHEMA_*` / dual / unbound; rg `node_clustering` empty — [`schema-packs-node-data-model-ru.md`](../../../../../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md)
- Civic knobs as-of-Done SSR-20 — [`service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py); [`schema.py:50–56`](../../../../../../../src/core/config/schema.py)
- Pack civic key already documented (SSR-19) — [`schema-packs/README.md:60–78`](../../../../../../../../schema-packs/README.md)
- `ClusterLens` = 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] Мануал явно разделяет `exact_lenses` vs `node_clustering.civic`
- [x] Операторский путь смены порогов/линз/geo = правка активного pack + рестарт
- [x] Dual / unbound legacy / cron=процесс описаны без dual-source env+pack
- [x] Не invent `GET /schema-active`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`

## Out of scope
- Product runtime. Env inventory (T02). README/matrix (T03). Invent HTTP schema-active.
- Overlay bans (every task):
  - Docs only. No product runtime except doc-driven typos.
  - Semantic `CLUSTER_*` documented as **moved to pack**. **Keep** `CLUSTER_CRON_*` in env docs.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет invent HTTP. Нет IDX.
  - Не учить «клиент выбирает pack». Не учить dual-source env+pack.
  - Geo `settlement:tallinn` в pack tallinn — данные зоны, не URL `/tallinn`.
  - **Не переписывать T-wave G3** (`orchestrator-t-wave-runbook.md:271`).
  - **Нет SSR-06/07/12.** Не reopen 01–20. Не стартовать 22…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать. Closed audits не в diff.

## Verification commands
```bash
rg -n "node_clustering|exact_lenses" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
