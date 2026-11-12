# task-gw-ssr-19-t01-types-schema-context

## Task: implement — dataclass on SchemaContext (T01)

## Meta
- **Story:** [STORY-GW-SSR-19](../STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000076
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-08-30T19:16:21Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md` T01

## Purpose
Dataclass(es) on `SchemaContext` for `node_clustering.civic` fields listed in story In: `active_lenses`, `primary_lens`, `min_size`, `min_size_by_lens`, `readiness_threshold`, `signal_source`, `id_algorithm`, `geo_filter`, `geo_scope`, `tie_breaker`, `type_resolution`.

## Code Facts
- `SchemaContext` has exact/dual/card; **no** `node_clustering` — [`contracts.py:52–60`](../../../../../../../src/core/schema/contracts.py)
- Civic knobs only AppConfig — [`schema.py:47–59`](../../../../../../../src/core/config/schema.py)
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] `node_clustering.civic` представлен на `SchemaContext` (dataclass)
- [x] Нет новых членов `ClusterLens`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/contracts.py` `:52–60`

## Out of scope
- Новые `ClusterLens` members. Factory wire (→20).
- Overlay bans (every task):
  - **`node_clustering.civic` loader + pack data only.** No factory / handler wire (→20).
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **No cron in pack.** `CLUSTER_CRON_*` stay env (D-SSR-9).
  - **No env override** «поверх pack» this story.
  - **Values from current EnvSpec / conftest defaults.** Do not invent new thresholds.
  - **Нет `GET /schema-active`.** Нет filter HTTP. Нет `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет new SQL. Нет IDX.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–18. Не стартовать 20/21/22…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "node_clustering|class SchemaContext" doge-complaints-gateway/src/core/schema/contracts.py
rg -n "class ClusterLens" -A 14 doge-complaints-gateway/src/core/cluster/types.py
```
