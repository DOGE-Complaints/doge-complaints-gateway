# task-gw-ssr-24-t04-lifecycle-preserve

## Task: implement — preserve new geo fields on advance (T04)

## Meta
- **Story:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:07:09Z
- **Package:** pkg-000081
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T20:55:32Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md` T04

## Purpose
`advance_story_readiness` / `dataclasses.replace` **preserve** новых geo fields. Не silent wipe.

## Code Facts
1. `advance_story_readiness` = `replace(current, lifecycle_status, updated_at)` — [`services.py:537–541`](../../../../../../../src/core/application/services.py). Frozen dataclass `replace` keeps unspecified fields on `current`.
2. **As-of-Done (SSR-24 pkg-000081):** snapshot depth fields exist — [`contracts.py:41–45`](../../../../../../../src/core/domain/contracts.py); preserve covered by `test_advance_preserves_geo_depth`.
3. **Historical (pre-SSR-24):** snapshot без street — [`contracts.py:28–40`](../../../../../../../src/core/domain/contracts.py) pre-P3.

## Acceptance / DoD
- [x] Advance / replace не стирает street/house depth/coords
- [x] Нет silent wipe на lifecycle
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/services.py` (only if replace drops fields)
- Any other `replace(` / rebuild of `StoryRecord` that reconstructs `geo`

## Out of scope
- ClusterLens. GPT UI. live_integration.
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
rg -n "advance_story_readiness|replace\(" doge-complaints-gateway/src/core/application/services.py
```
