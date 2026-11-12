# task-gw-ssr-01-t05-legacy-m2-compat-type

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061
- **Skill declared:** python-pro
- **Depends on:** T02 (runtime package exists)
- **Scaffolded:** 2026-08-28T13:11:39Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` T05; COMPAT-001

## Purpose
Тип/адаптер `LegacyM2StorySchema` (маркер civic envelope). Без удаления v2.

## Code Facts
- Envelope constant — [`contracts.py:19`](../../../../../../../src/core/intake/contracts.py) `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v2"`
- Story «Не делать»: Менять `INTAKE_SCHEMA_VERSION`
- COMPAT-001 conceptual name — story Target AC

## Acceptance / DoD
- [x] Traces story T05 / COMPAT-001: `LegacyM2StorySchema` named in code/docs
- [x] v2 envelope not deleted; `INTAKE_SCHEMA_VERSION` unchanged
- [x] Type lives under `src/core/schema/`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/` (compat type/adapter)
- Optional docs mention of the conceptual name (not REQ rewrite)

## Out of scope
- Менять `INTAKE_SCHEMA_VERSION`
- `schema_binding` parser (SSR-03); persist columns (SSR-02)
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
rg -n 'LegacyM2StorySchema' doge-complaints-gateway/src/core/schema/
rg -n 'INTAKE_SCHEMA_VERSION' doge-complaints-gateway/src/core/intake/contracts.py
```
