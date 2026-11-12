# task-gw-ssr-02-t00-parent-persist-field-map

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** docs / contract
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** SSR-01 Done
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T00; INDEX **D-SSR-5** persist map

## Purpose
Зафиксировать map parent→`StoryRecord`/SQL (таблица в стори). Semantic version = `bound_schema_version`. Envelope stays `schema_version`. No extra `envelope_version` column.

## Code Facts
- Envelope field — [`contracts.py:46`](../../../../../../../src/core/domain/contracts.py) `StoryRecord.schema_version`
- Persist map — pipeline story §Стыковка (parent token → SQL)
- `bound_schema_version` / `structured_payload` / `payload_hash` — **P3:** domain comments + SQL `bound_schema_version` (not a second `schema_version`)
- Hosted envelope column — [`20260423_1500_init_db_wave.sql:8`](../../../../../../../supabase/migrations/20260423_1500_init_db_wave.sql)

## Acceptance / DoD
- [x] Traces story T00: parent→`StoryRecord`/SQL map in this story (table)
- [x] Semantic persist named `bound_schema_version` (not a second `schema_version` column)
- [x] Envelope remains existing `schema_version`; no extra `envelope_version` column
- [x] Domain comments (P3) match the map
- [x] BULLRUN phases complete

## Where to change
- Pipeline story persist map (already in this folder)
- Domain comments on `StoryRecord` (P3, with T01)

## Out of scope
- Вторая колонка `schema_version`
- Domain fields / sqlite ALTER / hash helper (T01–T03)
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
rg -n 'bound_schema_version|envelope_version' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/STORY-GW-SSR-02-structured-payload-persist.md
```
