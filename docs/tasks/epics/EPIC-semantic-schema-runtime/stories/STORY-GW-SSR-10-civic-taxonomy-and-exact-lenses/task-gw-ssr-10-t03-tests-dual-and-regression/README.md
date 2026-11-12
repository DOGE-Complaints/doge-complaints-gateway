# task-gw-ssr-10-t03-tests-dual-and-regression

## Task: tests — dual fixture + civic / exact-only green

## Meta
- **Story:** [STORY-GW-SSR-10](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000068
- **Skill declared:** python-pro
- **Depends on:** T00–T02
- **Scaffolded:** 2026-08-29T18:25:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md` T03

## Purpose
Unbound civic green; `legal_process` exact-only green (no dual key); dual fixture: labels+payload → civic lens value **and** pack `lens_id` on same `story_id` (разные `lens` строки; not one `cluster_id`). `ClusterLens` still 10. G10 slice: civic / SSR-04 / SSR-05 tests run, do not weaken.

## Code Facts
- `ClusterLens` 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Membership PK — [`db_sqlite.py:416`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- G10 commands — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.3
- Existing civic / pack tests — `tests/test_clustering_engine.py`, `tests/test_gw_ssr_04_*`, `tests/test_gw_ssr_05_*`

## Acceptance / DoD
- [ ] Dual fixture: civic lens value и pack `lens_id` на одном `story_id`
- [ ] Pack без dual-ключа = T-wave exact-only (`legal_process` зелёный)
- [ ] Civic без binding зелёный
- [ ] `ClusterLens` по-прежнему 10; нет pack lens в enum
- [ ] Не прогонять dual через один `cluster_id`
- [ ] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_10_*.py` (new)
- Reuse civic/04/05 as G10 regression slice (run, do not weaken)

## Out of scope
- Прогонять dual через один `cluster_id`; add pack `lens_id` to `ClusterLens` enum
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
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_10_*.py
.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_clustering_engine.py tests/test_gw_ssr_04_*.py tests/test_gw_ssr_05_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```
