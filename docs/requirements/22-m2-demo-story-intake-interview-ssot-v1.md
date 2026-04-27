# 22. M2 Demo: Story Intake — решения интервью (SSOT v1)

## 1. Назначение и статус

Этот документ **фиксирует на уровне requirements** итог первого доменного интервью по целевому story intake-контракту для demo / перехода M1 → M2.

| Атрибут | Значение |
|--------|----------|
| Источник (сырой артефакт) | `docs/tasks/task-domain-story-contract-interview-01/interview-report-domain-story-contract-01.md` |
| Дата интервью | 2026-04-26 |
| Область | **Demo**; production и полный конвержент с «широким» envelope из `19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md` — вне этого SSOT до отдельной синхронизации |

**Правило приоритета:** для реализации интеграции с **текущим runtime** `doge-complaints-gateway` (минимальный `StoryIntakeRequest` в коде) решения из раздела 3 этого файла — **целевые требования**; фактическое поведение кода — в разделе 2 (верификация на момент фиксации документа).

---

## 2. Верификация по коду gateway (as-is)

Утверждения ниже проверены по репозиторию `doge-complaints-gateway` (не по GPT UI).

### 2.1 Схема intake и парсер

- Версия intake-схемы в коде: `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v1"` — см. `src/core/intake/contracts.py` (строки с определением константы и проверкой в `parse_story_intake_request`).
- Поля `Narrative.language` и `Narrative.title_hint` объявлены как **опциональные** (`str | None = None`); парсер **не отклоняет** запрос при их отсутствии — см. `parse_story_intake_request` в `src/core/intake/contracts.py` (ветки `language_raw` / `title_hint_raw` → `None` допустимы).

### 2.2 Доменная запись story

- `StoryRecord` содержит `narrative_original_text`, `submitter_external_user_id`, `submitter_identity_issuer`, поля origin/privacy, **не содержит** отдельных полей для `narrative.language`, `narrative.title_hint`, `canonical_type`, `canonical_labels` — см. `src/core/domain/contracts.py` (`class StoryRecord`).

### 2.3 Lifecycle после приёма story

- После сохранения story сервис вычисляет `narrative_complete` как наличие непустого `narrative_original_text` **и** truthy `request.narrative.language` **и** truthy `request.narrative.title_hint`; при `False` статус переходит в `PARTIAL_READY` (из начального `ACCEPTED`) — см. `StoryIntakeService.create_story` / `advance_story_readiness` в `src/core/application/services.py` (логика `narrative_complete` и присвоение `StoryLifecycleStatus.PARTIAL_READY`).

**Замечание по трассировке из интервью:** в отчёте интервью указана строка `application/services.py:28` для `PARTIAL_READY` — **в текущем коде** соответствующая логика находится в блоке `create_story` / `advance_story_readiness` (порядок десятков строк ~73–147), а не на строке 28.

### 2.4 HTTP API

- В runtime зарегистрированы и `POST /intake/stories`, и `POST /issues` — см. `src/core/api/asgi_app.py` (список путей и декораторы `@app.post`).

### 2.5 Ответ `POST /intake/stories`

- Контракт успешного ответа через `StoryIntakeResponse` включает `story_id` и `status` (и обёртку envelope с `trace_id`) — см. `build_story_intake_response` в `src/core/intake/contracts.py`. **Отдельного поля** с результатом extraction/issue в этом контракте **нет** (на момент фиксации документа).

---

## 3. Принятые решения интервью (целевое состояние demo)

Ниже — нормализованная выжимка из разделов 3–4 отчёта интервью. Идентификаторы `D-xx` совпадают с отчётом.

