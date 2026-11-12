# task-gw-ssr-20-t01-factory-pack-wire

## Task: implement — engine + civic gate + orchestrator min from active pack (T01)

## Meta
- **Story:** [STORY-GW-SSR-20](../STORY-GW-SSR-20-node-clustering-runtime-wire.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000077
- **Skill declared:** python-pro
- **Depends on:** SSR-19 Done (G19)
- **Scaffolded:** 2026-08-30T19:31:05Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md` T01

## Purpose
`get_clustering_engine`, civic `PromotionGatePolicy`, orchestrator `cluster_min_size` / `cluster_min_size_by_lens` — из `resolve_pack` активного `(node_schema_id, node_schema_version)` → `node_clustering.civic`. Missing/битый блок → `ConfigError`. No env override.

## Code Facts
- Engine from config — [`service_factory.py:93–104`](../../../../../../../src/core/infrastructure/service_factory.py)
- Civic gate from config — [`:110–113`](../../../../../../../src/core/infrastructure/service_factory.py)
- Orchestrator min from config — [`:158–159`](../../../../../../../src/core/infrastructure/service_factory.py)
- Node pair already on factory — [`:161–162`](../../../../../../../src/core/infrastructure/service_factory.py)
- Civic block on SchemaContext — [`contracts.py`](../../../../../../../src/core/schema/contracts.py) / [`resolver.py`](../../../../../../../src/core/schema/resolver.py)

## Acceptance / DoD
- [ ] Civic `ClusteringEngine` knobs = `node_clustering.civic` активного pack
- [ ] Civic `PromotionGatePolicy` min_readiness / min_stories из pack (не менять `require_actionable_canonical_type=True`)
- [ ] Orchestrator min_size / by_lens из pack
- [ ] Missing/битый `node_clustering` на активном pack → `ConfigError`
- [ ] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/infrastructure/service_factory.py` `:93–104`, `:110–113`, `:158–159`

## Out of scope
- Env override поверх pack. Новый HTTP path. Удаление `CLUSTER_CRON_*`.
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
rg -n "node_clustering|cluster_active_lenses|cluster_min_size" doge-complaints-gateway/src/core/infrastructure/service_factory.py
```
