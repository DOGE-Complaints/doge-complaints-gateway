# task-gw-ssr-08-t00-tallinn-civic-pack-catalog

## Meta
- **Story:** [STORY-GW-SSR-08](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000066
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-29T17:47:38Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md` T00

## Purpose
Каталог `schema-packs/tallinn_civic/v1/`: `pack.json` + `payload.schema.json` по loader keys; map таблицы `$storyFile` → schema properties (`signals.civic_domain` … `geo.district`).

## Code Facts
- Loader keys — [`schema-packs/README.md`](../../../../../../../schema-packs/README.md) `pack.json` + `payload.schema.json`; `SCHEMA_PACKS_ROOT` or default
- Resolver default root — [`resolver.py:23–30`](../../../../../../../src/core/schema/resolver.py) `default_packs_root`
- Example packs — `schema-packs/legal_process/v1`, `mobility_observation/v1`
- `tallinn_civic` on disk — **As-of-Done** [`schema-packs/tallinn_civic/v1/`](../../../../../../../schema-packs/tallinn_civic/v1/pack.json)
- Loader 3 knobs — [`contracts.py:30–36`](../../../../../../../src/core/schema/contracts.py) `ReadinessPolicy`

## Acceptance / DoD
- [x] Traces story T00: catalog `tallinn_civic/v1/` with loader keys
- [x] JSON Schema covers map SignalDimension/label keys → dotted paths
- [x] No new YAML dialect; no `ClusterLens` edit
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/tallinn_civic/v1/` only. Consume existing loader — do not invent YAML keys.

## Out of scope
- Новый YAML-диалект; править `ClusterLens`; копировать enum в Python
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
test -f doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json
rg -n "schema_id|payload_schema|field_policy|exact_lenses" doge-complaints-gateway/schema-packs/README.md
rg -n "class ClusterLens" -A 14 doge-complaints-gateway/src/core/cluster/types.py
```
