# task-gw-ssr-08-t02-pack-readiness-policy

## Meta
- **Story:** [STORY-GW-SSR-08](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000066
- **Skill declared:** python-pro
- **Depends on:** T00, T01
- **Scaffolded:** 2026-08-29T17:47:38Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md` T02

## Purpose
`readiness_policy` 3 knobs в файле пака (числа **не** civic 70/2). Mapper SSR-05 `promotion_gate_policy_from_pack` **as-is**.

## Code Facts
- Mapper SSR-05 — [`pack_policy.py:9–19`](../../../../../../../src/core/schema/pack_policy.py) `promotion_gate_policy_from_pack` — **as-is**, do not rewrite
- Civic default — [`gates.py:11–14`](../../../../../../../src/core/promotion/gates.py) 70/2/`require_actionable_canonical_type=True`
- Civic factory — [`service_factory.py:108–111`](../../../../../../../src/core/infrastructure/service_factory.py)
- Example pack knobs — [`legal_process/v1/pack.json`](../../../../../../../schema-packs/legal_process/v1/pack.json) 40/3/false; [`mobility_observation/v1/pack.json`](../../../../../../../schema-packs/mobility_observation/v1/pack.json) 25/4/false
- Loader parse — [`resolver.py:38–43`](../../../../../../../src/core/schema/resolver.py) `_parse_readiness`

## Acceptance / DoD
- [x] Traces story T02: 3 knobs in pack file; mapper as-is
- [x] Pack promote knobs from file; civic factory default unchanged
- [x] Numbers **not** civic 70/2 as Python SSOT
- [x] BULLRUN phases complete

## Where to change
- `schema-packs/tallinn_civic/v1/pack.json` `readiness_policy` на каждом `exact_lenses[]`.

## Out of scope
- Менять factory civic `PromotionGatePolicy`; rewrite `pack_policy.py`; 4th knob
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
rg -n "require_actionable_canonical_type: bool = True" doge-complaints-gateway/src/core/promotion/gates.py
rg -n "PromotionGatePolicy\(" doge-complaints-gateway/src/core/infrastructure/service_factory.py
rg -n "def promotion_gate_policy_from_pack" doge-complaints-gateway/src/core/schema/pack_policy.py
```
