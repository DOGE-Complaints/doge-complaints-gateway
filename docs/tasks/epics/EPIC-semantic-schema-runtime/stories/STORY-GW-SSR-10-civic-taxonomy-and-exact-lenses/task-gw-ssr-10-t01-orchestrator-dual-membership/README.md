# task-gw-ssr-10-t01-orchestrator-dual-membership

## Task: implement — dual civic + pack exact on one story

## Meta
- **Story:** [STORY-GW-SSR-10](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000068
- **Skill declared:** python-pro
- **Depends on:** T00 (R1 flag)
- **Scaffolded:** 2026-08-29T18:25:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md` T01

## Purpose
Если pack говорит dual: civic memberships из `story_labels` / `infer_signals_from_canonical` **и** pack exact-lenses с payload на той же story. Bound без dual-ключа остаётся `_process_pack_bound_story` only. Civic без binding не менять. `ClusterLens` enum не расширять. G10: dual fixture civic lens value **и** pack `lens_id` на одном `story_id`.

## Code Facts
- Fork bound → pack-only — [`cluster_orchestrator.py:236–237`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic skip bound — [`cluster_orchestrator.py:87–88`](../../../../../../../src/core/application/cluster_orchestrator.py) `_civic_ready`
- Pack reads payload only — [`pack_engine.py:103–105`](../../../../../../../src/core/schema/pack_engine.py)
- Membership PK — [`db_sqlite.py:416`](../../../../../../../src/core/infrastructure/db_sqlite.py) `PRIMARY KEY (story_id, lens)`
- `ClusterLens` 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [ ] Dual: membership и civic-линз (enum value) и pack `lens_id` на одном `story_id`
- [ ] Pack without dual key: still `_process_pack_bound_story` only (T-wave)
- [ ] Civic stories без binding не менять
- [ ] `ClusterLens` не расширять
- [ ] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/cluster_orchestrator.py` (`:236–237`, `:87–88`)
- Civic engine as-is; pack_engine still payload-only for exact

## Out of scope
- Всегда civic для любого binding; расширять enum; pack via civic `lens_dimension` as default for all packs
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79) как default для всех packs.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/11/12/13. Не reopen 01–05/08/09.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "is_schema_bound|_civic_ready|_process_pack_bound_story" \
  doge-complaints-gateway/src/core/application/cluster_orchestrator.py
rg -n "class ClusterLens" -A 14 doge-complaints-gateway/src/core/cluster/types.py
```
