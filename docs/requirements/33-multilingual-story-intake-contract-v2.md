# REQ-33: Multilingual Story Intake Contract v2

**Статус:** Реализовано (2026-05-15, STORY-M2-02-07 / pkg-000012)  
**Источник:** Gap-интервью 2026-05-13, G-01, G-07, G-08  
**Приоритет:** P0 (блокирует demo)  
**Связанные SA:** SA-04, SA-05, SA-10  

---

## 1. Контекст

Текущий intake-контракт (`m2.story_intake_envelope.v1`) использует плоские строковые поля:
- `title_hint: str` — одиночная строка без указания языка
- `title_hint_et/ru/en: str | None` — плоские опциональные поля
- Нет поля `description`
- Нет поля `session_language`

GPT-модель (`GPT UI/instructions/story-data-model.md §4.1`) **уже формирует** payload с dict-форматом `{et, ru, en}` для всех текстовых полей. Текущий gateway теряет эти данные, принимая старый flat-формат — нарушение data contract между GPT и gateway.

---

## 2. Требования

### 2.1 Версия контракта
- `schema_version`: `m2.story_intake_envelope.v1` → `m2.story_intake_envelope.v2`
- Breaking change — все клиенты (GPT-оркестратор) должны мигрировать на v2

### 2.2 Новый формат полей `narrative`

| Поле | Тип | Обязательное | Описание |
|------|-----|-------------|----------|
| `title` | `{et: str, ru: str, en: str}` | ✅ ДА | Заменяет `title_hint` и `title_hint_et/ru/en` |
| `description` | `{et: str, ru: str, en: str}` | ✅ ДА | Новое поле; GPT уже отправляет его |
| `summary` | `{et: str, ru: str, en: str}` | ❌ нет | Опциональный структурированный краткий текст |
| `session_language` | `"et"\|"ru"\|"en"` | ✅ ДА | Первичный язык сессии GPT (`normalization_metadata.session_language`) |
| `language` | `"et"\|"ru"\|"en"` | ✅ ДА | Язык оригинального текста (существует, сохраняется) |

**Удаляются:**
- `title_hint: str` (плоское поле)
- `title_hint_et: str | None`
- `title_hint_ru: str | None`
- `title_hint_en: str | None`
- `summary_languages: tuple[tuple[str,str],...]` (заменяется на `summary: dict`)

### 2.3 Поле `submitter.identity_issuer` — обязательное (eID gate)

- Текущий тип: `str | None` (опциональное)
- Целевой тип: `str` (обязательное)
- При отсутствии: HTTP 400 с сообщением о необходимости eID верификации
- Логика: все подающие истории должны быть верифицированы через eID; gateway не принимает истории без идентификатора провайдера

### 2.4 Idempotency-Key fallback

При отсутствии заголовка `Idempotency-Key`:
```python
idempotency_key = header_value or hashlib.sha256(raw_body_bytes).hexdigest()
```
- Защищает от дублей при GPT-retry (сетевые ошибки)
- Использовать сырые байты запроса (до `json.loads()`) для стабильности hash

### 2.5 HTTP-валидация

При нарушении обязательных полей v2:
- Отсутствие `narrative.title` → HTTP 400
- Отсутствие `narrative.description` → HTTP 400
- Отсутствие `narrative.session_language` → HTTP 400
- Отсутствие `submitter.identity_issuer` → HTTP 400
- Неверный `session_language` (не `et/ru/en`) → HTTP 400

---

## 3. Изменения `StoryRecord` (доменный уровень)

| Поле | Изменение |
|------|-----------|
| `narrative_title: dict[str,str]` | ✅ Новое — заменяет `narrative_title_hint` + flat поля |
| `narrative_description: dict[str,str]` | ✅ Новое |
| `narrative_summary: dict[str,str] \| None` | ✅ Новое — заменяет `summary_languages` tuple |
| `narrative_session_language: str \| None` | ✅ Новое |
| `narrative_title_hint: str \| None` | ❌ Удалить |
| `narrative_title_hint_et/ru/en: str \| None` | ❌ Удалить |
| `submitter_identity_issuer: str` | ♻️ NOT NULL (убрать `| None`) |

---

## 4. Cascade — файлы для изменения

| Файл | Изменение |
|------|-----------|
| `intake/contracts.py` | Полная переработка `Narrative` dataclass и `parse_story_intake_request()` |
| `domain/contracts.py` | `StoryRecord` новые/изменённые поля; `Submitter.identity_issuer: str` |
| `application/services.py` | Маппинг Narrative v2 → StoryRecord; `narrative_complete` логика |
| `api/handlers.py` | SHA-256 idempotency fallback; identity_issuer gate |
| `api/asgi_app.py` | Обеспечить доступность `raw_body` до парсинга JSON |
| `infrastructure/db_sqlite.py` | Новые колонки |
| `infrastructure/db_supabase.py` | Новые колонки + JSONB |
| Bootstrap SQL | Миграция новых колонок в `stories` |
| `GPT UI/api-orchestrator.md` | Обновить wire contract |
| Тесты intake | Полное обновление под v2 |

---

## 5. Acceptance Criteria

- [x] `POST /intake/stories` с v2 payload → HTTP 202, story создана со всеми новыми полями
- [x] `POST /intake/stories` без `identity_issuer` → HTTP 400
- [x] `POST /intake/stories` без `narrative.title` → HTTP 400
- [x] `POST /intake/stories` без `narrative.description` → HTTP 400
- [x] Повторный `POST` с идентичным body и без `Idempotency-Key` → тот же `story_id`
- [x] `StoryRecord.narrative_title` содержит `{et, ru, en}` из payload
- [x] `StoryRecord.narrative_session_language` заполнен
- [x] `schema_version` v1 → HTTP 400 с понятным сообщением

**Связанные таски:** декомпозиция в [`STORY-M2-02-07`](../tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-07-multilingual-intake-contract-v2/STORY-M2-02-07-multilingual-intake-contract-v2.md) (`TASK-M2-02-07-T01`…`T05`); operative queue [`pkg-000012-20260513-req33-multilingual-intake-v2.yaml`](../tasks/gateway-active-packages/pkg-000012-20260513-req33-multilingual-intake-v2.yaml).

---

## 6. Не в scope этого REQ

- Multilingual отображение в SPA (относится к SA-07 / EPIC-M2-06)
- Миграция существующих v1 историй (separate migration task)
