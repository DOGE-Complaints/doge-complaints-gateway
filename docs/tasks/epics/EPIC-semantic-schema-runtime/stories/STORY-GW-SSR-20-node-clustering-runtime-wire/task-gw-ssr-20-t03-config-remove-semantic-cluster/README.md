# task-gw-ssr-20-t03-config-remove-semantic-cluster

## Task: implement — remove semantic CLUSTER_* from AppConfig (T03)

## Meta
- **Story:** [STORY-GW-SSR-20](../STORY-GW-SSR-20-node-clustering-runtime-wire.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000077
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T19:31:05Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md` T03

## Purpose
Убрать семантические `CLUSTER_*` из AppConfig / `ENV_SCHEMA` и dataclass fields. **Оставить** `CLUSTER_CRON_ENABLED`, `CLUSTER_CRON_INTERVAL_S` + `NODE_SCHEMA_*`. Leftover env ignored by OS (не dual-source).

## Code Facts
- AppConfig cluster_* — [`schema.py:47–59`](../../../../../../../src/core/config/schema.py)
- EnvSpec semantic CLUSTER_* — [`schema.py:166–240`](../../../../../../../src/core/config/schema.py)
- Cron EnvSpec stay — [`:241–251`](../../../../../../../src/core/config/schema.py)
- NODE_SCHEMA stay — [`:261–272`](../../../../../../../src/core/config/schema.py)

## Acceptance / DoD
- [ ] Семантические `CLUSTER_*` не в AppConfig / ENV_SCHEMA
- [ ] `CLUSTER_CRON_*` + `NODE_SCHEMA_*` остаются
- [ ] Missing env `CLUSTER_MIN_SIZE` больше не ConfigError
- [ ] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/config/schema.py` (`:47–59`, EnvSpec, parsers)

## Out of scope
- Удалить `CLUSTER_CRON_*`. Env override поверх pack. Глубокий мануал (→21).
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
rg -n "CLUSTER_MIN_SIZE|CLUSTER_ACTIVE_LENSES|CLUSTER_CRON_|NODE_SCHEMA" doge-complaints-gateway/src/core/config/schema.py
```
