# task-gw-ssr-02-t04-lifecycle-copy-replace

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T04; INDEX silent-wipe seam

## Purpose
`StoryRecord(` intake create defaults None; **lifecycle copy** `services.py:461` — all new fields. Prefer `dataclasses.replace(current, lifecycle_status=…, updated_at=…)`.

## Code Facts
- Intake create — [`services.py:236–238`](../../../../../../../src/core/application/services.py) `schema_version=request.schema_version`
- Lifecycle reconstruct by name — [`services.py:461`](../../../../../../../src/core/application/services.py) — **P3:** `dataclasses.replace`
- Status-only UPDATE — [`db_sqlite.py:670`](../../../../../../../src/core/infrastructure/db_sqlite.py) — not this reconstruct

## Acceptance / DoD
- [x] Traces story T04: intake create new fields default None
- [x] `advance_story_readiness` copies `schema_id`, `bound_schema_version`, `profile_*`, `structured_payload`, `payload_hash`
- [x] Prefer `dataclasses.replace`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/services.py`

## Out of scope
- Забыть copy (READY_FOR_PROFILE wipe)
- `schema_binding` parser (SSR-03)
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
rg -n 'bound_schema_version|structured_payload|payload_hash' doge-complaints-gateway/src/core/application/services.py
rg -n 'advance_story_readiness|dataclasses.replace|StoryRecord\(' doge-complaints-gateway/src/core/application/services.py
```
