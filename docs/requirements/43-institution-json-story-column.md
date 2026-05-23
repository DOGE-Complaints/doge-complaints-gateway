# REQ-43: institution_json — колонка в stories и intake-поле

**Статус:** requirements — ready for tasking  
**Источник:** Gap-интервью 2026-05-21 (Q7 — institution → stories column)  
**Приоритет:** P1  
**Зависит от:** REQ-33 (intake v2), REQ-40 (geo propagation pattern для doge_issues)  
**GPT-парная задача:** REQ-22 (GPT UI/docs/requirements/) — маппинг canonical_payload.institution → narrative.institution

---

## 1. Контекст

`institution` — структурированное i18n-поле `{et, ru, en}`, описывающее ведомство/организацию к которой относится жалоба. GPT уже способен генерировать это поле (в `canonical_payload.institution`), но в demo-режиме явно его omit-ит.

Сейчас `institution` персистируется **только** в `doge_issues.payload_json` — туда оно попадает через clustering/promotion pipeline. Это означает потерю данных: если issue ещё не создан, а история уже содержит `institution`, поле теряется.

Принято решение: хранить `institution` непосредственно в `stories` в новой колонке `institution_json` (JSONB). Это обеспечивает:
1. Сохранность данных с момента intake
2. Прямую доступность при кластеризации и при построении issue-проекций
3. Полноту Story persistence layer (согласно `docs/runtime-docs/story-persistence-model.md`)

---

## 2. Требования

### 2.1 Новое intake-поле `narrative.institution` (опциональное)

```json
{
  "narrative": {
    "original_text": "...",
    "language": "et",
    "session_language": "et",
    "title": {"et": "...", "ru": "...", "en": "..."},
    "description": {"et": "...", "ru": "...", "en": "..."},
    "institution": {"et": "Tallinna Linnavalitsus", "ru": "Таллинская городская управа", "en": "Tallinn City Government"}
  }
}
```

| Поле | Тип | Обязательное | Описание |
|------|-----|-------------|----------|
| `narrative.institution` | `{et: str, ru: str, en: str}` | ❌ нет | Ведомство/организация. Если передан — все три языковые ключа обязательны. |

Валидация: если `institution` передан — применить `parse_optional_i18n_dict()` (аналогично `summary`). При отсутствии хотя бы одного языкового ключа → HTTP 400.

### 2.2 Новая колонка в `stories`

```sql
alter table public.stories
    add column if not exists institution_json jsonb;
```

- Тип: `jsonb`
- Nullable: `true` (опциональное поле)
- Значение по умолчанию: `null`

### 2.3 StoryRecord — новое поле

```python
@dataclass
class StoryRecord:
    ...
    narrative_institution: dict[str, str] | None = None  # {et, ru, en} | None
```

### 2.4 Propagation в doge_issues.payload_json

При построении `DOGEIssue` через promotion pipeline:
- Если `story.narrative_institution` не None → использовать как `institution` в `payload_json`
- Если несколько stories в кластере имеют разные institution → брать institution из story с наибольшим readiness_score, либо применять majority vote (логика на усмотрение реализующего — задокументировать в коде)
- Текущий `doge_issues.payload_json.institution` формат остаётся без изменений (`{et, ru, en}`)

---

## 3. Изменения в слоях

### 3.1 Intake contract (`src/core/intake/contracts.py`)

- В `NarrativeBlock`: добавить `institution: dict[str,str] | None = None`
- В `parse_story_intake_request()`: валидация через `parse_optional_i18n_dict("institution", ...)`
- Константы enum-значений не нужны (свободный текст)

### 3.2 Domain (`src/core/domain/contracts.py`)

- `StoryRecord`: добавить поле `narrative_institution: dict[str, str] | None = None`

### 3.3 Application layer (`src/core/application/services.py`)

- В маппинге `parse_story_intake_request() → StoryRecord`: `narrative_institution = request.narrative.institution`

### 3.4 Infrastructure

- `db_supabase.py`:
  - `_STORY_SELECT_FIELDS`: добавить `institution_json`
  - `save_story()`: маппить `narrative_institution` → `institution_json`
  - `_row_to_story_record()`: читать `institution_json` обратно в `narrative_institution`
- `db_sqlite.py`: аналогично
- `db_inmemory.py`: аналогично

### 3.5 Bootstrap SQL (миграция)

```sql
-- Добавить в 000_full_init.sql и как отдельную миграцию:
alter table public.stories
    add column if not exists institution_json jsonb;
```

### 3.6 Promotion pipeline

- `src/core/promotion/` или `src/core/application/issue_create.py`: при построении `DOGEIssue` — извлечь `institution` из `narrative_institution` связанных stories

---

## 4. Cascade — файлы для изменения

| Файл | Изменение |
|------|-----------|
| `src/core/intake/contracts.py` | `NarrativeBlock.institution`, валидация |
| `src/core/domain/contracts.py` | `StoryRecord.narrative_institution` |
| `src/core/application/services.py` | Маппинг в create_story |
| `src/core/infrastructure/db_supabase.py` | SELECT fields, save, read |
| `src/core/infrastructure/db_sqlite.py` | DDL + save/read |
| `src/core/infrastructure/db_inmemory.py` | save/read |
| `src/core/application/issue_create.py` | institution propagation в DOGEIssue |
| `supabase/bootstrap/000_full_init.sql` | `add column if not exists institution_json jsonb` |
| `docs/runtime-docs/api-reference/API_REFERENCE.md` | §6.3: narrative fields table |
| `docs/runtime-docs/story-persistence-model.md` | Layer 1: добавить institution_json |
| `GPT UI/instructions/api-orchestrator.md` | Добавить institution в StoryIntakeRequest |

---

## 5. Acceptance Criteria

- [ ] `POST /intake/stories` с `narrative.institution: {et, ru, en}` → HTTP 202
- [ ] После intake: `SELECT institution_json FROM stories WHERE story_id=X` → `{"et": "...", "ru": "...", "en": "..."}`
- [ ] `POST /intake/stories` без `narrative.institution` → HTTP 202, `institution_json IS NULL` в БД
- [ ] `POST /intake/stories` с `narrative.institution: {et: "...", ru: "..."}` (без `en`) → HTTP 400
- [ ] `DOGEIssue.payload_json.institution` заполнен из `StoryRecord.narrative_institution` при promotion
- [ ] Тест roundtrip: intake с institution → story_record.narrative_institution → issue.payload_json.institution

---

## 6. Не в scope этого REQ

- UI для отображения institution в SPA (SA-07)
- Нормализация/классификация institution (canonical institution registry — отдельный REQ)
- Индексация `institution_json` для full-text поиска
