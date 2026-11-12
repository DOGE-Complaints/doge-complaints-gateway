# task-gw-ssr-03-t05-absent-binding-civic-path

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000063
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-28T14:05:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` T05

## Purpose
No key / empty object: civic save as today; regression intake tests stay green (`test_story_intake_contract.py`, `test_gpt_signals_intake.py`). COMPAT-001: keep `m2.story_intake_envelope.v2`.

## Code Facts
- Civic narrative required — [`contracts.py:248–276`](../../../../../../../src/core/intake/contracts.py); `canonical_type` optional [`:294–298`](../../../../../../../src/core/intake/contracts.py)
- Required envelope — [`contracts.py:19`](../../../../../../../src/core/intake/contracts.py) `m2.story_intake_envelope.v2`
- Regression tests — [`tests/test_story_intake_contract.py`](../../../../../../../tests/test_story_intake_contract.py), [`tests/test_gpt_signals_intake.py`](../../../../../../../tests/test_gpt_signals_intake.py)
- Empty-object semantics live in T01 parser (`if key in payload` like `gpt_signals`)

## Acceptance / DoD
- [x] Traces story T05: no key / empty object → civic save
- [x] `tests/test_story_intake_contract.py` and `tests/test_gpt_signals_intake.py` green
- [x] `m2.story_intake_envelope.v2` not removed
- [x] BULLRUN phases complete

## Where to change
- Tests (this task); parser empty-object helper only if T01 needs it
- Product code only if T01 empty-object needs a helper

## Out of scope
- Менять civic narrative required; remove v2 envelope
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
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_story_intake_contract.py tests/test_gpt_signals_intake.py
rg -n "m2.story_intake_envelope.v2" src/core/intake/contracts.py
```
