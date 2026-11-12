# task-gw-ssr-05-t01-pack-policy-mapper

## Meta
- **Story:** [STORY-GW-SSR-05](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000065
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-28T14:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` T01

## Purpose
Mapper loader keys (SSR-01 `ReadinessPolicy` / `ExactLensBlock`) → `PromotionGatePolicy` **for that call**: `require_actionable_canonical_type=False`, `min_stories` / `min_readiness_score` from pack file (example legal_process 3 / 40). Not civic 70/2 as Python SSOT.

## Code Facts
- Loader 3 knobs — [`contracts.py:30–36`](../../../../../../../src/core/schema/contracts.py) `ReadinessPolicy`; `ExactLensBlock.readiness_policy` [`:47`](../../../../../../../src/core/schema/contracts.py); resolver [`:40`](../../../../../../../src/core/schema/resolver.py)
- Civic knobs — [`gates.py:11–14`](../../../../../../../src/core/promotion/gates.py) `min_readiness_score=70`, `min_stories=2`, `require_actionable_canonical_type=True`
- Civic factory — [`service_factory.py:108–111`](../../../../../../../src/core/infrastructure/service_factory.py) `PromotionGatePolicy(`
- Example pack — [`legal_process/v1/pack.json`](../../../../../../../schema-packs/legal_process/v1/pack.json) `min_size=3`; `min_readiness_score=40`, `min_stories=3`, `require_actionable_canonical_type=false`
- Pack **policy mapper** → `PromotionGatePolicy` — **Not found** (P1 scaffold)

## Acceptance / DoD
- [x] Traces story T01: mapper pack file knobs → `PromotionGatePolicy` on **that call**
- [x] `require_actionable_canonical_type=False`; `min_stories` / `min_readiness_score` from pack, not civic 70/2
- [x] Civic default / factory unchanged
- [x] No 4th knob; CL-003 algorithm/scope/scale/missing_value_policy not new `reasons`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/` mapper next to `pack_engine.py`; consume existing `ReadinessPolicy`

## Out of scope
- Менять default/factory civic policy; invent 4-й knob
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
- SSR-05 extras: override on that call only; CLUSTERED only after successful pack promote; no `structured_payload` on `to_public_dict`; no QRY; no second cron.

## Verification commands
```bash
rg -n "class ReadinessPolicy|class PromotionGatePolicy" doge-complaints-gateway/src/core/schema/contracts.py doge-complaints-gateway/src/core/promotion/gates.py
rg -n "require_actionable_canonical_type: bool = True" doge-complaints-gateway/src/core/promotion/gates.py
rg -n "PromotionGatePolicy\(" doge-complaints-gateway/src/core/infrastructure/service_factory.py
```
