# task-gw-ssr-24-t05-mirror-payload

## Task: implement — dual-write `structured_payload.geo` (T05)

## Meta
- **Story:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:07:09Z
- **Package:** pkg-000081
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T20:55:32Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md` T05

## Purpose
При `geo_intake.mirror_to_payload` — dual-write depth в `structured_payload.geo` (в т.ч. street/house после persist). Не dump whole payload / raw `geo_detail` в public Issue card.

## Code Facts
1. **As-of-Done (SSR-24 pkg-000081):** `mirror_geo_to_payload` writes snapshot street/house depth — [`intake_merge.py:136–161`](../../../../../../../src/core/geo/intake_merge.py).
2. Services call `mirror_geo_to_payload` when pack says — [`services.py:292–296`](../../../../../../../src/core/application/services.py).
3. **As-of-Done:** merge overlay кладёт street на snapshot — [`intake_merge.py:61–88`](../../../../../../../src/core/geo/intake_merge.py).
4. **Historical (pre-SSR-24):** merge не кладёт street на snapshot — [`intake_merge.py:51–79`](../../../../../../../src/core/geo/intake_merge.py) pre-P3.

## Acceptance / DoD
- [x] Mirror `structured_payload.geo` when `mirror_to_payload`
- [x] Нет dump raw `geo_detail` / whole payload public
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/geo/intake_merge.py`
- `doge-complaints-gateway/src/core/application/services.py`

## Out of scope
- Public Issue card dump. ClusterLens. GPT UI.
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
rg -n "mirror_geo_to_payload|mirror_to_payload" doge-complaints-gateway/src/core/geo/intake_merge.py doge-complaints-gateway/src/core/application/services.py
```