| ID | Решение | Смысл для backend / GPT |
|----|---------|-------------------------|
| D-01 | `POST /issues` deprecated в demo | Внешнее ручное создание issue не primary-path; выключить из публичного сценария или отвечать `410 Gone` (конкретика — в задаче на API boundary). |
| D-02 | Extraction issue — **асинхронно** (фон) | `POST /intake/stories` сохраняет story и возвращает **только** идентификатор и статус приёма; тяжёлая обработка — не в синхронном ответе. |
| D-03 | `language` + `title_hint` **обязательны** | При отсутствии — **HTTP 400** на intake (отказ от модели `PARTIAL_READY` как допустимого исходда для demo при неполном narrative). |
| D-04 | `title_hint` генерирует GPT (конец Phase 7) | Источник — GPT pipeline, не свободный ввод пользователя вне сценария. |
| D-05 | `language` = session language GPT | Маппинг в `narrative.language` из `normalization_metadata.session_language` (контракт GPT — внешний репозиторий `GPT UI`). |
| D-06 | `external_user_id` = wallet address | В demo — фиксированный адрес из mock auth (как в отчёте; реализация страницы — отдельная задача/артефакт gateway). |
| D-07 | Точка M2 для GPT — `POST /intake/stories` | `POST /issues/draft` (M1) — deprecate в пользу intake. |
| D-08 | `narrative.original_text` | Соответствует user-confirmed `description` на **primary** языке из нормализованного payload GPT (не «полированный» summary как единственный источник). |
| D-09 | Расширение контракта | В `StoryIntakeRequest` / persistence: `canonical_type`, `canonical_labels[]`, sidecar под `label_extraction_metadata` (деталь схемы sidecar — open point OP-02). |
| D-10 | `privacy.contains_pii` | По умолчанию `false` в demo; детекция PII — позже. |
| D-11 | Allowlist языков demo | Только `et`, `ru`, `en`; иное — **400**. |

---

## 4. Маппинг GPT → M2 intake (из отчёта)

Источник полей GPT — внешние инструкции репозитория **GPT UI** (ссылки из отчёта: `story-data-model.md`, `story-normalizer.md`, `story-label-taxonomy.md`, `api-orchestrator.md`). Здесь — только таблица маппинга как **требование к согласованию** интеграции.

| Выход GPT (концепт) | Целевое поле M2 intake | Замечание |
|---------------------|------------------------|-----------|
| `normalization_metadata.session_language` | `narrative.language` | Обязательно + allowlist D-11 |
| `canonical_payload.title.{primary}` | `narrative.title_hint` | Обязательно; мультиязычные варианты — см. OP-05 |
| `canonical_payload.description.{primary}` (подтверждённый) | `narrative.original_text` | Уже в контракте |
| `canonical_payload.type` | `narrative.canonical_type` (новое) | Требует расширения контракта и выравнивания enum (OP-01) |
| `canonical_payload.labels[]` | `narrative.canonical_labels[]` (новое) | Таксономия — `story-label-taxonomy.md` |
| `label_extraction_metadata` | sidecar (новое) | OP-02 |
| wallet (demo mock) | `submitter.external_user_id` | Уже в контракте |
| severity / impact / problem_status (non-wire) | не в StoryIntakeRequest | Явно исключены из wire |

---

## 5. Open points (из интервью, без решения в этом SSOT)

| ID | Суть |
|----|------|
| OP-01 | Выравнивание enum типа жалобы GPT ↔ backend (`INCIDENT` / `SERVICE_REQUEST` / `IMPROVEMENT` и т.д.). |
| OP-02 | Точная схема `label_extraction_metadata` в теле intake. |
| OP-03 | Нужна ли персистенция `live_story_context.consistency_notes`. |
| OP-04 | Передача wallet в GPT Actions вне demo. |
| OP-05 | Хранение non-primary языков title/description помимо `original_text`. |
| OP-06 | Семантика `identity_issuer` для wallet. |

---

## 6. Трассировка на задачи и код

| Зона | Задача / действие |
|------|-------------------|
| Расширение контракта + persist + allowlist + 400 | `TASK-INTAKE-STORY-CONTRACT-EXPANSION-02` (и связанные DB-задачи по полям story) |
| Deprecated `/issues`, story-first boundary | `TASK-API-STORY-FIRST-BOUNDARY-01` |
| Асинхронный extraction | отдельная реализация после D-02 (оркестрация/очередь — уточнять в объёме demo) |
| Связь GAP ↔ TASK | `docs/analysis/story-first-gap-task-linkage.md` |
| Кластеризация, пороги из `.env`, cluster→issue | **`23-m2-demo-story-clustering-interview-ssot-v1.md`** (второе интервью; зависит от полей из строки выше) |

---

## 7. Согласованность с документом 19

`19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md` описывает **расширенный** envelope (`structured_signals`, `spa_issue_draft`, и т.д.). Текущий **реализованный** минимальный JSON-контракт в коде — см. `StoryIntakeRequest` в `src/core/intake/contracts.py`.

До полной конвергенции §4–§7 документа 19 с кодом **для demo-итерации** при согласовании полей и поведения GPT ↔ gateway опираться на:

1. этот файл **22** (решения интервью + as-is раздел 2);
2. фактический код в `src/core/intake/contracts.py` и `src/core/application/services.py`.
