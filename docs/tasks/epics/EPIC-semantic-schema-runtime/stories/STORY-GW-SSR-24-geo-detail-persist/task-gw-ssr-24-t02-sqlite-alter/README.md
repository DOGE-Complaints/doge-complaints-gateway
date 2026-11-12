# task-gw-ssr-24-t02-sqlite-alter

## Task: implement — sqlite ALTER + INSERT/SELECT (T02)

## Meta
- **Story:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:07:09Z
- **Package:** pkg-000081
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T20:55:32Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md` T02

## Purpose
Sqlite ALTER + INSERT/SELECT для новых geo depth cols. Не drop `geo_admin_*`.

## Code Facts
1. **As-of-Done (SSR-24 pkg-000081):** sqlite depth cols `geo_street`/`geo_house`/`geo_house_range`/`geo_houses_json`/`geo_address_line` + `geo_admin_*` remain — [`db_sqlite.py:153`](../../../../../../../src/core/infrastructure/db_sqlite.py), [`:403–407`](../../../../../../../src/core/infrastructure/db_sqlite.py).
2. **As-of-Done:** snapshot depth on `StoryGeoSnapshot` — [`contracts.py:41–45`](../../../../../../../src/core/domain/contracts.py).
3. **Historical (pre-SSR-24):** sqlite geo cols = `geo_admin_*` only; snapshot без street — [`db_sqlite.py:122`](../../../../../../../src/core/infrastructure/db_sqlite.py) pre-P3.

## Acceptance / DoD
- [x] ALTER + INSERT/SELECT round-trip street/range/houses/coords
- [x] `geo_admin_*` columns remain
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/infrastructure/db_sqlite.py`

## Out of scope
- Supabase migration (T03). Drop admin_*. ClusterLens.
- Overlay bans (every task):
  - StoryGeoSnapshot depth; sqlite/supabase; migration; omit-probe; mirror; lifecycle preserve.
  - Tests `test_gw_ssr_24_*`. G24 = **full** offline pytest (`-m "not live_integration"`) + `test_stories_schema_cross_layer_invariant.py`.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет IDX / QRY / `story_dimensions`. Нет GPT UI.
  - Не dump raw `geo_detail` в public Issue card.
  - Новые geo cols **не** в `required_columns_ready` (omit-probe как `geo_admin_*`).
  - Не drop `geo_admin_*`. Civic `geo_filter_bucket` (admin_*) stays.
  - Hosted apply migration = operator proof как SSR-09 (артефакт на диске обязателен; не live_integration).
  - **Нет SSR-06/07/12.** Не reopen 01–23 product. Не стартовать 25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "geo_admin_|geo_street|house_range" doge-complaints-gateway/src/core/infrastructure/db_sqlite.py
```
