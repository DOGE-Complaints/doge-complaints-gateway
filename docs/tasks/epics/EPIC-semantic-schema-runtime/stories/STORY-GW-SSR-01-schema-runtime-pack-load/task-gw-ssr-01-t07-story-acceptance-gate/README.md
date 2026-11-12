# task-gw-ssr-01-t07-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061
- **Skill declared:** python-pro
- **Depends on:** T00–T06 Done
- **Scaffolded:** 2026-08-28T13:11:39Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` T07 + Target / AC

## Purpose
Story acceptance: packs load; AC-004; SEC-001; `ClusterLens` enum **не** изменён (`rg ClusterLens src/core/cluster/types.py`).

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-01-….md`](../STORY-GW-SSR-01-schema-runtime-pack-load.md) §Target / AC (verbatim)
- `ClusterLens` members — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Gate **Date:** only after `--print-utc-now` post live pytest + `--verify` (P3) — not P1

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-01.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] All story Target / AC covered (pack load; AC-004; SEC-001/002; LegacyM2StorySchema; D-SSR-4; §29 tests)
- [x] `ClusterLens` enum unchanged (`rg ClusterLens src/core/cluster/types.py`)
- [x] Live verify commands + `--project gateway --verify` (+ tests) recorded
- **Date:** 2026-08-28T13:18:56Z (P3 live gate PASS)
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`. SSR INDEX/dashboard recount at P3 Done only.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-01.md`
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
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_01_*.py
rg -n 'class ClusterLens' -A 14 doge-complaints-gateway/src/core/cluster/types.py
```
