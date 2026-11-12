# task-gw-ssr-18-t04-docs-warehouse-vs-env

## Task: docs — warehouse vs NODE_SCHEMA_* (T04)

## Meta
- **Story:** [STORY-GW-SSR-18](../STORY-GW-SSR-18-cluster-active-schema.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000075
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-08-30T14:55:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md` T04

## Purpose
Мануал человеческий: склад vs `NODE_SCHEMA_*`; intake 4xx; кластеризация с сервера. Smoke matrix: canvas/smoke payload `schema_binding` = env. Не учить «клиент выбирает любой pack» / «решает тело intake» как текущий контракт.

## Code Facts
- Manual — [`schema-packs-node-data-model-ru.md`](../../../../../../../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md)
- Test-matrix — [`test-matrix-by-type-layer-mocks.md`](../../../../../../../docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md)
- G18 rg — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.3

## Acceptance / DoD
- [x] Мануал: склад vs `NODE_SCHEMA_*`; intake 4xx; кластеризация с сервера
- [x] Мануал **не** учит «клиент выбирает любой pack» / «решает тело intake» как текущий контракт
- [x] Smoke docs: binding в payload = env процесса
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`
- `doge-complaints-gateway/docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md`

## Out of scope
- Перепись T-wave G3. GPT UI. `gateway-mvp-dashboard.md`.
- Overlay bans (every task):
  - **Cluster only active pack.** Persist pair ≠ `NODE_SCHEMA_*` → skip (лог), не membership чужим pack.json.
  - **Unbound civic as-is.** `_civic_ready` stays unbound-only. Не migrate civic rows.
  - **Dual only from active pack.json.** Не подменять `story.schema_id` на env.
  - **Нет смены `ClusterLens`.** Civic engine **не** удалять. Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет нового cron. Нет new SQL. Нет IDX.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–17. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "клиент выбирает любой pack|решает тело intake" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
