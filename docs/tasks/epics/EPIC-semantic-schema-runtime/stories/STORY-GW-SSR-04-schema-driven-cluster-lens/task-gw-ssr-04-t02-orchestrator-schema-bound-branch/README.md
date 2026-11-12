# task-gw-ssr-04-t02-orchestrator-schema-bound-branch

## Meta
- **Story:** [STORY-GW-SSR-04](../STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000064
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-28T14:30:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md` T02

## Purpose
Branch at start of `process_story` / `process_all_pending`: if story has `schema_id`/`bound_schema_version` → pack engine, **not** `_compute_cluster_inputs` / civic `memberships()`. Civic pool excludes those stories. Cron **unchanged** (`cluster_cron.py:64` still `process_all_pending`). Civic tests on unlabeled fixtures stay green. Do not change `list_stories_ready_for_clustering` SQL so civic fixtures vanish.

## Code Facts
- `process_story` — [`cluster_orchestrator.py:80`](../../../../../../../src/core/application/cluster_orchestrator.py); civic `_compute_cluster_inputs` [`:106`](../../../../../../../src/core/application/cluster_orchestrator.py) on all ready
- `process_all_pending` — [`:164`](../../../../../../../src/core/application/cluster_orchestrator.py); civic pool [`:179`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Ready pool — `list_stories_ready_for_clustering()` [`:98`](../../../../../../../src/core/application/cluster_orchestrator.py) / [`:165`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Cron only `process_all_pending` — [`cluster_cron.py:64`](../../../../../../../src/core/scheduler/cluster_cron.py)
- Binding fields — [`contracts.py:69–74`](../../../../../../../src/core/domain/contracts.py) `schema_id` / `bound_schema_version`
- `composite_primary_signal_pair` unknown+unknown — [`engine.py:82–87`](../../../../../../../src/core/cluster/engine.py)

## Acceptance / DoD
- [x] Traces story T02: schema-bound → pack engine; civic pool without those stories
- [x] `cluster_cron.py` still calls `process_all_pending` only (no second job)
- [x] Civic unlabeled fixtures still green; SQL for `list_stories_ready_for_clustering` not rewritten to drop civic fixtures
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/cluster_orchestrator.py`

## Out of scope
- Второй `ClusterCronJob`; мешать pack в civic buckets; pack via `lens_dimension`; менять SQL so civic fixtures пропадут
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
- SSR-04 extras: no `CLUSTERED`; no `POLICE_STATION` on enum.

## Verification commands
```bash
rg -n "def process_story|def process_all_pending|_compute_cluster_inputs" doge-complaints-gateway/src/core/application/cluster_orchestrator.py
rg -n "process_all_pending" doge-complaints-gateway/src/core/scheduler/cluster_cron.py
rg -n "class ClusterCronJob" doge-complaints-gateway/src/core/scheduler/cluster_cron.py
```
