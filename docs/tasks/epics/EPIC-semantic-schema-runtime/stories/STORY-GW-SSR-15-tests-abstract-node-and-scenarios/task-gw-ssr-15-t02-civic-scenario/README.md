# task-gw-ssr-15-t02-civic-scenario

## Task: tests — civic unbound → GET `/node/issues` (T02)

## Meta
- **Story:** [STORY-GW-SSR-15](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000072
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-29T19:41:20Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md` T02 / scenario 1

## Purpose
Unbound civic → `GET /node/issues` (смысл текущего read API). Prefer extend existing offline civic list after T01 paths; add `tests/test_gw_ssr_15_*.py` only if no existing test states unbound → list on `/node/issues`.

## Code Facts
- Public GET list — [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py) `@app.get("/node/issues")` → `handle_issues_list`
- Civic list after T01 — [`test_req24_issues_read_api.py`](../../../../../../../tests/test_req24_issues_read_api.py) (after rename) / [`test_gw_public_01_public_issues_regression.py`](../../../../../../../tests/test_gw_public_01_public_issues_regression.py)
- Story scenario 1 — civic без binding → list `GET /node/issues`

## Acceptance / DoD
- [x] Сценарий 1 зелёный: unbound civic → `GET /node/issues`
- [x] Binding not required
- [x] BULLRUN phases complete

## Where to change
- Existing civic list tests after T01 **or** `doge-complaints-gateway/tests/test_gw_ssr_15_*.py` if missing

## Out of scope
- Binding required. New HTTP filter.
- INDEX/runbook §8 + fence hard bans:
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`.
  - Не alias 200. Не `live_integration` proof.
  - Не менять geo `tallinn` / pack id `tallinn_civic`.
  - Не переписывать T-wave G3 / §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не реализовывать SSR-06/07/12. Не reopen 01–05/08–11/13/14.
  - SPA repository unit tests — **not this story**.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" tests/test_gw_public_01_public_issues_regression.py tests/test_req24_issues_read_api.py
```
