# task-gw-ssr-05-t02-optional-gate-policy-command

## Meta
- **Story:** [STORY-GW-SSR-05](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000065
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-28T14:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` T02

## Purpose
Optional `gate_policy` on `IssueCreateCommand`; `submit_for_review(..., policy=…)`. `None` = `self.gate_policy`. Civic callers omit the field.

## Code Facts
- `IssueCreateCommand` — [`issue_create.py:28–34`](../../../../../../../src/core/application/issue_create.py) — **no** `gate_policy` field
- `_create_issue` always civic submit — [`:226–229`](../../../../../../../src/core/application/issue_create.py)
- `submit_for_review` always `self.gate_policy` — [`service.py:75–86`](../../../../../../../src/core/promotion/service.py)
- Civic factory singleton — [`service_factory.py:108–111`](../../../../../../../src/core/infrastructure/service_factory.py)

## Acceptance / DoD
- [x] Traces story T02: optional `gate_policy` on command; None = civic
- [x] `submit_for_review` accepts per-call policy without flipping factory
- [x] Civic `_create_issue` path still works when field omitted
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/issue_create.py`
- `doge-complaints-gateway/src/core/promotion/service.py`

## Out of scope
- Ломать civic `_create_issue` path; flip factory singleton
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
- SSR-05 extras: 3 knobs only; CLUSTERED only after successful pack promote; no QRY; no second cron.

## Verification commands
```bash
rg -n "class IssueCreateCommand" -A 8 doge-complaints-gateway/src/core/application/issue_create.py
rg -n "def submit_for_review" -A 14 doge-complaints-gateway/src/core/promotion/service.py
```
