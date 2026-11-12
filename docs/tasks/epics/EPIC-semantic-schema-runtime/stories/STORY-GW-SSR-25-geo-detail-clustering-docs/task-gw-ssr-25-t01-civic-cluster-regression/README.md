# task-gw-ssr-25-t01-civic-cluster-regression

## Task: tests — civic cluster regression with snapshot depth (T01)

## Meta
- **Story:** [STORY-GW-SSR-25](../STORY-GW-SSR-25-geo-detail-clustering-docs.md)
- **Type:** tests
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:31:59Z
- **Package:** pkg-000082
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-30T21:20:50Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-25-geo-detail-clustering-docs.md` T01

## Purpose
Civic clustering остаётся зелёным с расширенным `StoryGeoSnapshot` (street/houses не ломают unlabeled / `geo_filter_bucket`). `test_clustering_engine.py` + civic кейсы в `test_gw_ssr_25_*`. Не новые `ClusterLens`.

## Code Facts
1. **As-of-Done (SSR-25 pkg-000082):** civic snapshot depth не меняет `geo_filter_bucket` / cluster key — [`test_gw_ssr_25_geo_detail_clustering.py`](../../../../../../../tests/test_gw_ssr_25_geo_detail_clustering.py); [`test_clustering_engine.py`](../../../../../../../tests/test_clustering_engine.py) `test_snapshot_depth_does_not_split_civic_district_bucket`.
2. **As-of-Done:** unlabeled → `geo:agnostic`; missing admin + street depth → `geo:unknown` — [`scope.py:94–101`](../../../../../../../src/core/geo/scope.py).
3. Civic `geo_filter_bucket` = admin_* only — [`scope.py:55–63`](../../../../../../../src/core/geo/scope.py); engine — [`engine.py:101`](../../../../../../../src/core/cluster/engine.py), [`:126`](../../../../../../../src/core/cluster/engine.py).
4. Snapshot depth persist (SSR-24) — [`contracts.py:41–45`](../../../../../../../src/core/domain/contracts.py).
5. `ClusterLens` = 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py).
6. **Historical (P1 scaffold):** no `test_gw_ssr_25_*`.

## Acceptance / DoD
- [x] Civic clustering зелёный с snapshot depth (unlabeled + `geo_filter`)
- [x] `test_gw_ssr_25_*` civic кейс(ы) на диске
- [x] Нет новых членов `ClusterLens`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_25_*.py` (new)
- `doge-complaints-gateway/tests/test_clustering_engine.py` only if fixture needs snapshot depth (regression, not new lens)

## Out of scope
- Pack exact lenses (T02). Manual (T03). Matrix (T04). Gate (T05).
- Overlay bans (every task):
  - Civic/pack cluster regression; manuals `geo_intake`; README/matrix; tests `test_gw_ssr_25_*`.
  - G25 = **full** offline pytest (`-m "not live_integration"`) + `test_clustering_engine.py` + `test_gw_ssr_25_*`.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет invent HTTP geo-filter API. Нет IDX / QRY / `story_dimensions`. Нет GPT UI / instruction pack. Нет SPA map overlay.
  - Civic `geo_filter_bucket` остаётся `admin_*`. Не dual-source env+pack для geo knobs (D-SSR-9).
  - **Нет SSR-06/07/12.** Не reopen 01–24 product. Не стартовать 26.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
python3 -m pytest -q -m "not live_integration" doge-complaints-gateway/tests/test_clustering_engine.py doge-complaints-gateway/tests/test_gw_ssr_25_*.py
rg -n "class ClusterLens" -A 14 doge-complaints-gateway/src/core/cluster/types.py
```
