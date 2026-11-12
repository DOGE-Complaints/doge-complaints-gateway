# task-gw-ssr-05-t06-civic-promotion-regression

## Meta
- **Story:** [STORY-GW-SSR-05](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Type:** test
- **Status:** 🔵 Done
- **Package:** pkg-000065
- **Skill declared:** python-pro
- **Depends on:** T01–T05
- **Scaffolded:** 2026-08-28T14:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` T06

## Purpose
Existing clustering/promotion tests green (AC-008 / §29 Compatibility). G5 civic slice plus `tests/test_gw_ssr_05_*`. Pack promote without civic types in story tests; civic `require_actionable` tests stay green.

## Code Facts
- Civic default knob — [`gates.py:14`](../../../../../../../src/core/promotion/gates.py) `require_actionable_canonical_type: bool = True`
- Civic factory — [`service_factory.py:108–111`](../../../../../../../src/core/infrastructure/service_factory.py)
- G5 civic files — `tests/test_promotion_canonical_type_gate.py`, `tests/test_issue_promotion_service.py`, `tests/test_clustering_engine.py`, `tests/test_gw_tax_02_cluster_axis_expansion.py`

## Acceptance / DoD
- [x] Traces story T06: civic clustering/promotion tests green
- [x] `tests/test_gw_ssr_05_*` exist; pack promote without civic type tokens
- [x] Default `require_actionable_canonical_type=True` still in `gates.py`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_05_*`; keep civic files unmodified-green

## Out of scope
- Weaken civic `require_actionable` tests; change default knob
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
- SSR-05 extras: no QRY; no second cron; CLUSTERED only after pack promote.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_05_*.py \
  tests/test_promotion_canonical_type_gate.py \
  tests/test_issue_promotion_service.py \
  tests/test_clustering_engine.py \
  tests/test_gw_tax_02_cluster_axis_expansion.py
rg -n "require_actionable_canonical_type: bool = True" src/core/promotion/gates.py
```
