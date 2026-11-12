# task-gw-ssr-21-t02-env-docs-inventory

## Task: docs — 05-env + server-env: семантика → pack; cron stay (T02)

## Meta
- **Story:** [STORY-GW-SSR-21](../STORY-GW-SSR-21-node-clustering-docs.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000078
- **Skill declared:** python-pro
- **Depends on:** T01 (мануал как цель ссылки)
- **Scaffolded:** 2026-08-30T19:50:48Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md` T02

## Purpose
`05-env-config-and-launch.md` строки про семантические CLUSTER_* (≈111–120) → «перенесено в pack / см. мануал»; оставить `CLUSTER_CRON_*`. `server-env-quickstart.md` — убрать обязательность/инструкции семантических CLUSTER_* как текущий путь кастомизации.

## Code Facts
- 05-env учит CLUSTER_* из env — [`05-env-config-and-launch.md:111–122`](../../../../../../../runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md); cron `:121–122`
- server-env CLUSTER_ACTIVE_LENSES обязателен — [`server-env-quickstart.md:118–121,143–144,347–349`](../../../../../../../runtime-docs/manuals/server-env-quickstart.md)
- AppConfig as-of-Done SSR-20: только `cluster_cron_*` + `NODE_SCHEMA_*` — [`schema.py:50–56`](../../../../../../../src/core/config/schema.py)

## Acceptance / DoD
- [x] `05-env-config-and-launch.md` не учит строки 111–120 как текущий SSOT; cron documented
- [x] `server-env-quickstart.md` не требует семантические CLUSTER_* для кастомизации
- [x] `CLUSTER_CRON_*` остаются в env docs (не удалять cron)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md` `:111–122`
- `doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md` `:118+`

## Out of scope
- Удалить cron из docs. Product AppConfig. T-wave G3. Closed audits.
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
rg -n "CLUSTER_MIN_SIZE|CLUSTER_ACTIVE_LENSES|CLUSTER_PRIMARY_LENS|CLUSTER_GEO_SCOPE" \
  doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md
rg -n "CLUSTER_CRON" doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md
rg -n "CLUSTER_ACTIVE_LENSES|CLUSTER_PRIMARY_LENS" \
  doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md
```
