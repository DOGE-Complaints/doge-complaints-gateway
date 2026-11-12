# task-gw-ssr-01-t06-unit-tests

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061
- **Skill declared:** python-pro
- **Depends on:** T00–T05
- **Scaffolded:** 2026-08-28T13:11:39Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` T06; Tests §29 Unit

## Purpose
Unit: resolve, validate pass/fail, two packs same runtime, no code exec from pack bytes. Civic parser tests **не** трогать (ещё нет wire).

## Code Facts
- Target glob — `tests/test_gw_ssr_01_*` (story T06)
- Civic parser tests exist; **do not** edit them this story
- Do not change `test_clustering_engine.py` — story T06 «Не делать»
- `ClusterLens` baseline — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] Traces story T06 / Tests §29: schema resolution, JSON Schema validation, canonicalization, field-policy as represented in pack
- [x] Unit: resolve; validate pass/fail; two packs same runtime; no code exec from pack bytes
- [x] Files `tests/test_gw_ssr_01_*`
- [x] Civic parser tests untouched; `test_clustering_engine.py` untouched
- [x] BULLRUN phases complete

## Where to change
- New `doge-complaints-gateway/tests/test_gw_ssr_01_*.py`

## Out of scope
- Менять `test_clustering_engine.py`
- Civic parser tests; HTTP filter tests; SSR-02 persist tests
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
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_01_*.py
rg -n 'class ClusterLens' -A 14 doge-complaints-gateway/src/core/cluster/types.py
```
