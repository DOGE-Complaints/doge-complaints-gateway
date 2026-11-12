# task-gw-ssr-02-t05-supabase-row-select

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T05

## Purpose
save row dict + from_row + `_STORY_SELECT_FIELDS`. Omit-probe if unmigrated host (как geo_admin).

## Code Facts
- `_STORY_SELECT_FIELDS` — [`db_supabase.py:66–74`](../../../../../../../src/core/infrastructure/db_supabase.py)
- from_row — [`db_supabase.py:154`](../../../../../../../src/core/infrastructure/db_supabase.py)
- save row — [`db_supabase.py:434–462`](../../../../../../../src/core/infrastructure/db_supabase.py)
- Omit-probe geo_admin — [`db_supabase.py:418`](../../../../../../../src/core/infrastructure/db_supabase.py)
- `required_columns_ready` — [`db_supabase.py:336`](../../../../../../../src/core/infrastructure/db_supabase.py) — **do not** add binding cols

## Acceptance / DoD
- [x] Traces story T05: save + from_row + `_STORY_SELECT_FIELDS` include binding fields
- [x] Omit-probe if unmigrated host (geo_admin pattern); civic SELECT not broken
- [x] Binding columns **not** in `required_columns_ready`
- [x] Geo-split untouched
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/infrastructure/db_supabase.py`

## Out of scope
- Класть поля в `required_columns_ready`; ломать geo-split
- Node-specific DDL (T06)
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
rg -n 'bound_schema_version|_STORY_SELECT_FIELDS|required_columns_ready' doge-complaints-gateway/src/core/infrastructure/db_supabase.py
```
