# task-gw-ssr-03-t02-intake-stash-dataclass-fields

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000063
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-28T14:05:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` T02

## Purpose
Field on `StoryIntakeRequest` (`:106`) **and** `StoryDraftStashRequest` (`:93`). Stash and submit share parsed binding. Update `intake_request_from_stash_and_submitter` (`:486–499`) so GPT stash does not drop binding before submit.

## Code Facts
- `StoryDraftStashRequest` — [`contracts.py:93–99`](../../../../../../../src/core/intake/contracts.py) — no binding field
- `StoryIntakeRequest` — [`contracts.py:106–113`](../../../../../../../src/core/intake/contracts.py) — no binding field
- Stash→submit bridge — [`contracts.py:486–499`](../../../../../../../src/core/intake/contracts.py) copies `gpt_signals` only
- Submit parse — [`contracts.py:413`](../../../../../../../src/core/intake/contracts.py); stash parse — [`:445`](../../../../../../../src/core/intake/contracts.py)

## Acceptance / DoD
- [x] Traces story T02: field on both request dataclasses
- [x] `intake_request_from_stash_and_submitter` copies binding
- [x] Stash and submit share the same envelope-body parse
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/intake/contracts.py` (`StoryIntakeRequest`, `StoryDraftStashRequest`, `intake_request_from_stash_and_submitter`)

## Out of scope
- Менять identity handlers; new envelope enum
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
- SSR-03 extras: sidecar only; `payload_hash` not on the wire.

## Verification commands
```bash
rg -n "class StoryIntakeRequest|class StoryDraftStashRequest|intake_request_from_stash_and_submitter|schema_binding" doge-complaints-gateway/src/core/intake/contracts.py
```
