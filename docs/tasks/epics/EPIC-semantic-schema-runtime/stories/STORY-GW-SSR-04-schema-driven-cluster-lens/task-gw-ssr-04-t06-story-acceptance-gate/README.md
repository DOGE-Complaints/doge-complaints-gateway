# task-gw-ssr-04-t06-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-SSR-04](../STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000064
- **Skill declared:** python-pro
- **Depends on:** T01–T05 Done
- **Scaffolded:** 2026-08-28T14:30:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md` T06 + Target / AC

## Purpose
Story acceptance: exact membership without new `ClusterLens`; civic clustering green; cron still `process_all_pending`; rg `class ClusterLens` baseline; no `POLICE_STATION`/`police_station` in `types.py`/`engine.py`. SSR INDEX/dashboard at P3 Done — **not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка». Wave dashboard: `gateway-semantic-schema-runtime-dashboard.md`.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-04-….md`](../STORY-GW-SSR-04-schema-driven-cluster-lens.md) §Target / AC (verbatim)
- G4 commands — [`orchestrator-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) §6.4
- Gate **Date:** only after `--print-utc-now` post live pytest + `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done) — **not** `gateway-mvp-dashboard.md`

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-04.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] All story Target / AC covered (AC-007; AC-008; CL-004; SEC-004)
- [x] G4 rg: `ClusterLens` baseline; no `POLICE_STATION`/`police_station` in `types.py`/`engine.py`; `cluster_cron.py` still `process_all_pending`
- [x] Live verify commands + `--project gateway --verify` (+ tests) recorded
- **Date:** 2026-08-28T14:36:12Z
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`. SSR INDEX/dashboard recount at P3 Done only.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-04.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold

## Out of scope
- Implementing missing product gaps; P3 execution
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
- SSR-04 extras: no second cron; no `CLUSTERED`; no invent pack YAML keys.

## Verification commands
```bash
# P3 only (G4):
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
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
