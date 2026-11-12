# task-gw-ssr-24-t06-tests

## Task: tests — `test_gw_ssr_24_*` round-trip + cross-layer (T06)

## Meta
- **Story:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist.md)
- **Type:** tests
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:07:09Z
- **Package:** pkg-000081
- **Skill declared:** python-pro
- **Depends on:** T01–T05
- **Scaffolded:** 2026-08-30T20:55:32Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md` T06

## Purpose
Тесты `test_gw_ssr_24_*`: round-trip coords + street + range + houses[]. Cross-layer invariant. Не `live_integration` как proof.

## Code Facts
1. **As-of-Done (SSR-24 pkg-000081):** [`test_gw_ssr_24_geo_detail_persist.py`](../../../../../../../tests/test_gw_ssr_24_geo_detail_persist.py) round-trip street/range/houses/coords.
2. Cross-layer — [`test_stories_schema_cross_layer_invariant.py`](../../../../../../../tests/test_stories_schema_cross_layer_invariant.py).
3. G24 commands — [`orchestrator-geo-detail-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md) §6.3.
4. **Historical (pre-SSR-24):** no `test_gw_ssr_24_*` this scaffold.

## Acceptance / DoD
- [x] `tests/test_gw_ssr_24_*.py` round-trip street/range/houses/coords
- [x] Cross-layer invariant green
- [x] Не `live_integration` как proof
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_24_*.py` (new)
- `doge-complaints-gateway/tests/test_stories_schema_cross_layer_invariant.py` (if needed)

## Out of scope
- live_integration hosted apply. ClusterLens. GPT UI.
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
# P3 only — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_24_*.py
python3 -m pytest -q -m "not live_integration" tests/test_stories_schema_cross_layer_invariant.py
```
