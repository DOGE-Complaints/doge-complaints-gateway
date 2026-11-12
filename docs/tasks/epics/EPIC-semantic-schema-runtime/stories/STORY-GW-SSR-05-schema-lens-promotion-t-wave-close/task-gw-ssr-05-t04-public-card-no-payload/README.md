# task-gw-ssr-05-t04-public-card-no-payload

## Meta
- **Story:** [STORY-GW-SSR-05](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000065
- **Skill declared:** python-pro
- **Depends on:** T03
- **Scaffolded:** 2026-08-28T14:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` T04

## Purpose
Assert `to_public_dict` without `structured_payload`; type/title from civic narrative fields. Pack Issue projection = civic narrative (title/description required on intake).

## Code Facts
- Public card — [`dto.py:26–36`](../../../../../../../src/core/projection/dto.py) `DOGEIssue.to_public_dict` — **нет** `structured_payload`
- `GET /tallinn/issues` — [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py)

## Acceptance / DoD
- [x] Traces story T04: `to_public_dict` без `structured_payload`
- [x] type/title from civic narrative; no invented Issue field names
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/projection/dto.py` + test (assert unchanged shape; do not add fields)

## Out of scope
- Новые Issue field names; add payload to public dict
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
- SSR-05 extras: SPA-003; no QRY; civic tests stay green.

## Verification commands
```bash
rg -n "structured_payload" doge-complaints-gateway/src/core/projection/dto.py
rg -n "def to_public_dict" -A 16 doge-complaints-gateway/src/core/projection/dto.py
```
