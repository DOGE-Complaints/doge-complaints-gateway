# task-gw-ssr-03-t03-runtime-validate-hook

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000063
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-08-28T14:05:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` T03

## Purpose
If binding present: `LocalSchemaRuntime.validate` **before** `save_story`. Map `SchemaRuntimeError` (RUNTIME-005) → `IntakeValidationError` / 4xx envelope (same class as other intake errors, not silent drop). Wire runtime in factory (`service_factory.py:75–84`) + intake service. `enforce_policy` без identity claims.

## Code Facts
- `LocalSchemaRuntime.validate` — [`runtime.py:35–38`](../../../../../../../src/core/schema/runtime.py); class docstring «Not wired into intake»
- RUNTIME-005 — [`errors.py:1–16`](../../../../../../../src/core/schema/errors.py) `SchemaRuntimeError`
- `StoryIntakeService` DI — [`services.py:94–101`](../../../../../../../src/core/application/services.py) — no SchemaRuntime field
- Factory — [`service_factory.py:75–84`](../../../../../../../src/core/infrastructure/service_factory.py)
- `dependencies.py` SchemaRuntime — **Not found**
- IntakeValidationError → 4xx — [`handlers.py:333`](../../../../../../../src/core/api/handlers.py)

## Acceptance / DoD
- [x] Traces story T03: validate before `save_story` when binding present
- [x] RUNTIME-005 → 4xx envelope, not silent drop
- [x] Factory wires runtime; no identity `policy_context`
- [x] Required `narrative` not weakened
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/services.py` intake
- `doge-complaints-gateway/src/core/infrastructure/service_factory.py`
- Optionally `doge-complaints-gateway/src/core/api/dependencies.py` only if needed for existing DI pattern — **no** new HTTP route

## Out of scope
- Identity `policy_context`; weaken required `narrative`; pack domain instead of title/description
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
rg -n "LocalSchemaRuntime|SchemaRuntimeError|schema_runtime" doge-complaints-gateway/src/core/application/services.py doge-complaints-gateway/src/core/infrastructure/service_factory.py
```
