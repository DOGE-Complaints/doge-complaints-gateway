# task-gw-ssr-03-t01-optional-schema-binding-parse

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000063
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-28T14:05:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` T01

## Purpose
Optional `schema_binding` object in `_parse_story_envelope_body`. Unknown inner keys → error. Inner `schema_version` ≠ envelope `m2.story_intake_envelope.v2`. Allowed inner keys only: `schema_id`, `schema_version`, `profile_id`, `profile_version`, `structured_payload`. Pattern: `gpt_signals` `:397–401` (`if key in payload`). Absence of key = current 6-tuple civic path. Empty object: civic (story T05).

## Code Facts
- Envelope body 6-tuple — [`contracts.py:228–235`](../../../../../../../src/core/intake/contracts.py) → return [`:403–410`](../../../../../../../src/core/intake/contracts.py) — **no** `schema_binding`
- Optional sidecar `gpt_signals` — [`contracts.py:397–401`](../../../../../../../src/core/intake/contracts.py)
- Required envelope — [`contracts.py:19`](../../../../../../../src/core/intake/contracts.py) `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v2"`
- `schema_binding` in `src/` — **Not found** (P1 scaffold)

## Acceptance / DoD
- [x] Traces story T01: optional `schema_binding` object
- [x] Unknown inner keys → `IntakeValidationError`
- [x] Inner `schema_version` ≠ envelope id
- [x] No flat root `schema_id`; `payload_hash` not on the wire
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/intake/contracts.py` `_parse_story_envelope_body`

## Out of scope
- Плоские root `schema_id`; `payload_hash` на проводе; invent extra inner keys
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
- SSR-03 extras: sidecar only (like `gpt_signals`); no new envelope enum.

## Verification commands
```bash
rg -n "schema_binding" doge-complaints-gateway/src/core/intake/contracts.py
rg -n "_parse_story_envelope_body|gpt_signals" doge-complaints-gateway/src/core/intake/contracts.py
```
