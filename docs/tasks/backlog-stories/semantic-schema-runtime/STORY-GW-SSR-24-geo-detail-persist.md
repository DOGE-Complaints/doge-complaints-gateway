# STORY-GW-SSR-24 — Persist normalized geo (address depth)

## Meta
- **Key:** `STORY-GW-SSR-24-geo-detail-persist`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — geo-detail wave (sequence **24**)
- **Тип:** implement (domain + sqlite/supabase + migration)
- **Parent REQ:** 40 geo projection / 51 DATA; INDEX **D-SSR-10**
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [geo-detail Шаг 0](./orchestrator-geo-detail-runbook.md)
- **Зависит от:** SSR-23

## Зачем простыми словами

Нормализованная геодетализация должна **лежать на story**: координаты + адрес до предоставленной глубины (улица, диапазон, несколько домов). Иначе cluster/read теряют то, что клиент уже прислал.

## Scope / Out of scope

**In:** расширить [`StoryGeoSnapshot`](../../../../src/core/domain/contracts.py) (`street`, `house` / `house_range` / `houses`, `address_line`, depth/meta as needed). Sqlite ALTER + supabase `_STORY_SELECT_FIELDS` / row map + migration SQL + [`000_full_init.sql`](../../../../supabase/bootstrap/000_full_init.sql) cross-layer ([`test_stories_schema_cross_layer_invariant.py`](../../../../tests/test_stories_schema_cross_layer_invariant.py)). `advance_story_readiness` / `dataclasses.replace` **preserve** новых полей. Omit-probe как у `geo_admin_*` — **не** класть в `required_columns_ready`. При `geo_intake.mirror_to_payload` — dual-write в `structured_payload.geo`. Тесты round-trip: coords + street + range + houses[].

**Out:** IDX / `story_dimensions`; dump raw `geo_detail` целиком в public Issue card; GPT UI.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-24 pkg-000081):** snapshot depth persist sqlite+supabase; omit-probe; not in `required_columns_ready`; G24 PASS 2026-08-30T21:00:56Z | [`contracts.py:28–45`](../../../../src/core/domain/contracts.py); [`db_sqlite.py`](../../../../src/core/infrastructure/db_sqlite.py); [`db_supabase.py:75`](../../../../src/core/infrastructure/db_supabase.py) |
| **Historical (pre-SSR-24):** snapshot lat/lon/admin only | [`contracts.py:28–40`](../../../../src/core/domain/contracts.py) pre-P3 |

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

- SSR-23. Clustering + docs — SSR-25.
