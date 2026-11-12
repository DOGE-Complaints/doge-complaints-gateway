# task-gw-ssr-20-t02-handlers-geo-scope

## Task: implement — handlers geo_scope from active pack (T02)

## Meta
- **Story:** [STORY-GW-SSR-20](../STORY-GW-SSR-20-node-clustering-runtime-wire.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000077
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T19:31:05Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md` T02

## Purpose
`handlers.py` `geo_scope` из того же активного pack `node_clustering.civic`, не `config.cluster_geo_scope`. No new HTTP path.

## Code Facts
- Handlers geo from config — [`handlers.py:253`](../../../../../../../src/core/api/handlers.py) `dependencies.config.cluster_geo_scope`
- Civic `geo_scope` already parsed on pack — [`resolver.py`](../../../../../../../src/core/schema/resolver.py) / [`contracts.py`](../../../../../../../src/core/schema/contracts.py)

## Acceptance / DoD
- [ ] Handlers geo_scope из pack активного `NODE_SCHEMA_*`
- [ ] Нет нового HTTP path / `GET /schema-active`
- [ ] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/api/handlers.py` `:253`

## Out of scope
- Новый HTTP path. Filter HTTP. Env override.
- Overlay bans (every task):
  - Factory/handlers from **active** pack `node_clustering.civic`. No env override поверх pack.
  - Remove semantic `CLUSTER_*` from AppConfig; **keep** `CLUSTER_CRON_*`.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет filter HTTP. Нет IDX.
  - Не менять civic `require_actionable_canonical_type=True` (только числа из pack).
  - **Нет SSR-06/07/12.** Не reopen 01–19. Не стартовать 21/22…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "cluster_geo_scope|node_clustering|geo_scope" doge-complaints-gateway/src/core/api/handlers.py
```
