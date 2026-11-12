# task-gw-ssr-05-t03-pack-promote-clustered

## Meta
- **Story:** [STORY-GW-SSR-05](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000065
- **Skill declared:** python-pro
- **Depends on:** T01, T02
- **Scaffolded:** 2026-08-28T14:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` T03

## Purpose
Same SSR-04 orchestrator branch: after membership, if pack gate pass → `create_issue` **with override** + `CLUSTERED`. Score: if `len(members) >= pack.min_size`, score ≥ pack `min_readiness_score`; else below threshold (gate fail). **Not** `readiness_score_for_cluster(..., lens: ClusterLens)`.

## Code Facts
- Pack branch membership only — [`cluster_orchestrator.py:89–90`](../../../../../../../src/core/application/cluster_orchestrator.py) `_process_pack_bound_story`; pack `process_story` returns None [`:143–145`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic `_create_issue_for_cluster` — [`:324`](../../../../../../../src/core/application/cluster_orchestrator.py); preview [`:369`](../../../../../../../src/core/application/cluster_orchestrator.py); `CLUSTERED` [`:422–425`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic score — [`engine.py:192`](../../../../../../../src/core/cluster/engine.py) `readiness_score_for_cluster(*, lens: ClusterLens, …)`
- Cron still `process_all_pending` — [`cluster_cron.py:64`](../../../../../../../src/core/scheduler/cluster_cron.py)

## Acceptance / DoD
- [x] Traces story T03: pack gate pass → create_issue with override + CLUSTERED
- [x] Score not from civic `readiness_score_for_cluster`
- [x] Do not use `_create_issue_for_cluster` as-is; no second cron
- [x] CLUSTERED only after successful pack promote
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/cluster_orchestrator.py` pack path (`_process_pack_bound_story`)

## Out of scope
- `_create_issue_for_cluster` as-is; второй cron; `CLUSTERED` before successful promote
- INDEX/runbook §4 + §8 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :108–111).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / новый intake path. OpenAPI only existing paths. `GET /tallinn/issues` must stay (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`.
- SSR-05 extras: 3 knobs from pack file; no QRY; civic promotion tests stay green.

## Verification commands
```bash
rg -n "_process_pack_bound_story|_create_issue_for_cluster|CLUSTERED" doge-complaints-gateway/src/core/application/cluster_orchestrator.py
rg -n "process_all_pending" doge-complaints-gateway/src/core/scheduler/cluster_cron.py
rg -n "readiness_score_for_cluster" doge-complaints-gateway/src/core/cluster/engine.py
```
