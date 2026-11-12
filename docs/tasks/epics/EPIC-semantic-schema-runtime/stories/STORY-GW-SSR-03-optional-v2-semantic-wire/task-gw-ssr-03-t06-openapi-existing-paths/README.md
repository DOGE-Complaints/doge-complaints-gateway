# task-gw-ssr-03-t06-openapi-existing-paths

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000063
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-08-28T14:05:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` T06; runbook §6.3

## Purpose
Optional object on **existing** intake/stash schemas (`StoryIntakeRequest`, `StoryDraftStashRequest`). Document inner tokens (`schema_id`, semantic `schema_version`, optional profiles, `structured_payload`). No `payload_hash` on the wire. No new GET filter / new HTTP path. Keep `GET /tallinn/issues`.

## Code Facts
- OpenAPI schemas — [`openapi.yaml:393–435`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) `StoryIntakeRequest` / `StoryDraftStashRequest` have `gpt_signals`, **no** `schema_binding`
- Existing HTTP paths — [`openapi.yaml:725+`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) `/story-drafts`, `/{draft_id}`, `/current`, `/{draft_id}/submit`
- Public `POST /intake/stories` removed — [`API_REFERENCE.md:135`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md)
- `GET /tallinn/issues` — [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py)

## Acceptance / DoD
- [x] Traces story T06: optional `schema_binding` on existing intake/stash schema
- [x] No extra OpenAPI names beyond `schema_binding` + parent token list
- [x] No new GET filter / new HTTP path; `GET /tallinn/issues` stays
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml`
- `doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md`

## Out of scope
- Новый GET filter / новый HTTP path; extra OpenAPI names beyond `schema_binding` + parent token list
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
rg -n "schema_binding" doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md
rg -n "def (GET|POST|PUT|PATCH|DELETE)|add_route|/tallinn/" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "GET /tallinn/issues" doge-complaints-gateway/src/core/api/asgi_app.py
```
