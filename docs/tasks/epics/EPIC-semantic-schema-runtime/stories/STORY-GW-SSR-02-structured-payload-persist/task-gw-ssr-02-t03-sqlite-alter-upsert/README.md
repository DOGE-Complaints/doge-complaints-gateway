# task-gw-ssr-02-t03-sqlite-alter-upsert

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T03; runbook §6.2

## Purpose
ALTER in `_ensure_sqlite_schema_migrations`; `_STORY_SELECT_COLUMNS`; `_story_record_from_sqlite_row`; INSERT **и** `ON CONFLICT DO UPDATE SET` for each new field.

## Code Facts
- ALTER pattern — [`db_sqlite.py:302–314`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- SELECT list — [`db_sqlite.py:72`](../../../../../../../src/core/infrastructure/db_sqlite.py) `_STORY_SELECT_COLUMNS`
- INSERT — [`db_sqlite.py:537–548`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- ON CONFLICT — [`db_sqlite.py:549`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- `CREATE TABLE stories` — [`db_sqlite.py:177`](../../../../../../../src/core/infrastructure/db_sqlite.py) — **do not rewrite**

## Acceptance / DoD
- [x] Traces story T03: ALTER + SELECT + INSERT **and** ON CONFLICT SET for each new field
- [x] Existing DBs pick up columns via `_ensure_sqlite_schema_migrations` (not CREATE TABLE rewrite)
- [x] No new table in `REQUIRED_READINESS_TABLES`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/infrastructure/db_sqlite.py`

## Out of scope
- Новая таблица в REQUIRED; только INSERT без UPDATE SET; rewrite `CREATE TABLE stories`
- `required_columns_ready` (T05 ban)
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
rg -n 'bound_schema_version|structured_payload|payload_hash' doge-complaints-gateway/src/core/infrastructure/db_sqlite.py
rg -n 'CREATE TABLE IF NOT EXISTS stories' doge-complaints-gateway/src/core/infrastructure/db_sqlite.py
```
