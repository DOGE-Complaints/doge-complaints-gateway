# task-gw-ssr-24-t03-supabase-migration

## Task: implement — supabase SELECT/row + migration + full_init (T03)

## Meta
- **Story:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:07:09Z
- **Package:** pkg-000081
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T20:55:32Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md` T03

## Purpose
Supabase `_STORY_SELECT_FIELDS` / row map + migration SQL + [`000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql). Omit-probe как `geo_admin_*`. **Не** класть новые cols в `required_columns_ready`. Hosted apply = operator (артефакт на диске).

## Code Facts
1. **As-of-Done (SSR-24 pkg-000081):** SELECT includes `geo_street`/`geo_house*`/`geo_address_line` — [`db_supabase.py:75`](../../../../../../../src/core/infrastructure/db_supabase.py).
2. **As-of-Done:** omit-probe `_STORIES_GEO_DETAIL_COLUMNS`; **не** в `required_columns_ready` — [`db_supabase.py:371–377`](../../../../../../../src/core/infrastructure/db_supabase.py), [`:538`](../../../../../../../src/core/infrastructure/db_supabase.py).
3. **As-of-Done:** `000_full_init.sql` SSR-24 alter block — [`000_full_init.sql:44–50`](../../../../../../../supabase/bootstrap/000_full_init.sql); migration [`20260830_2100_gw_ssr_24_stories_geo_detail.sql`](../../../../../../../supabase/migrations/20260830_2100_gw_ssr_24_stories_geo_detail.sql).
4. Existing geo migration — [`20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql`](../../../../../../../supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql).
5. Cross-layer invariant — [`test_stories_schema_cross_layer_invariant.py`](../../../../../../../tests/test_stories_schema_cross_layer_invariant.py).
6. **Historical (pre-SSR-24):** SELECT/`000_full_init` geo = `geo_admin_*` only — [`db_supabase.py:74`](../../../../../../../src/core/infrastructure/db_supabase.py) pre-P3.

## Acceptance / DoD
- [x] SELECT/row map новых geo depth cols
- [x] Migration SQL на диске; `000_full_init.sql` synced
- [x] Новые cols **не** в `required_columns_ready`; omit-probe like `geo_admin_*`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/infrastructure/db_supabase.py`
- `doge-complaints-gateway/supabase/migrations/`
- `doge-complaints-gateway/supabase/bootstrap/000_full_init.sql`

## Out of scope
- `required_columns_ready` include. live_integration hosted apply. ClusterLens.
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
rg -n "required_columns_ready" -A 20 doge-complaints-gateway/src/core/infrastructure/db_supabase.py
ls doge-complaints-gateway/supabase/migrations/*geo* 2>/dev/null || ls doge-complaints-gateway/supabase/migrations/ | tail -5
```
