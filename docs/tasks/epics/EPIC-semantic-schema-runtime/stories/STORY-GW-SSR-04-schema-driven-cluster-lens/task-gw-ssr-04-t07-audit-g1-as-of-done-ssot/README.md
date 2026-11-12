# task-gw-ssr-04-t07-audit-g1-as-of-done-ssot

## Meta
- **Story:** [STORY-GW-SSR-04](../STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000064 (parent product Done); wave `run_mode=gw_ssr_04_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-04
- **Depends on:** T01–T06 Done
- **Audit ref:** [`audit-gw-ssr-04-schema-driven-cluster-lens-2026-08-28.md`](../../../../../../analysis/audit-gw-ssr-04-schema-driven-cluster-lens-2026-08-28.md) **G1**
- **Scaffolded:** 2026-08-28T14:42:37Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-04_gap_20260828T144143Z.plan.md` G1 TASKED follow_up=none

## Purpose
As-of-Done vs Historical split для persistent SSOT: backlog + pipeline SSR-04 §Verified / §Стыковка still present-tense pre-P3 (orchestrator pool «все READY_FOR_PROFILE»; imperative «новый `SchemaPackClusterEngine`»; civic `_persist_memberships` cite `:365–381`). Без runtime pack/civic. INDEX civic orchestrator + membership-vs-Issue seams already As-of-Done — do not regress.

## Code Facts
- Pack engine — [`pack_engine.py`](../../../../../../../src/core/schema/pack_engine.py) `SchemaPackClusterEngine` / `pack_cluster_id` / `is_schema_bound`
- Civic pool filter — [`cluster_orchestrator.py:86–87`](../../../../../../../src/core/application/cluster_orchestrator.py) `_civic_ready`
- Pack branch — [`:89–145`](../../../../../../../src/core/application/cluster_orchestrator.py) `_process_pack_bound_story`; `process_story` pack returns None [`:143–145`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic persist after Issue — [`:425–436`](../../../../../../../src/core/application/cluster_orchestrator.py); `_persist_memberships` [`:452–468`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Factory — [`service_factory.py:158`](../../../../../../../src/core/infrastructure/service_factory.py) `schema_pack_engine=SchemaPackClusterEngine()`
- Stale backlog §Verified — split applied (As-of-Done vs Historical) in [`STORY-GW-SSR-04`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- Stale backlog §Стыковка — As-of-Done cites `:422–436` / `:452–468`; Historical keeps `:365–381`
- Stale pipeline copy — split applied (same) in [`pipeline`](../STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- INDEX civic orchestrator + membership-vs-Issue already As-of-Done — [`INDEX.md:107,114`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md); do not rewrite as Historical-only
- Product Status 🔵 Done; gate PASS 2026-08-28T14:36:12Z

## Acceptance / DoD
- [x] Backlog SSR-04 §Verified: Current (`_civic_ready` / `_process_pack_bound_story`; pack membership without CLUSTERED) vs Historical (pre-P3 «все READY_FOR_PROFILE» / no pack branch)
- [x] Backlog SSR-04 §Стыковка: As-of-Done (engine exists; persist cite `:425–436` / `:452–468`) vs Historical (imperative «новый engine»; cite `:365–381`)
- [x] Pipeline SSR-04 §Verified / §Стыковка: same split (keep in sync with backlog)
- [x] INDEX civic orchestrator + membership-vs-Issue As-of-Done rows not reverted
- [x] No `src/` / civic enum / cron / pack runtime edits
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-04-t07.md` signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md` (§Verified current state + §Стыковка)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-04-schema-driven-cluster-lens/STORY-GW-SSR-04-schema-driven-cluster-lens.md` (§Verified current state + §Стыковка)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime pack engine / orchestrator / cron / CLUSTERED / Issue create
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
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`.
- SSR-04 extras: no second cron; no `CLUSTERED`; no pack via civic `lens_dimension`; no SSR-05.

## Verification commands
```bash
rg -n 'все READY_FOR_PROFILE|новый SchemaPackClusterEngine|:365–381' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-04-schema-driven-cluster-lens/STORY-GW-SSR-04-schema-driven-cluster-lens.md
rg -n '_civic_ready|_process_pack_bound_story' \
  doge-complaints-gateway/src/core/application/cluster_orchestrator.py
```
