## Task workspace — `task-m2-02-06-t02-gap-03-summary-transport-and-storage`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — §16 слой 1, **GAP-03** (реализация 2026-05-11: закрыт)

## Task: implement — `summary[et/ru/en]` в контракте и персистенции

### Цель
Добавить транспорт и хранение summary (или зафиксировать отказ с ADR), т.к. сейчас поле отсутствует в `StoryIntakeRequest` и `StoryRecord`.

### Факты из кода (§16)
1) `grep summary` по `intake/contracts.py` и `domain/contracts.py` — пусто (см. анализ).
2) Колонки в `public.stories` под summary отсутствуют до явного решения.

### Gap / Проблема
Решение: `narrative.summary` как объект `et|ru|en` → `Narrative.summary_languages`, JSON-колонка `narrative_summary_json` на `stories`.

### AC/DoD
- [x] (P0) Продуктовое решение: хранение в одной JSON-колонке `narrative_summary_json`.
- [x] (P0) Согласованные изменения intake → record → Supabase/SQLite + bootstrap + миграция `20260511_1200_*`.
- [x] (P1) Тесты: `test_story_intake_live_context_not_on_record.py`, bootstrap asserts.

### Где менять код
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py)
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) / `supabase/migrations/` при расширении схемы

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_story_intake_contract.py
```

### Артефакты процесса (`task-execution-process.md`)
- [`BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- [`implementation-plan-m2-02-06-t02.md`](./implementation-plan-m2-02-06-t02.md)
- [`acceptance-verification-m2-02-06-t02.md`](./acceptance-verification-m2-02-06-t02.md)
- [`retrospective-m2-02-06-t02-full.md`](./retrospective-m2-02-06-t02-full.md)
