# task-gw-ssr-05-t05-negative-ac-018-no-qry

## Meta
- **Story:** [STORY-GW-SSR-05](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000065
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-28T14:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` T05

## Purpose
No generic filter HTTP; processor delivery not required to close T-wave. Grep `asgi_app.py` — no new filter route; `build_index` remains no-op (`runtime.py:62–66`). `GET /tallinn/issues` stays `:462`.

## Code Facts
- `GET /tallinn/issues` — [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py)
- `build_index` / `project` stub — [`runtime.py:62–72`](../../../../../../../src/core/schema/runtime.py) `NotImplementedError`

## Acceptance / DoD
- [x] Traces story T05 / AC-018: no generic filter HTTP
- [x] Processor delivery not required; `build_index` stays no-op
- [x] `GET /tallinn/issues` remains
- [x] BULLRUN phases complete

## Where to change
- Evidence: `asgi_app.py` routes + tests/rg. Do **not** add filter path.

## Out of scope
- Invent QRY / `story_dimensions`; implement SSR-06/07
- INDEX/runbook §4 + §8 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :108–111).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / новый intake path. OpenAPI only existing paths. `GET /tallinn/issues` must stay (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`.
- SSR-05 extras: T-wave close without QRY; no second cron.

## Verification commands
```bash
rg -n "story_dimensions|/schema-filter|generic.filter" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "GET /tallinn/issues|/tallinn/issues" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "def build_index|NotImplementedError" doge-complaints-gateway/src/core/schema/runtime.py
```
