# task-gw-ssr-05-t07-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-SSR-05](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000065
- **Skill declared:** python-pro
- **Depends on:** T01–T06 Done
- **Scaffolded:** 2026-08-28T14:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` T07 + Target / AC

## Purpose
Story acceptance + Product T-wave close. AC-014/018. SSR-06/07 not in DoD. G5: pack promote without civic types; civic promotion green; default knob True; `dto.py` without `structured_payload`; no filter HTTP; **full offline pytest** required. After PASS: wave closed; dashboard active 5/5; INDEX Status. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка».

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-05-….md`](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md) §Target / AC (verbatim)
- G5 commands — [`orchestrator-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) §6.5
- Gate **Date:** only after `--print-utc-now` post live pytest + `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done) — **not** `gateway-mvp-dashboard.md`

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-05.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-05-t07.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered (AC-014; AC-018; CL-006; SPA-003)
- [x] G5 rg: default knob True; no `structured_payload` in `dto.py`; no filter HTTP; ClusterLens baseline
- [x] Live verify commands + `--project gateway --verify` (+ G5 pytest + full offline pytest) recorded
- **Date:** not in P1
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`. SSR INDEX/dashboard recount at P3 Done only (active 5/5). Do not start SSR-06/07.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-05.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold

## Out of scope
- Implementing missing product gaps; P3 execution
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
- SSR-05 extras: no second cron; CLUSTERED only after pack promote; 3 knobs from pack file.

## Verification commands
```bash
# P3 only (G5):
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_05_*.py \
  tests/test_promotion_canonical_type_gate.py \
  tests/test_issue_promotion_service.py \
  tests/test_clustering_engine.py \
  tests/test_gw_tax_02_cluster_axis_expansion.py
.venv/bin/python -m pytest -q -m "not live_integration"
rg -n "require_actionable_canonical_type: bool = True" src/core/promotion/gates.py
rg -n "structured_payload" src/core/projection/dto.py
rg -n "story_dimensions|/schema-filter|generic.filter" src/core/api/asgi_app.py
```
