# STORY-GW-SSR-24 — Persist normalized geo (address depth)

## Meta
- **Key:** `STORY-GW-SSR-24-geo-detail-persist`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — geo-detail wave (sequence **24**)
- **Тип:** implement (domain + sqlite/supabase + migration)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md)
- **Parent REQ:** 40 geo projection / 51 DATA; INDEX **D-SSR-10**
- **Decision:** INDEX **D-SSR-10**
- **decision_ref:** backlog SSR-24 + INDEX **D-SSR-10**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-23](../STORY-GW-SSR-23-geo-detail-intake-contract/STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000081-20260830-gw-ssr-24-geo-detail-persist.yaml`](../../../../gateway-active-packages/pkg-000081-20260830-gw-ssr-24-geo-detail-persist.yaml)
- **Git:** только `semantic-schema-runtime` — [geo-detail Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md)
- **Зависит от:** SSR-23 ([pipeline](../STORY-GW-SSR-23-geo-detail-intake-contract/STORY-GW-SSR-23-geo-detail-intake-contract.md)); G23 PASS
- **Scaffolded:** 2026-08-30T20:55:32Z
- **P4 audit:** 2026-08-30T21:07:09Z [`audit-gw-ssr-24-geo-detail-persist-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-24-geo-detail-persist-2026-08-30.md) · product AC yes · G1 OPEN SSOT (T01–T06 Code Facts) · G2 WAIVED-likely operator

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 40 / 51 DATA | INDEX **D-SSR-10** |
| Decision | INDEX **D-SSR-10** | persist `StoryGeoSnapshot` depth |

- **Разблокирует:** G24 → SSR-25 (не этот pkg).
- **Не reopen:** SSR-01…05 / 08–23 product; T-wave G3 historical
- **Не трогаем:** GPT UI; `ClusterLens`; `GET /schema-active`; IDX / `story_dimensions`; bullrun §«Актуальная точка»

## Nested tasks (pkg-000081)

| ID | Folder |
|----|--------|
| T01 | [`task-gw-ssr-24-t01-snapshot-depth`](./task-gw-ssr-24-t01-snapshot-depth/README.md) |
| T02 | [`task-gw-ssr-24-t02-sqlite-alter`](./task-gw-ssr-24-t02-sqlite-alter/README.md) |
| T03 | [`task-gw-ssr-24-t03-supabase-migration`](./task-gw-ssr-24-t03-supabase-migration/README.md) |
| T04 | [`task-gw-ssr-24-t04-lifecycle-preserve`](./task-gw-ssr-24-t04-lifecycle-preserve/README.md) |
| T05 | [`task-gw-ssr-24-t05-mirror-payload`](./task-gw-ssr-24-t05-mirror-payload/README.md) |
| T06 | [`task-gw-ssr-24-t06-tests`](./task-gw-ssr-24-t06-tests/README.md) |
| T07 | [`task-gw-ssr-24-t07-story-acceptance-gate`](./task-gw-ssr-24-t07-story-acceptance-gate/README.md) |
| T08 | [`task-gw-ssr-24-t08-audit-g1-as-of-done-ssot`](./task-gw-ssr-24-t08-audit-g1-as-of-done-ssot/README.md) |

## Зачем простыми словами

Нормализованная геодетализация должна **лежать на story**: координаты + адрес до предоставленной глубины (улица, диапазон, несколько домов). Иначе cluster/read теряют то, что клиент уже прислал.

## Scope / Out of scope

**In:** расширить [`StoryGeoSnapshot`](../../../../../../src/core/domain/contracts.py) (`street`, `house` / `house_range` / `houses`, `address_line`, depth/meta as needed). Sqlite ALTER + supabase `_STORY_SELECT_FIELDS` / row map + migration SQL + [`000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) cross-layer ([`test_stories_schema_cross_layer_invariant.py`](../../../../../../tests/test_stories_schema_cross_layer_invariant.py)). `advance_story_readiness` / `dataclasses.replace` **preserve** новых полей. Omit-probe как у `geo_admin_*` — **не** класть в `required_columns_ready`. При `geo_intake.mirror_to_payload` — dual-write в `structured_payload.geo`. Тесты round-trip: coords + street + range + houses[].

**Out:** IDX / `story_dimensions`; dump raw `geo_detail` целиком в public Issue card; GPT UI.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-24 pkg-000081):** `StoryGeoSnapshot` street/house/house_range/houses/address_line | [`contracts.py:28–45`](../../../../../../src/core/domain/contracts.py) |
| **As-of-Done:** sqlite ALTER + INSERT/SELECT depth cols | [`db_sqlite.py:153`](../../../../../../src/core/infrastructure/db_sqlite.py), [`:403–407`](../../../../../../src/core/infrastructure/db_sqlite.py) |
| **As-of-Done:** supabase SELECT/row + omit-probe; **не** в `required_columns_ready` | [`db_supabase.py:75`](../../../../../../src/core/infrastructure/db_supabase.py), [`:371–377`](../../../../../../src/core/infrastructure/db_supabase.py), [`:538`](../../../../../../src/core/infrastructure/db_supabase.py) |
| **As-of-Done:** migration + `000_full_init` | [`20260830_2100_gw_ssr_24_stories_geo_detail.sql`](../../../../../../supabase/migrations/20260830_2100_gw_ssr_24_stories_geo_detail.sql) |
| **As-of-Done:** merge/mirror snapshot depth | [`intake_merge.py`](../../../../../../src/core/geo/intake_merge.py) |
| G24 PASS | pkg-000081; `2026-08-30T21:00:56Z` — **801 passed**, 18 skipped, 10 deselected |
| `ClusterLens` = 10 | [`types.py:10–22`](../../../../../../src/core/cluster/types.py) |
| **Historical (pre-SSR-24):** snapshot lat/lon/admin only; sqlite/supabase `geo_admin_*` only | [`contracts.py:28–40`](../../../../../../src/core/domain/contracts.py) pre-P3 |

## Стыковка

Не ломать civic `geo_filter_bucket` (admin_*). Новые поля — для pack lenses и audit. Hosted apply migration = operator proof как SSR-09 (артефакт на диске обязателен).

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Domain | Расширить StoryGeoSnapshot | Новые ClusterLens |
| **T02** | Sqlite | ALTER + INSERT/SELECT | Drop admin_* |
| **T03** | Supabase | SELECT/row + migration + full_init | required_columns_ready |
| **T04** | Lifecycle | replace / advance preserve | Silent wipe |
| **T05** | Mirror | structured_payload.geo when pack says | Dump whole payload public |
| **T06** | Tests | round-trip + cross-layer | live_integration proof |
| **T07** | Gate | persist ok; omit-probe; ClusterLens=10 | |

## Target / AC

- [x] Street / house_range / houses / coords persist на story.
- [x] Lifecycle advance не стирает новые geo fields.
- [x] Binding/geo новые cols не в `required_columns_ready`.
- [x] Mirror в payload когда `mirror_to_payload`.
- [x] Migration SQL на диске.

## Dependencies

- SSR-23 Done (G23). Clustering + docs — SSR-25.
