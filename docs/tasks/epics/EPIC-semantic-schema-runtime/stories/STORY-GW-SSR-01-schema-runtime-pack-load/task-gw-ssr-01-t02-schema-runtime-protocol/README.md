# task-gw-ssr-01-t02-schema-runtime-protocol

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-28T13:11:39Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` T02; INDEX **D-SSR-3** / **D-SSR-4**

## Purpose
`SchemaRuntime` Protocol + `LocalSchemaRuntime`: `resolve` / `validate` / `canonicalize` / `enforce_policy` (policy_context **без** identity claims). `build_index` / `project` — stub `NotImplemented` или no-op с явным later (SSR-06/07), не притворяться working IDX/PROC.

## Code Facts
- `src/core/schema/` **Not found** (Glob 0 at P1)
- `SchemaRuntime` in `src/` **Not found** (Grep 0 at P1)
- Intake parser **not** this story — [`contracts.py:413`](../../../../../../../src/core/intake/contracts.py) `parse_story_intake_request`
- D-SSR-3: no identity claims in `policy_context` — [`INDEX.md`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md)

## Acceptance / DoD
- [x] Traces story T02: Protocol + `LocalSchemaRuntime` with `resolve` / `validate` / `canonicalize` / `enforce_policy`
- [x] `enforce_policy` policy_context without identity claims (D-SSR-3)
- [x] `build_index` / `project` stub/`NotImplemented`/no-op with explicit later (SSR-06/07) — not working IDX/PROC
- [x] Code under `src/core/schema/` (D-SSR-4)
- [x] No call from intake
- [x] BULLRUN phases complete

## Where to change
- New `doge-complaints-gateway/src/core/schema/` (Protocol + `LocalSchemaRuntime`)

## Out of scope
- Вызов из intake
- Resolver path/config (T03); JSON Schema validate body (T04); persist (SSR-02)
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
rg -n 'class SchemaRuntime|class LocalSchemaRuntime|def enforce_policy|def build_index|def project' doge-complaints-gateway/src/core/schema/
rg -n 'parse_story_intake_request' doge-complaints-gateway/src/core/schema/ || true
```
