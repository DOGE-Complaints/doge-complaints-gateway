# task-gw-ssr-04-t01-pack-engine-exact-membership

## Meta
- **Story:** [STORY-GW-SSR-04](../STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000064
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-28T14:30:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md` T01

## Purpose
New `SchemaPackClusterEngine` (working name) in `src/core/schema/` **or** `src/core/cluster/pack_engine.py`. Exact membership from pack `exact_lenses[].source_fields` dotted paths on `structured_payload`. Unknown/missing path → typed skip/error per pack `missing_value_policy` (example: `skip`). `cluster_id` = `schema:<schema_id>:<lens_id>:…` joined field values — **not** `SignalDimension` / `stable_cluster_id(ClusterLens, …)`. No `ClusterLens` member. Do not call `readiness_score_for_cluster` / `build_cluster_narrative`.

## Code Facts
- `ClusterLens` civic-only — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- `lens_dimension` exhaustive — [`engine.py:66–79`](../../../../../../../src/core/cluster/engine.py)
- `stable_cluster_id(lens: ClusterLens, …)` prefix `cluster:` — [`engine.py:130–136`](../../../../../../../src/core/cluster/engine.py)
- `build_cluster_narrative` / `readiness_score_for_cluster` — [`engine.py:162`](../../../../../../../src/core/cluster/engine.py), [`:192`](../../../../../../../src/core/cluster/engine.py)
- SSR-01 loader `ExactLensBlock` — [`schema/contracts.py:39–48`](../../../../../../../src/core/schema/contracts.py); [`resolver.py:46`](../../../../../../../src/core/schema/resolver.py) / [`:91–101`](../../../../../../../src/core/schema/resolver.py)
- Example path — [`legal_process/v1/pack.json`](../../../../../../../schema-packs/legal_process/v1/pack.json) `lens_id=police_station` `source_fields=["institution.office_id"]` `missing_value_policy=skip`
- Pack membership engine — [`pack_engine.py`](../../../../../../../src/core/schema/pack_engine.py) `SchemaPackClusterEngine` / `pack_cluster_id`

## Acceptance / DoD
- [x] Traces story T01: exact membership from payload paths
- [x] Unknown path → skip/error typed per `missing_value_policy`
- [x] `cluster_id` namespaced `schema:<schema_id>:<lens_id>:…`
- [x] No `ClusterLens` member; no `readiness_score_for_cluster` / `build_cluster_narrative` for pack
- [x] BULLRUN phases complete

## Where to change
- new module: `doge-complaints-gateway/src/core/schema/` **or** `src/core/cluster/pack_engine.py` (consume SSR-01 `ExactLensBlock` / `LocalSchemaRuntime.resolve`)

## Out of scope
- Править `lens_dimension` dict; `POLICE_STATION` on enum; copy raw payload into narrative string; invent pack YAML keys
- INDEX/runbook §4 + §8 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :108–111).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44` — `cluster_memberships` уже есть).
  - Не invent HTTP filter / новый intake path. OpenAPI only existing paths. `GET /tallinn/issues` must stay (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
- SSR-04 extras: no second cron; no `CLUSTERED`; no pack via civic `lens_dimension`.

## Verification commands
```bash
rg -n "class ClusterLens" -A 14 doge-complaints-gateway/src/core/cluster/types.py
rg -n "POLICE_STATION|SchemaPackClusterEngine|pack_engine" doge-complaints-gateway/src/core/cluster doge-complaints-gateway/src/core/schema
rg -n "stable_cluster_id|build_cluster_narrative|readiness_score_for_cluster" doge-complaints-gateway/src/core/cluster/engine.py
```
