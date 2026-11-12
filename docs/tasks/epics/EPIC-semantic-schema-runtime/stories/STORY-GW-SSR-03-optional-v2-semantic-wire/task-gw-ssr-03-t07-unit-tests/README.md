# task-gw-ssr-03-t07-unit-tests

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000063
- **Skill declared:** python-pro
- **Depends on:** T01–T06
- **Scaffolded:** 2026-08-28T14:05:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` T07; runbook §6.3 G3

## Purpose
present→persist; absent→legacy; invalid payload rejected (4xx, not silent drop); stash round-trip. Civic suite green. Tests §29: optional parse vs ignore-absent.

## Code Facts
- G3 bundle — runbook §6.3: `tests/test_gw_ssr_03_*.py` + `tests/test_story_intake_contract.py` + `tests/test_gpt_signals_intake.py`
- Civic intake tests — [`tests/test_story_intake_contract.py`](../../../../../../../tests/test_story_intake_contract.py)
- `gpt_signals` sidecar tests — [`tests/test_gpt_signals_intake.py`](../../../../../../../tests/test_gpt_signals_intake.py)

## Acceptance / DoD
- [x] Traces story T07: present→persist; absent→legacy; invalid payload rejected; stash round-trip
- [x] Files `tests/test_gw_ssr_03_*`
- [x] Civic suite (`test_story_intake_contract.py`, `test_gpt_signals_intake.py`) green
- [x] BULLRUN phases complete

## Where to change
- New `doge-complaints-gateway/tests/test_gw_ssr_03_*.py`

## Out of scope
- Live hosted as only proof; invent new routes in tests as product
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
  tests/test_gw_ssr_03_*.py tests/test_story_intake_contract.py tests/test_gpt_signals_intake.py
```
