# task-gw-ssr-04-t04-lifecycle-keep-ready-for-profile

## Meta
- **Story:** [STORY-GW-SSR-04](../STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000064
- **Skill declared:** python-pro
- **Depends on:** T02, T03
- **Scaffolded:** 2026-08-28T14:30:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md` T04

## Purpose
Do **not** set `CLUSTERED` (SSR-05 after promote). Pack-story stays `READY_FOR_PROFILE`. Repeat cron must not duplicate membership (T03 upsert). Do not copy civic «membership only after issue».

## Code Facts
- Civic `CLUSTERED` after successful issue — [`cluster_orchestrator.py:367–370`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic `_create_issue_for_cluster` — [`:269`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic skip if already `CLUSTERED` — [`:85–90`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Ready gate — [`:91–96`](../../../../../../../src/core/application/cluster_orchestrator.py) `READY_FOR_PROFILE`
- sqlite upsert membership — [`db_sqlite.py:1457–1467`](../../../../../../../src/core/infrastructure/db_sqlite.py)

## Acceptance / DoD
- [x] Traces story T04: pack path does not `update_lifecycle_status(…, CLUSTERED)`
- [x] Pack path skips `_create_issue_for_cluster`
- [x] Repeat cron does not duplicate membership (T03 upsert)
- [x] BULLRUN phases complete

## Where to change
- Pack path in `doge-complaints-gateway/src/core/application/cluster_orchestrator.py` — skip `update_lifecycle_status(…, CLUSTERED)` and skip `_create_issue_for_cluster`

## Out of scope
- Promote / `PromotionGatePolicy` override (SSR-05); invent promotion thresholds; copy civic «membership only after issue»
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
- SSR-04 extras: no second cron; no `POLICE_STATION` on enum.

## Verification commands
```bash
rg -n "CLUSTERED|_create_issue_for_cluster|update_lifecycle_status" doge-complaints-gateway/src/core/application/cluster_orchestrator.py
rg -n "require_actionable_canonical_type: bool = True" doge-complaints-gateway/src/core/promotion/gates.py
```
