# task-gw-ssr-01-t04-jsonschema-validate

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061
- **Skill declared:** python-pro
- **Depends on:** T00 Done (manifest/schema files named); T01 (`jsonschema` dep)
- **Scaffolded:** 2026-08-28T13:11:39Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` T04; AC-004; SEC-001/002

## Purpose
JSON Schema validate `structured_payload`; no silent coerce; forbidden/missing/type errors. SEC-002: reject cyclic `$ref` / oversized payload (лимиты в коде, числа — константы модуля, не invent product threshold в REQ).

## Code Facts
- `jsonschema` not in deps at P1 — T01 must land first
- No `src/core/schema/validator.py` at P1
- SEC-001: pack YAML/JSON cannot execute arbitrary Python/JS/shell — story AC
- Do not use `eval` / import pack as Python — story T04 «Не делать»

## Acceptance / DoD
- [x] Traces story T04 / AC-004: validate `structured_payload`; no silent coerce; forbidden/missing/type errors
- [x] SEC-002: reject cyclic `$ref` / oversized payload; limits as module constants (not new REQ thresholds)
- [x] SEC-001: no code execution from pack bytes
- [x] Module `src/core/schema/validator.py`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/validator.py`

## Out of scope
- `eval` / import pack as Python
- Самописный validator «как JSON Schema» (use T01 `jsonschema`)
- Invent product threshold in REQ
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
rg -n 'jsonschema|structured_payload|eval\\(|exec\\(' doge-complaints-gateway/src/core/schema/validator.py
```
