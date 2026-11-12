# task-gw-ssr-03-t08-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000063
- **Skill declared:** python-pro
- **Depends on:** T01–T07 Done
- **Scaffolded:** 2026-08-28T14:05:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` T08 + Target / AC

## Purpose
Story acceptance: AC-015 present bind+validate / absent civic; COMPAT-001 v2 envelope remains; FLOW-003 tokens persisted (no silent-ignore). G3 rg (`schema_binding` in intake+services; `asgi_app.py` без нового filter path; `GET /tallinn/issues` на месте).

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-03-….md`](../STORY-GW-SSR-03-optional-v2-semantic-wire.md) §Target / AC (verbatim)
- G3 commands — [`orchestrator-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) §6.3
- Gate **Date:** only after `--print-utc-now` post live pytest + `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done) — **not** `gateway-mvp-dashboard.md`

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-03.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] All story Target / AC covered (AC-015; COMPAT-001; FLOW-003; Tests §29)
- [x] G3 rg: `schema_binding` in `src/core/intake/contracts.py` and `src/core/application/services.py`; `asgi_app.py` without new filter/schema-metadata path; `GET /tallinn/issues` present
- [x] Live verify commands + `--project gateway --verify` (+ tests) recorded
- **Date:** 2026-08-28T14:13:05Z
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`. SSR INDEX/dashboard recount at P3 Done only.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-03.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold

## Out of scope
- Implementing missing product gaps; P3 execution
- INDEX/runbook §4 + §8 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :102–109).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:29–43`).
  - Не invent HTTP filter / новый intake path. OpenAPI only existing paths. `GET /tallinn/issues` must stay (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.

## Verification commands
```bash
# P3 only (G3):
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_03_*.py tests/test_story_intake_contract.py tests/test_gpt_signals_intake.py
rg -n "schema_binding" src/core/intake/contracts.py src/core/application/services.py
rg -n "def (GET|POST|PUT|PATCH|DELETE)|add_route|/tallinn/" src/core/api/asgi_app.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
