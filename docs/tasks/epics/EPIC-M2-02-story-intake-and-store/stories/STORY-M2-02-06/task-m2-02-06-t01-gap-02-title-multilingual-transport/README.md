## Task workspace — `task-m2-02-06-t01-gap-02-title-multilingual-transport`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — §16 слой 1, **GAP-02** (реализация safe-override 2026-05-11: закрыт в коде + §16)

## Task: implement — транспорт и хранение мультиязычного `title` (et/ru/en)

### Цель
Устранить безвозвратную потерю двух из трёх языковых вариантов заголовка: сейчас в intake и домене только одно поле `title_hint` / `narrative_title_hint`.

### Факты из кода (§16)
1) `StoryRecord`: одно поле `narrative_title_hint` — см. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py).
2) `StoryIntakeRequest` / narrative: один `title_hint` — [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py).
3) GPT-инструкции `api-orchestrator.md §5.2.1` отправляют только `title[session_language]` — см. анализ §16.

### Gap / Проблема
Реализация: опциональные `title_hint_et|ru|en` в intake/`Narrative`, колонки на `StoryRecord` + SQLite/Supabase + bootstrap/миграция; §16 обновлён.

### AC/DoD
- [x] (P0) Принято продуктовое решение: расширение контракта полями `_et/_ru/_en` (совместимо с существующим `title_hint`).
- [x] (P0) Реализация согласована с `parse_story_intake_request`, `StoryIntakeService.create_story`, `db_supabase.save_story` и DDL `public.stories`.
- [x] (P1) Тесты: `test_story_intake_live_context_not_on_record.py`, `test_supabase_bootstrap_schema.py` (миграция narrative extensions).

### Где менять код
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py)
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- GPT UI: `instructions/api-orchestrator.md` (вне этого репозитория — отдельный PR)

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_story_intake_contract.py tests/test_issue_create_service.py
```

### Артефакты процесса (`task-execution-process.md`)
- [`BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- [`implementation-plan-m2-02-06-t01.md`](./implementation-plan-m2-02-06-t01.md)
- [`acceptance-verification-m2-02-06-t01.md`](./acceptance-verification-m2-02-06-t01.md)
- [`retrospective-m2-02-06-t01-full.md`](./retrospective-m2-02-06-t01-full.md)
