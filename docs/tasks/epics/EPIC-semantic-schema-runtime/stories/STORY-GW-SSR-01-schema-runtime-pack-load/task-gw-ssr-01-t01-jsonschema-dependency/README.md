# task-gw-ssr-01-t01-jsonschema-dependency

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-28T13:11:39Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` T01

## Purpose
Добавить `jsonschema` в `pyproject.toml` + `requirements.txt`.

## Code Facts
- `jsonschema` **Not found** — Grep `doge-complaints-gateway/pyproject.toml` (P1 scaffold)
- Deps block cite — [`pyproject.toml:11–16`](../../../../../../../pyproject.toml) (story Verified current state)
- INDEX seam: JSON Schema lib absent — [`INDEX.md`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md)

## Acceptance / DoD
- [x] Traces story T01: `jsonschema` declared in `pyproject.toml` and `requirements.txt`
- [x] `python3 -c "import jsonschema"` works after install (P3)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/pyproject.toml`
- `doge-complaints-gateway/requirements.txt`

## Out of scope
- Самописный validator «как JSON Schema»
- Validator implementation (T04); pack files (T00)
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
rg -n 'jsonschema' doge-complaints-gateway/pyproject.toml doge-complaints-gateway/requirements.txt
cd doge-complaints-gateway && python3 -c "import jsonschema"
```
