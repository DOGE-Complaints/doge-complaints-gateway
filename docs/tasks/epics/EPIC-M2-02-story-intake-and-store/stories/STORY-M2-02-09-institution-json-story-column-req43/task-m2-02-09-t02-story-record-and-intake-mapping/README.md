## Task workspace — `task-m2-02-09-t02-story-record-and-intake-mapping`

- Story: [`../STORY-M2-02-09-institution-json-story-column-req43.md`](../STORY-M2-02-09-institution-json-story-column-req43.md)
- Decision Ref: [`../../../../../../requirements/43-institution-json-story-column.md`](../../../../../../requirements/43-institution-json-story-column.md) §2.3, §3.2–3.3

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000023`  
---

## Task: implement — `StoryRecord.narrative_institution` + intake mapping

### Цель
Перенести `request.narrative.institution` в доменную модель при `create_story()`.

### Факты из кода
1. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) L44–66 — `StoryRecord` без `narrative_institution`.
2. [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) L181–216 — `StoryRecord(...)` без institution; `narrative_summary` уже мапится (L193–196).

### Gap / Проблема
Даже после парсера intake institution не сохраняется в `StoryRecord` — нет поля и маппинга.

### AC/DoD
- [ ] (P0) `StoryRecord.narrative_institution: dict[str, str] | None = None`.
- [ ] (P0) `create_story()`: `narrative_institution=request.narrative.institution`.
- [ ] (P1) Idempotency hit path: возврат существующего story без повторного save — institution уже на записи.

### Где менять код
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)

### Out of scope
- SQL/Supabase columns (T03).
- `doge_issues` payload (T04).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_institution_intake.py -k "record or mapping" --co -q
```
