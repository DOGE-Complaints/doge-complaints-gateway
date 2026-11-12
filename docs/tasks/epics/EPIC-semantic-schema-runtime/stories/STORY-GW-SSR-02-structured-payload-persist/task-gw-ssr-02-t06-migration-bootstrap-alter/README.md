# task-gw-ssr-02-t06-migration-bootstrap-alter

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T06

## Purpose
`supabase/migrations/` ADD COLUMN nullable; **тот же** `ALTER … ADD COLUMN IF NOT EXISTS` in `000_full_init.sql`. Не schema-specific DDL.

## Code Facts
- Envelope column — [`000_full_init.sql:9`](../../../../../../../supabase/bootstrap/000_full_init.sql) `schema_version text not null`
- Init wave — [`20260423_1500_init_db_wave.sql:8`](../../../../../../../supabase/migrations/20260423_1500_init_db_wave.sql)
- Cross-layer test — [`tests/test_stories_schema_cross_layer_invariant.py`](../../../../../../../tests/test_stories_schema_cross_layer_invariant.py)
- `REQUIRED_READINESS_TABLES` already includes `stories` — [`db_supabase.py:29–43`](../../../../../../../src/core/infrastructure/db_supabase.py)

## Acceptance / DoD
- [x] Traces story T06: nullable ADD COLUMN for T00 map fields
- [x] Same ALTER IF NOT EXISTS in bootstrap `000_full_init.sql`
- [x] No schema-specific / node-specific domain columns; no `story_dimensions`
- [x] `_STORY_SELECT_FIELDS` names exist in bootstrap (cross-layer green)
- [x] BULLRUN phases complete

## Where to change
- New `doge-complaints-gateway/supabase/migrations/` (ADD COLUMN nullable)
- `doge-complaints-gateway/supabase/bootstrap/000_full_init.sql`

## Out of scope
- Node-specific columns; SELECT без bootstrap; `story_dimensions` table
- New table in `REQUIRED_READINESS_TABLES`
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
rg -n 'bound_schema_version|structured_payload|payload_hash' \
  doge-complaints-gateway/supabase/bootstrap/000_full_init.sql \
  doge-complaints-gateway/supabase/migrations/
```
