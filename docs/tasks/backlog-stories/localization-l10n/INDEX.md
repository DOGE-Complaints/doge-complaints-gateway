# Localization (L10N) — backend story package · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/localization-l10n/`
**Тип:** backlog (продуктовая проработка; не активный build-пакет — не путать с `gateway-active-packages/`).
**Метод проработки:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — все факты по фактическому коду, пути указаны.
**Источник требований (фронт):** [`REQUIREMENTS-BACKEND-L10N.md`](../../../../../spa-app/docs/tasks/backlog-stories/localization/REQUIREMENTS-BACKEND-L10N.md) (REQ-BE-1/2/3).
**Интервью PM/CTO:** 2026-06-03 (решения D-L10N ниже).

> **L10N** = «localization» (l + 10 букв + n) — отраслевое сокращение для локализации/мультиязычности.
> **MT** = «machine translation», машинный (авто) перевод.

## Коды статусов (S)
⚪ Todo · 🟡 In Progress · 🔵 Implemented (Waiting Acceptance) · 🟢 Done (Committed) · ⏸️ Deferred (future)

## Стори пакета

| S | Key | Story | Закрывает | Severity (FE) | Зависит от |
|---|-----|-------|-----------|---------------|------------|
| 🔵 | GW-L10N-01 | [Сохранение реального мультиязычного контента в проекции](./STORY-GW-L10N-01-projection-content-i18n-preservation.md) | основа REQ-BE-1 | 🔴 | — | Done |
| 🔵 | GW-L10N-02 | [`original_locale` в публичной проекции issue](./STORY-GW-L10N-02-original-locale-in-public-projection.md) | REQ-BE-1 | 🔴 | GW-L10N-01 | Done |
| 🔵 | GW-L10N-03 | [Анонимный приём телеметрии непереведённых меток](./STORY-GW-L10N-03-label-miss-telemetry-sink.md) | REQ-BE-2 | 🟠 | — | Done |
| ⏸️ | GW-L10N-04 | [Реестр таксономии меток (FUTURE)](./STORY-GW-L10N-04-label-taxonomy-registry-future.md) | REQ-BE-3 | ⚪ отложено | GW-L10N-03 (опц.) | Deferred |

**Progress:** 3/4 Done (75%); GW-L10N-04 Deferred

## Решения интервью (D-L10N, 2026-06-03)

- **D-L10N-1 (цель REQ-BE-1):** «сохранить реальные переводы + добавить `original_locale`». Бэк перестаёт схлопывать контент в идентичные копии (см. GW-L10N-01) и отдаёт `original_locale` (GW-L10N-02). Без сохранения переводов MT-маркер фронта бессмысленен (сейчас все 3 локали одинаковы).
- **D-L10N-2 (семантика `original_locale`):** **список** всех различных языков-оригиналов историй в кластере (не один скаляр). Локали вне списка фронт трактует как MT.
- **D-L10N-3 (телеметрия меток):** **отдельная таблица** + простой запрос/агрегатор для оператора (не только лог).
- **D-L10N-4 (состав пакета):** BE-1 + BE-2, плюс BE-3 зафиксирован как явная future-заглушка.

## Ключевой verified-факт пакета (контекст для всех сторей)

Публичная проекция issue хранится как `payload_json` (JSON-блоб) в таблице `doge_issues` ([db_supabase.py:638-712](../../../../src/core/infrastructure/db_supabase.py#L638-L712)). Поэтому **новые поля контента и `original_locale` идут внутрь JSON — миграция схемы для них не нужна**; нужен ре-проджектинг существующих issue для бэкфилла. Телеметрия (GW-L10N-03) — наоборот, требует новой таблицы.

Текущий разрыв (verified): пайплайн проекции берёт один текст и копирует его в `{et,ru,en}` одинаково ([extraction_policy.py:171-175](../../../../src/core/projection/extraction_policy.py#L171-L175)), при этом реальный 3-язычный контент из intake (`narrative.title/description`, обязателен во всех языках — [contracts.py:255-258](../../../../src/core/intake/contracts.py#L255-L258)) теряется. Язык-оригинал есть в `StoryRecord.narrative_language`, доступен в точке сборки проекции ([issue_create.py:140-160](../../../../src/core/application/issue_create.py#L140-L160)), но в проекцию не прокидывается.
