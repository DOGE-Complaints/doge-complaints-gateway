# task-gw-ssr-02-t02-payload-hash

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000062
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-08-28T13:38:52Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` T02; INDEX **D-SSR-5**

## Purpose
Canonical JSON of validated payload → `payload_hash`. Не принимать client hash as authority (считает runtime после validate).

## Code Facts
- Runtime lives under [`src/core/schema/`](../../../../../../../src/core/schema/) (SSR-01)
- D-SSR-5 — [`INDEX.md`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md): `payload_hash` делаем в SSR-02
- Intake does **not** write binding this story (SSR-03)

## Acceptance / DoD
- [x] Traces story T02 / DATA-004: deterministic hash of canonical validated payload
- [x] Helper under `src/core/schema/`
- [x] Client-supplied hash not treated as authority
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/` (helper)
- Callers in persist path this story; intake callers → SSR-03

## Out of scope
- Trust client-supplied hash; invent extra persist tokens
- `schema_binding` wire (SSR-03)
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
rg -n 'payload_hash' doge-complaints-gateway/src/core/schema/
```
