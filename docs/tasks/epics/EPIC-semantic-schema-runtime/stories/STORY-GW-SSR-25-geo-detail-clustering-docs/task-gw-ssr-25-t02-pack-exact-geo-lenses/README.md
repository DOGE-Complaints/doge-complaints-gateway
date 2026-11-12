# task-gw-ssr-25-t02-pack-exact-geo-lenses

## Task: tests — pack exact membership on `geo.*` (T02)

## Meta
- **Story:** [STORY-GW-SSR-25](../STORY-GW-SSR-25-geo-detail-clustering-docs.md)
- **Type:** tests
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:31:59Z
- **Package:** pkg-000082
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T21:20:50Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-25-geo-detail-clustering-docs.md` T02

## Purpose
Pack exact membership по `geo.street` / `geo.district` / … из mirrored `structured_payload`. Fixture + optional tallinn pack lens update только если нужно для demo. Не второй cron. Не новые `ClusterLens`.

## Code Facts
1. **As-of-Done (SSR-25 pkg-000082):** pack exact membership на `geo.district` (tallinn `geographic_district_micro`) + fixture `geo.street` — [`test_gw_ssr_25_geo_detail_clustering.py`](../../../../../../../tests/test_gw_ssr_25_geo_detail_clustering.py).
2. **As-of-Done:** missing `geo.district` + `missing_value_policy=skip` → no geo membership. `pack.json` не меняли (district lens уже есть).
3. Pack exact = payload `source_fields` — [`pack_engine.py:57`](../../../../../../../src/core/schema/pack_engine.py), [`:129–140`](../../../../../../../src/core/schema/pack_engine.py).
4. Tallinn `geographic_district_micro` = `geo.district`; payload `geo.street` optional — [`pack.json:15–19`](../../../../../../../schema-packs/tallinn_civic/v1/pack.json), [`:101–102`](../../../../../../../schema-packs/tallinn_civic/v1/pack.json).
5. `ClusterLens` = 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py).
6. **Historical (P1 scaffold):** no `test_gw_ssr_25_*`.

## Acceptance / DoD
- [x] Pack exact membership по настроенным `geo.*` lenses (fixture)
- [x] Нет второго cron / нет новых `ClusterLens`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_25_*.py`
- Optional: `schema-packs/tallinn_civic/v1/pack.json` lens `source_fields` only if demo needs extra `geo.*`

## Out of scope
- Civic engine rewrite (T01). Manual (T03). Matrix (T04). Gate (T05).
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
python3 -m pytest -q -m "not live_integration" doge-complaints-gateway/tests/test_gw_ssr_25_*.py
rg -n "geo.street|geo.district" doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json
```
