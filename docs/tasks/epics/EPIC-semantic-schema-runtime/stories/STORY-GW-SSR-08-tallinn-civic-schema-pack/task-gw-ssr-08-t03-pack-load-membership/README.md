# task-gw-ssr-08-t03-pack-load-membership

## Meta
- **Story:** [STORY-GW-SSR-08](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md)
- **Type:** test
- **Status:** 🔵 Done
- **Package:** pkg-000066
- **Skill declared:** python-pro
- **Depends on:** T00–T02
- **Scaffolded:** 2026-08-29T17:47:38Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md` T03

## Purpose
Load pack; две stories с одинаковым payload path → один `cluster_id`; missing path → skip/policy.

## Code Facts
- Resolver — [`resolver.py:23–30`](../../../../../../../src/core/schema/resolver.py) `SCHEMA_PACKS_ROOT` / default
- Pack membership — [`pack_engine.py`](../../../../../../../src/core/schema/pack_engine.py) `SchemaPackClusterEngine`; `missing_value_policy` skip
- Orchestrator split — [`cluster_orchestrator.py:236–237`](../../../../../../../src/core/application/cluster_orchestrator.py) bound → pack branch
- G8 pytest — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.1 `tests/test_gw_ssr_08_*.py`

## Acceptance / DoD
- [x] Traces story T03: load + same payload path → one `cluster_id`; missing path → skip/policy
- [x] Exact membership for bound stories; `lens` = pack `lens_id`
- [x] Do not run bound story through civic engine
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_08_*`

## Out of scope
- Прогонять bound story через civic engine
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22). 10 members stay.
  - Не править `lens_dimension` под pack (`engine.py` :66–79). Pack **не** via civic `lens_dimension`.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / новый intake path / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать / не ставить в очередь SSR-06/07/12.
  - `build_index` / `project` — stub/no-op (`runtime.py` :62–72).
  - Не переименовывать `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0*`.
  - Civic path без binding **must stay**.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не новый Python engine; не прогонять bound story через civic engine (dual → SSR-10).
  - Pack cluster_id namespace `schema:…`; civic `_persist_memberships` / `_create_issue_for_cluster` as-is не для pack.

## Verification commands
```bash
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_08_*.py
```
