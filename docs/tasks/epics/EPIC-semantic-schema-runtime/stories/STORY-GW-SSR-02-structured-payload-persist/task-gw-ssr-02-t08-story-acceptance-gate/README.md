# task-gw-ssr-02-t08-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** T00–T07 Done
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T08 + Target / AC

## Purpose
Story acceptance: AC-002/003; DATA-001/004; envelope `schema_version` civic rows unchanged; G2 rg invariants (`bound_schema_version` in lifecycle; `required_columns_ready` without binding).

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-02-….md`](../STORY-GW-SSR-02-structured-payload-persist.md) §Target / AC (verbatim)
- G2 commands — [`orchestrator-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) §6.2
- Gate **Date:** only after `--print-utc-now` post live pytest + `--verify` (P3) — not P1

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-02.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] All story Target / AC covered (AC-002/003; DATA-001/004; envelope civic operational)
- [x] G2 rg: binding fields in `advance_story_readiness` / replace; `required_columns_ready` without binding cols
- [x] Live verify commands + `--project gateway --verify` (+ tests) recorded
- **Date:** 2026-08-28T13:47:57Z
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`. SSR INDEX/dashboard recount at P3 Done only.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-02.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold

## Out of scope
- Implementing missing product gaps; P3 execution
- INDEX/runbook §4 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :106–109).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :336).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:29–43`).
  - Не invent HTTP filter / новый intake path.
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.

## Verification commands
```bash
# P3 only:
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_02_*.py
rg -n "bound_schema_version|structured_payload|payload_hash" src/core/application/services.py
rg -n "required_columns_ready" -A 30 src/core/infrastructure/db_supabase.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
