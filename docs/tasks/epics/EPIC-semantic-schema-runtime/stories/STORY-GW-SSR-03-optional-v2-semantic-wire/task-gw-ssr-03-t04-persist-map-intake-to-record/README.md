# task-gw-ssr-03-t04-persist-map-intake-to-record

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000063
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-08-28T14:05:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` T04; INDEX D-SSR-1 / D-SSR-5

## Purpose
Root envelope → `StoryRecord.schema_version`. Inner → `schema_id` / `bound_schema_version` / `profile_id` / `profile_version` / `structured_payload` + **server** `payload_hash` via `authoritative_payload_hash`. Do not persist client hash. FLOW-003: silently ignoring a present block is non-compliant.

## Code Facts
- Intake create — [`services.py:236–238`](../../../../../../../src/core/application/services.py) `schema_version=request.schema_version` only; binding omitted → defaults None
- Persist targets (SSR-02 Done) — [`domain/contracts.py:68–74`](../../../../../../../src/core/domain/contracts.py)
- Hash helper — [`payload.py:23–27`](../../../../../../../src/core/schema/payload.py) `authoritative_payload_hash`
- Lifecycle keep binding — [`services.py:461`](../../../../../../../src/core/application/services.py) `replace(` — do not regress

## Acceptance / DoD
- [x] Traces story T04: envelope → `StoryRecord.schema_version`; inner → SSR-02 fields + hash
- [x] Client `payload_hash` not used as authority
- [x] No second SQL/Python column named `schema_version`
- [x] Present binding is persisted (not silent-drop)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/services.py` `StoryRecord(` at intake create (`:236`)

## Out of scope
- Client `payload_hash`; вторая колонка `schema_version`; silent-ignore present block
- INDEX/runbook §4 + §8 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :102–109).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:29–43`).
  - Не invent HTTP filter / новый intake path. OpenAPI only existing paths. `GET /tallinn/issues` must stay (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.

## Verification commands
```bash
rg -n "bound_schema_version|structured_payload|authoritative_payload_hash|schema_id" doge-complaints-gateway/src/core/application/services.py
```
