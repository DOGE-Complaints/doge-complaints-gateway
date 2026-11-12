# task-gw-ssr-08-t01-exact-lenses-civic-equivalents

## Meta
- **Story:** [STORY-GW-SSR-08](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000066
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-08-29T17:47:38Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md` T01

## Purpose
`exact_lenses` для civic-эквивалентов (включая composite как два `source_fields`). `lens_id` **строки** (civic lens *values* as data), не член `ClusterLens`.

## Code Facts
- Pack engine — [`pack_engine.py:103`](../../../../../../../src/core/schema/pack_engine.py) `payload = story.structured_payload`; `pack_cluster_id` [`:44–46`](../../../../../../../src/core/schema/pack_engine.py) join `\|`
- Civic `ClusterLens` 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- `lens_dimension` civic dict — [`engine.py:66–79`](../../../../../../../src/core/cluster/engine.py) — do not edit for pack
- Composite civic pair — [`engine.py:82–87`](../../../../../../../src/core/cluster/engine.py) `composite_primary_signal_pair`
- Etalon lens block — [`legal_process/v1/pack.json`](../../../../../../../schema-packs/legal_process/v1/pack.json) `lens_id` + `source_fields`

## Acceptance / DoD
- [x] Traces story T01: exact_lenses civic-equivalents including composite two `source_fields`
- [x] `lens_id` strings, not enum members; `cluster_memberships.lens` = pack `lens_id`
- [x] No `lens_dimension` dict edit; no civic `_persist_memberships`
- [x] BULLRUN phases complete

## Where to change
- тот же `schema-packs/tallinn_civic/v1/pack.json`. Engine `pack_engine.py` as-is.

## Out of scope
- `lens_dimension` dict; civic `_persist_memberships`; новый enum member
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
rg -n "class ClusterLens" -A 14 doge-complaints-gateway/src/core/cluster/types.py
rg -n "def lens_dimension" -A 14 doge-complaints-gateway/src/core/cluster/engine.py
rg -n "source_fields|lens_id|composite_primary" doge-complaints-gateway/schema-packs/README.md
```
