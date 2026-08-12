## Task workspace — `task-m2-02-06-t04-gap-06-live-story-context-persist-or-contract`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — §16 слой 2, **GAP-06** (закрыт: persist `consistency_notes`)
- Связь: регрессионный тест «не персистится» уже может существовать (`test_story_intake_live_context_not_on_record.py`); этот таск — **продуктовое** закрытие gap (persist или сужение контракта).

## Task: fix / implement — `live_story_context.consistency_notes`: персистенция или явный отказ

### Цель
Убрать молчаливую потерю данных: либо перенос `consistency_notes` в `StoryRecord` + Supabase, либо удаление/ошибка на уровне API при передаче поля (с версией контракта).

### Факты из кода (§16)
1) `parse_story_intake_request` принимает `live_story_context` — [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py).
2) `StoryIntakeService.create_story` не читает `request.live_story_context` — [`src/core/application/services.py`](../../../../../../../src/core/application/services.py).

### Gap / Проблема
Решение: **persist** — `live_story_context.consistency_notes` → `StoryRecord.narrative_consistency_notes` → БД.

### AC/DoD
- [x] (P0) Решение: persist (зафиксировано в story и §16).
- [x] (P0) Реализация + колонка `narrative_consistency_notes` (bootstrap + миграция).
- [x] (P1) Тесты: `test_story_intake_live_context_not_on_record.py` (round-trip).

### Где менять код
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) при изменении DDL

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_story_intake_live_context_not_on_record.py tests/test_story_intake_contract.py
```

### Артефакты процесса (`task-execution-process.md`)
- [`BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- [`implementation-plan-m2-02-06-t04.md`](./implementation-plan-m2-02-06-t04.md)
- [`acceptance-verification-m2-02-06-t04.md`](./acceptance-verification-m2-02-06-t04.md)
- [`retrospective-m2-02-06-t04-full.md`](./retrospective-m2-02-06-t04-full.md)
