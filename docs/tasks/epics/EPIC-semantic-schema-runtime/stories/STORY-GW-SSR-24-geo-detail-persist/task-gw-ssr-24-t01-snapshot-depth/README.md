# task-gw-ssr-24-t01-snapshot-depth

## Task: implement — extend `StoryGeoSnapshot` depth (T01)

## Meta
- **Story:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:07:09Z
- **Package:** pkg-000081
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-30T20:55:32Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md` T01

## Purpose
Расширить [`StoryGeoSnapshot`](../../../../../../../src/core/domain/contracts.py): `street`, `house` **XOR** `house_range` **XOR** `houses`, `address_line` (depth/meta as needed). Не новые `ClusterLens`.

## Code Facts
1. **As-of-Done (SSR-24 pkg-000081):** `StoryGeoSnapshot` street/house/house_range/houses/address_line — [`contracts.py:28–45`](../../../../../../../src/core/domain/contracts.py).
2. **As-of-Done:** merge overlay writes street/house depth — [`intake_merge.py:61–88`](../../../../../../../src/core/geo/intake_merge.py).
3. `ClusterLens` = 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py).
4. **Historical (pre-SSR-24):** snapshot lat/lon/admin only; merge `admin_*` only — [`contracts.py:28–40`](../../../../../../../src/core/domain/contracts.py) pre-P3.

## Acceptance / DoD
- [x] `StoryGeoSnapshot` несёт street / house depth / address_line
- [x] Нет новых членов `ClusterLens`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/domain/contracts.py`
- Callers constructing `StoryGeoSnapshot` (merge / repos — follow T02–T05)

## Out of scope
- Sqlite/supabase (T02/T03). ClusterLens. GPT UI.
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
rg -n "class StoryGeoSnapshot" -A 16 doge-complaints-gateway/src/core/domain/contracts.py
```
