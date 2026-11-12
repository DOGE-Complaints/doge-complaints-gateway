# STORY-GW-SSR-12 — Complementary pair matching (experimental; not exact-lens)

## Meta
- **Key:** `STORY-GW-SSR-12-complementary-pair-matching`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 📝 **Draft (experimental)** — sequence **12**; не T-wave; не IDX (06). Refine до P1.3.
- **Приоритет:** ⚪ LOW — эксперимент ноды (lost/found и подобные)
- **Тип:** implement (новый matcher, не ClusteringEngine) — **не активировать** до refine
- **Parent REQ:** 51 **не** покрывает pair-matching; CL exact ≠ complementary
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [runbook Шаг 0](./orchestrator-t-wave-runbook.md)
- **Зависит от:** SSR-02 persist payload; pack schema для полей. Не зависит от SSR-06/07.

## Зачем простыми словами

Модель «потерянная / найденная кошка» в JSON Schema pack **можно** описать уже сейчас (поля + знак). Текущая кластеризация **не** соединяет «−» с «+»: exact-lens кладёт одинаковые значения в одну кучу. Нужен другой механизм: комплементарный знак + схожесть по критериям. Приюты / уведомления — вне первого слоя.

## Scope / Out of scope

**In when refined:** in-process matcher по `structured_payload`; pack **data** описывает: поле знака, какие поля скорить, что считается комплементом (`lost`↔`found`); тесты на фикстурах payload; не использовать `ClusterLens`. Честно: это **не** `exact_lenses` и не civic taxonomy.

**Out now:** public HTTP path (не invent, пока отдельный REQ не назовёт); интеграция приютов; GPT UI; reuse issue SHA-256 «embedding» как семантическое сходство кошек; менять `algorithm: exact` так, чтобы lost и found попали в один `cluster_id`.

## Verified current state

| Fact | Ref |
|------|-----|
| Pack membership | `algorithm != "exact"` → `None` [`pack_engine.py:100–101`](../../../../src/core/schema/pack_engine.py) |
| Exact join | одинаковые leaf tokens → один `cluster_id` [`:44–46`](../../../../src/core/schema/pack_engine.py) |
| Issue embedding | SHA-256 текста карточки [`issue_create.py:442–451`](../../../../src/core/application/issue_create.py) — не feature-vector кошки |
| `lost_pets` pack | **Not found** |

## Стыковка (inventory)

Не притворяться, что новая `exact_lenses[].algorithm` строка сама заработает: non-exact сегодня skip.

Не класть matching в `process_all_pending` civic/pack promote без отдельного решения (иначе «куча lost» станет Issue «все потерянные»).

Пример pack полей (черновик, не loader contract): `status` ∈ {lost, found}, критерии `color`, `district`, … — JSON Schema. Matcher отдельно от `SchemaPackClusterEngine`.

HTTP / доска пар — **Unknown** until named. Первый слой = engine + tests; read API — refine.

## Подзадачи (только refine-inventory)

| ID | Слой | Задача | Не делать сейчас |
|----|------|--------|------------------|
| **R1** | Product | Нода-эксперимент vs платформенный matcher в schema runtime | Приюты, push |
| **R2** | Contract | Pack keys для sign + score fields; не ломать existing `exact_lenses` | Менять legal_process |
| **R3** | Engine | Complementary + similarity; не SHA-256 issue embedding | `ClusterLens` |
| **R4** | API | Path unnamed | Роут в `asgi_app` |

## Target / AC (после refine)

- [ ] Matcher соединяет opposite sign + scored criteria; exact-lens T-wave green.
- [ ] Нет: lost+found в одном exact `cluster_id` как «решение».
- [ ] Нет обязательного HTTP в этой Draft-постановке.

## Границы

- Не T-wave. Не SSR-06 index. Не SSR-10 dual civic.
- Пакет gateway: да (payload + pack data). GPT/SPA — siblings later.

## Условие refine / активации

- Явная команда оператора (эксперимент кошки / общая pair-модель).
- Иначе остаётся Draft.
