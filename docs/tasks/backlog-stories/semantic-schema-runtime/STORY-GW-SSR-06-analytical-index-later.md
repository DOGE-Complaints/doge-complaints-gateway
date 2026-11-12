# STORY-GW-SSR-06 — story_dimensions / generic index (post-T-wave Draft)

## Meta
- **Key:** `STORY-GW-SSR-06-analytical-index-later`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 📝 **Draft (post-T-wave refine)** — sequence **6** (после product 08–15; не сразу после T-wave 1–5). Не T-wave close. Не overnight post-T-wave. Доработать после SSR-08…15.
- **Приоритет:** ⚪ LOW — later 51 / parent §33.2
- **Тип:** implement (index) — **не активировать** до refine
- **Parent REQ:** 51 §2 later, §5 items 11; AC-005/006/012 — **без** naming HTTP path
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [runbook Шаг 0](./orchestrator-t-wave-runbook.md)
- **Зависит от:** SSR-02; refine **после** SSR-08…15 (INDEX: product wave затем 06)

## Зачем простыми словами

Черновик later-51: аналитические измерения из payload. Сейчас постановка тонкая — **обязательно refine** после T-wave. Не закрывает REQ-51 T-wave (AC-018).

## Scope / Out of scope

**In when refined/activated:** typed dimensions rebuildable from payload+schema/profile (AC-012); privacy: non-indexable fields not in `story_dimensions` (AC-006). Generic filter **mechanism** (AC-005) без HTTP path в этом Draft (51 §6 Q1 still open).

**Out now:** invent HTTP path/query; включать в T-wave DoD; identity (**D-SSR-3**).

## Verified current state

| Fact | Ref |
|------|-----|
| `story_dimensions` in src+sql | **Not found** (Grep) |
| `SchemaRuntime.build_index` | parent Protocol only; SSR-01 stub/no-op — **не** считать IDX сделанным |
| `/ready` table set | [`REQUIRED_READINESS_TABLES`](../../../../src/core/infrastructure/db_supabase.py) `:29` — новая таблица сюда **без** отдельного решения = риск 503 (L10N-03 lesson) |
| Filter HTTP | parent QRY unnamed; [`asgi_app.py`](../../../../src/core/api/asgi_app.py) не имеет generic dimension filter |

## Стыковка (inventory, не execute)

Шов есть: rebuild из `structured_payload` + `schema_id`/`bound_schema_version` (SSR-02). Физическая таблица `story_dimensions` **не** существует — это новая сущность, не ALTER stories.

**Не** писать сейчас таск «добавить в REQUIRED_READINESS_TABLES» — это refine-решение после T-wave (host readiness).

**Не** invent HTTP path в субтасках.

## Подзадачи (только refine-inventory — не P3)

| ID | Слой | Задача | Не делать сейчас |
|----|------|--------|------------------|
| **R1** | Model | Выбрать: колонки parent IDX-001 vs JSONB document. | Implement |
| **R2** | Readiness | Явно: новая таблица в `REQUIRED_READINESS_TABLES`? колонки в `required_columns_ready`? (это **разные** множества; оба дают 503/fail если включить рано). | Добавлять в set |
| **R3** | Privacy | Как pack marks `index: false` стыкуется с loader contract SSR-01. | |
| **R4** | Query | Mechanism без named HTTP (in-process API). Path = Unknown. | Роут в `asgi_app` |

## Target / AC (после refine)

- [ ] AC-GW-REQ3-05/06 as IDX (HTTP path остаётся Unknown until a later REQ names it)
- [ ] AC-012 reindexability
- [ ] Refine pass: сузить AC, pack metadata keys, tests из parent §29 Repository (typed dimension / privacy-excluded)

## Границы

- **Не** T-wave sequence 1–5.
- Всегда после product 08–15, затем эта стори, затем SSR-07.

## Условие refine / активации

- SSR-08…15 Done (INDEX: после T-wave product) **или** явная команда оператора на refine.
- Иначе остаётся Draft; T-wave close от этой стори не зависит.
