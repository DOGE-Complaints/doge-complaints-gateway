# task-gw-ssr-20-t04-lifespan-pack-log

## Task: implement — lifespan log pack knobs + cron env (T04)

## Meta
- **Story:** [STORY-GW-SSR-20](../STORY-GW-SSR-20-node-clustering-runtime-wire.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000077
- **Skill declared:** python-pro
- **Depends on:** T01 + T03
- **Scaffolded:** 2026-08-30T19:31:05Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md` T04

## Purpose
Lifespan лог: lenses/min_size/geo из активного pack; cron из env. No payload dump.

## Code Facts
- Startup still logs config cluster_min_size + cron + NODE_SCHEMA — [`asgi_app.py:121–137`](../../../../../../../src/core/api/asgi_app.py)
- Cron loop uses `cluster_cron_enabled` / interval / `min_size_guard=config.cluster_min_size` — [`:165–184`](../../../../../../../src/core/api/asgi_app.py)

## Acceptance / DoD
- [ ] Lifespan лог pack knobs + cron env
- [ ] Нет dump payload
- [ ] Cron still env (`CLUSTER_CRON_*`)
- [ ] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/api/asgi_app.py` `:121–137`, `:165–184`

## Out of scope
- Dump payload. New HTTP. Глубокий мануал (→21).
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
rg -n "cluster_min_size|cluster_cron|node_schema|node_clustering" doge-complaints-gateway/src/core/api/asgi_app.py
```
