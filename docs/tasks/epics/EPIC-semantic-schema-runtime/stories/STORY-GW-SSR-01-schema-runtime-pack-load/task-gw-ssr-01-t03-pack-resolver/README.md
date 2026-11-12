# task-gw-ssr-01-t03-pack-resolver

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061
- **Skill declared:** python-pro
- **Depends on:** T00 Done (layout named — do not invent pack paths)
- **Scaffolded:** 2026-08-28T13:11:39Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` T03; INDEX **D-SSR-4**

## Purpose
Resolver: packs root из config/env default `schema-packs/`; unknown schema / unsupported version → typed error (RUNTIME-005).

## Code Facts
- Packs root default `schema-packs/` — story T03 / D-SSR-4
- `src/core/schema/` **Not found** at P1 — create `resolver.py` at execute
- Intake **not** this story — do not call from [`contracts.py:413`](../../../../../../../src/core/intake/contracts.py)

## Acceptance / DoD
- [x] Traces story T03: resolve by `(schema_id, schema_version)`
- [x] Packs root from config/env; default `schema-packs/`
- [x] Unknown schema / unsupported version → typed error (RUNTIME-005)
- [x] Module `src/core/schema/resolver.py`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/resolver.py`
- Config/env hook for packs root (no hardcode-only path without config)

## Out of scope
- Hardcode path только без config hook
- JSON Schema validate (T04); invent HTTP paths
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
rg -n 'schema-packs|unsupported|unknown schema|resolver' doge-complaints-gateway/src/core/schema/resolver.py
```
