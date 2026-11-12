# task-gw-ssr-04-t03-persist-membership-before-issue

## Meta
- **Story:** [STORY-GW-SSR-04](../STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000064
- **Skill declared:** python-pro
- **Depends on:** T01, T02
- **Scaffolded:** 2026-08-28T14:30:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md` T03

## Purpose
`ClusterMembershipStore.save_membership` **before** Issue. `lens` = pack `lens_id` (string). Idempotent upsert — sqlite already `ON CONFLICT(story_id, lens)` (`db_sqlite.py:1457–1467`); use stores as-is. For pack-bound: **do not** write civic memberships. CL-004: pack lens ids + civic lens ids on one `story_id` only if civic was not run; pack-bound civic memberships not written.

## Code Facts
- Protocol — [`contracts.py:213–218`](../../../../../../../src/core/domain/contracts.py) `save_membership(story_id, lens, cluster_id)` `lens: str`
- sqlite table PK `(story_id, lens)` — [`db_sqlite.py:411–417`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- sqlite upsert — [`db_sqlite.py:1457–1467`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- in-memory — [`repositories.py:456–458`](../../../../../../../src/core/infrastructure/repositories.py)
- supabase — [`db_supabase.py:1311`](../../../../../../../src/core/infrastructure/db_supabase.py)
- Civic `_persist_memberships` iterates `active_lenses: ClusterLens` — [`cluster_orchestrator.py:397–414`](../../../../../../../src/core/application/cluster_orchestrator.py)
- `REQUIRED_READINESS_TABLES` already includes `cluster_memberships` — [`db_supabase.py:30–44`](../../../../../../../src/core/infrastructure/db_supabase.py)

## Acceptance / DoD
- [x] Traces story T03: `save_membership` before Issue; idempotent upsert
- [x] `lens` = pack `lens_id` string; no new table
- [x] Pack-bound does not call civic `_persist_memberships`
- [x] BULLRUN phases complete

## Where to change
- Pack path in `doge-complaints-gateway/src/core/application/cluster_orchestrator.py` calling existing sqlite/supabase/in-memory stores

## Out of scope
- Новая таблица; civic `_persist_memberships`; add `cluster_memberships` again to `REQUIRED_READINESS_TABLES`
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
- SSR-04 extras: no `CLUSTERED`; no second cron.

## Verification commands
```bash
rg -n "def save_membership|ON CONFLICT" doge-complaints-gateway/src/core/infrastructure/db_sqlite.py
rg -n "def _persist_memberships" doge-complaints-gateway/src/core/application/cluster_orchestrator.py
rg -n "cluster_memberships" doge-complaints-gateway/src/core/infrastructure/db_supabase.py
```
