# task-gw-ssr-02-t01-story-record-optional-fields

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T01

## Purpose
Optional fields на `StoryRecord` с default `None`: `schema_id`, `bound_schema_version`, `profile_id`, `profile_version`, `structured_payload`, `payload_hash`.

## Code Facts
- Dataclass — [`contracts.py:43–75`](../../../../../../../src/core/domain/contracts.py) `StoryRecord` — envelope `schema_version` + optional binding fields (P3)

## Acceptance / DoD
- [x] Traces story T01: optional fields default `None`
- [x] Names match T00 map (`bound_schema_version` not second `schema_version`)
- [x] No domain columns (`institution_type`, …)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/domain/contracts.py` (`StoryRecord`)

## Out of scope
- Domain columns (`institution_type`, …)
- sqlite/supabase persist (T03/T05); hash algorithm (T02)
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
rg -n 'bound_schema_version|structured_payload|payload_hash|schema_id' doge-complaints-gateway/src/core/domain/contracts.py
```
