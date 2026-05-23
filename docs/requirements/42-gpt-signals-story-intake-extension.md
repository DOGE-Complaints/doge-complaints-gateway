# REQ-42: GPT Signals — intake extension и персистенция в story_signals

**Статус:** requirements — ready for tasking  
**Источник:** Gap-интервью 2026-05-21 (Q6 — non_wire_metadata → story_signals)  
**Приоритет:** P1  
**Зависит от:** REQ-33 (intake v2), REQ-34 (story_signals table)  
**GPT-парная задача:** REQ-23 (GPT UI/docs/requirements/)

---

## 1. Контекст

GPT-модель (story-normalizer) выдаёт три классификационных сигнала в блоке `non_wire_metadata`:
- `severity` — тяжесть проблемы (`LOW` / `MEDIUM` / `HIGH` / `CRITICAL`)
- `impact_estimation` — оценка масштаба (`LOCAL` / `DISTRICT` / `CITY` / `NATIONAL`)
- `problem_status` — статус проблемы (`ONGOING` / `RESOLVED` / `RECURRING` / `UNKNOWN`)

Сейчас эти поля помечены «non-wire» и сервер их не принимает. Принято решение: персистировать как GPT-сигналы через уже существующую таблицу `story_signals` с `extraction_policy = "gpt.story_classifier.v1"`.

Таблица `story_signals` (REQ-34) принимает произвольный `signals_json` — схема уже позволяет это без изменений. Нужен только новый опциональный блок в intake-контракте и маппинг в `services.py`.

---

## 2. Требования

### 2.1 Новый intake-блок `gpt_signals` (опциональный)

```json
{
  "schema_version": "m2.story_intake_envelope.v2",
  ...
  "gpt_signals": {
    "severity": "HIGH",
    "impact_estimation": "DISTRICT",
    "problem_status": "ONGOING"
  }
}
```

| Поле | Тип | Обязательное | Допустимые значения |
|------|-----|-------------|---------------------|
| `gpt_signals` | object | ❌ нет | Если передан — применяются валидации ниже |
| `gpt_signals.severity` | string | ❌ нет (если блок передан) | `"LOW"`, `"MEDIUM"`, `"HIGH"`, `"CRITICAL"` |
| `gpt_signals.impact_estimation` | string | ❌ нет | `"LOCAL"`, `"DISTRICT"`, `"CITY"`, `"NATIONAL"` |
| `gpt_signals.problem_status` | string | ❌ нет | `"ONGOING"`, `"RESOLVED"`, `"RECURRING"`, `"UNKNOWN"` |

Если `gpt_signals` отсутствует — сервер продолжает работу без изменений (никакая запись в story_signals не создаётся для этой политики).

Если `gpt_signals` передан с неизвестным значением enum → HTTP 400 с сообщением о недопустимом значении.

### 2.2 Персистенция в story_signals

После успешного сохранения StoryRecord сервер записывает:

```python
{
    "story_id": story.story_id,
    "extraction_policy": "gpt.story_classifier.v1",
    "signals_json": {
        "severity": gpt_signals.severity,           # None если отсутствует
        "impact_estimation": gpt_signals.impact_estimation,
        "problem_status": gpt_signals.problem_status,
        "source": "gpt_intake_v1"
    }
}
```

Запись выполняется в рамках той же транзакции, что и `save_story()`. Если `gpt_signals` не передан — запись не создаётся (не создавать пустую запись).

### 2.3 Политика версионирования

`extraction_policy = "gpt.story_classifier.v1"` — константа. Определена в `services.py` (рядом с `STORY_EMBEDDING_POLICY_VERSION`).

---

## 3. Изменения в слоях

### 3.1 Intake contract (`src/core/intake/contracts.py`)

- Добавить dataclass `GptSignalsBlock(frozen=True)` с полями `severity`, `impact_estimation`, `problem_status` (все `str | None`)
- Добавить валидацию enum-значений в `parse_story_intake_request()`
- `StoryIntakeRequest` получает опциональное поле `gpt_signals: GptSignalsBlock | None`

### 3.2 Application layer (`src/core/application/services.py`)

- Константа `GPT_CLASSIFIER_POLICY_VERSION = "gpt.story_classifier.v1"`
- В `create_story()`: после `save_story()` — если `request.gpt_signals is not None`, вызвать `story_signals_store.save_signals(story_id, policy, signals_json)`
- Не блокировать успех intake при ошибке записи signals (log + continue)

### 3.3 Infrastructure

- `db_supabase.py`: метод `save_story_signals()` — upsert в `story_signals` по `(story_id, extraction_policy)`
- `db_sqlite.py`: аналогичный метод для тестового backend

### 3.4 Bootstrap SQL

```sql
-- Не требуется: таблица story_signals уже существует (REQ-34)
-- Только убедиться что primary key (story_id, extraction_policy) допускает upsert
```

---

## 4. Cascade — файлы для изменения

| Файл | Изменение |
|------|-----------|
| `src/core/intake/contracts.py` | Новый `GptSignalsBlock` dataclass, расширение `StoryIntakeRequest` |
| `src/core/application/services.py` | `GPT_CLASSIFIER_POLICY_VERSION`, вызов save_signals в create_story |
| `src/core/infrastructure/db_supabase.py` | `save_story_signals()` — upsert |
| `src/core/infrastructure/db_sqlite.py` | `save_story_signals()` — upsert |
| `docs/runtime-docs/api-reference/API_REFERENCE.md` | §6: добавить описание блока `gpt_signals` |
| `GPT UI/instructions/api-orchestrator.md` | Добавить `gpt_signals` в StoryIntakeRequest transform |

---

## 5. Acceptance Criteria

- [ ] `POST /intake/stories` с `gpt_signals: {severity: "HIGH", impact_estimation: "DISTRICT", problem_status: "ONGOING"}` → HTTP 202
- [ ] После intake: `SELECT * FROM story_signals WHERE story_id=X AND extraction_policy='gpt.story_classifier.v1'` — возвращает запись с корректным `signals_json`
- [ ] `POST /intake/stories` без `gpt_signals` → HTTP 202, запись в story_signals для этой политики не создаётся
- [ ] `POST /intake/stories` с `gpt_signals.severity = "INVALID"` → HTTP 400
- [ ] Тест в `tests/`: roundtrip intake с gpt_signals → story_signals persisted
- [ ] Ошибка записи signals не блокирует HTTP 202 для основного intake

---

## 6. Не в scope этого REQ

- Индексация/поиск по gpt_signals (отдельная задача аналитики)
- Изменение кластерной логики на основе severity/impact (отдельный REQ)
- Добавление других GPT-классификационных полей (расширяется через новую политику `gpt.story_classifier.v2`)
