# task-gw-ssr-21-t03-readme-matrix-sync

## Task: docs — сверка README; test-matrix при необходимости (T03)

## Meta
- **Story:** [STORY-GW-SSR-21](../STORY-GW-SSR-21-node-clustering-docs.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000078
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-08-30T19:50:48Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md` T03

## Purpose
Сверка [`schema-packs/README.md`](../../../../../../../../schema-packs/README.md) (ключ уже с 19; убрать stale «factory still reads AppConfig CLUSTER_* until SSR-20»). Smoke / [`test-matrix`](../../../../../../../runtime-docs/testing/test-matrix-by-type-layer-mocks.md) — одна правка если упоминает `CLUSTER_ACTIVE_LENSES` как единственный способ.

## Code Facts
- README civic key + stale factory note — [`schema-packs/README.md:30,60–78`](../../../../../../../../schema-packs/README.md)
- test-matrix CLUSTER_ACTIVE_LENSES — [`test-matrix-by-type-layer-mocks.md:79`](../../../../../../../runtime-docs/testing/test-matrix-by-type-layer-mocks.md)
- As-of-Done SSR-20 factory from pack — [`service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py)

## Acceptance / DoD
- [x] `schema-packs/README.md` не учит factory из AppConfig `CLUSTER_*` как текущий контракт
- [x] test-matrix / smoke: одна правка только если `CLUSTER_ACTIVE_LENSES` как единственный способ; иначе N/A
- [x] Closed audits не в diff
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/README.md`
- `doge-complaints-gateway/docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md` (если нужно)

## Out of scope
- Перепись audits. Product tests rewrite. T-wave G3.
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
rg -n "Factory still reads AppConfig|CLUSTER_ACTIVE_LENSES" \
  doge-complaints-gateway/schema-packs/README.md \
  doge-complaints-gateway/docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md
```
