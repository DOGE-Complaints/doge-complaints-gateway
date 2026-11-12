# task-gw-ssr-02-t07-unit-tests

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** T00–T06
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T07; runbook §6.2 G2

## Purpose
Two payloads same table; round-trip sqlite+memory; civic save без binding (все None) зелёный; lifecycle advance **сохраняет** binding. Round-trip via `save_story` (intake ещё не пишет binding).

## Code Facts
- G2 bundle — runbook §6.2: `tests/test_gw_ssr_02_*` + `test_stories_schema_cross_layer_invariant.py` + civic intake persist tests
- In-memory stores whole dataclass — [`repositories.py:56–70`](../../../../../../../src/core/infrastructure/repositories.py)

## Acceptance / DoD
- [x] Traces story T07: two payloads same table; sqlite+memory round-trip
- [x] Civic save without binding (all None) green
- [x] Lifecycle advance preserves binding
- [x] Files `tests/test_gw_ssr_02_*`
- [x] Cross-layer invariant + civic persist tests still green
- [x] BULLRUN phases complete

## Where to change
- New `doge-complaints-gateway/tests/test_gw_ssr_02_*.py`

## Out of scope
- Live hosted как единственный proof; менять `test_clustering_engine.py`
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
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_02_*.py tests/test_stories_schema_cross_layer_invariant.py \
  tests/test_story_intake_contract.py tests/test_story_intake_field_persistence.py
```
