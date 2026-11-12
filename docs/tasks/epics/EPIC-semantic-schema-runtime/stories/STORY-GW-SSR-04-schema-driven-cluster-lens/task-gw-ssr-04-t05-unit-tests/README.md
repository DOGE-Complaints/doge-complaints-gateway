# task-gw-ssr-04-t05-unit-tests

## Meta
- **Story:** [STORY-GW-SSR-04](../STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- **Type:** test
- **Status:** 🔵 Done
- **Package:** pkg-000064
- **Skill declared:** python-pro
- **Depends on:** T01–T04
- **Scaffolded:** 2026-08-28T14:30:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md` T05

## Purpose
Two stories same `institution.office_id` (example path) → same `cluster_id`. Civic `test_clustering_engine.py` unchanged green. No new enum value in `types.py`. Schema-bound does not enter civic buckets. G4 also: `test_gw_tax_02_*`, `test_story_cluster_orchestrator.py`, `test_cluster_cron_job.py`, `test_e2e_story_cluster_issue_pipeline.py`. Engine MAY fixture `StoryRecord` with payload (wire not required for unit).

## Code Facts
- Example path — [`legal_process/v1/pack.json`](../../../../../../../schema-packs/legal_process/v1/pack.json) `source_fields=["institution.office_id"]`
- `ClusterLens` baseline — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Binding on `StoryRecord` — [`contracts.py:69–74`](../../../../../../../src/core/domain/contracts.py)
- G4 bundle — [`orchestrator-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) §6.4
- Civic tests — `tests/test_clustering_engine.py` `tests/test_gw_tax_02_cluster_axis_expansion.py`

## Acceptance / DoD
- [x] Traces story T05: two stories same `institution.office_id` → same `cluster_id`
- [x] Civic `test_clustering_engine.py` unchanged green; no new enum in `types.py`
- [x] Schema-bound not in civic buckets
- [x] `tests/test_gw_ssr_04_*` exist; G4 civic/cron/e2e still pass
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_04_*`

## Out of scope
- Live hosted as only proof; expand `ClusterLens` in tests as product; implement SSR-05 promote
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
- SSR-04 extras: no second cron; no `CLUSTERED`.

## Verification commands
```bash
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_04_*.py \
  tests/test_clustering_engine.py \
  tests/test_gw_tax_02_cluster_axis_expansion.py \
  tests/test_story_cluster_orchestrator.py \
  tests/test_cluster_cron_job.py \
  tests/test_e2e_story_cluster_issue_pipeline.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "POLICE_STATION|police_station" src/core/cluster/types.py src/core/cluster/engine.py
```
