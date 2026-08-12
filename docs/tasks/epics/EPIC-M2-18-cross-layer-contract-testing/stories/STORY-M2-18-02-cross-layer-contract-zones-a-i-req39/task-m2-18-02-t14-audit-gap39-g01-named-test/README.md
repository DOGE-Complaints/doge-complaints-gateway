## Task workspace — `task-m2-18-02-t14-audit-gap39-g01-named-test`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md`](../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md) §6 GAP-39-G01; Zone G

---
**Приоритет:** P1  
**Сложность:** S  
**Оценка времени:** ~30 мин  
**Статус:** ready  
**Wave:** audit override (`run_mode=story18_audit_req39_followup`)  
---

## Task: tests — REQ-39 G-01 named test (traceability alias)

### Цель
Закрыть трассируемость G-01: тест с именем `test_story_select_fields_covered_by_bootstrap` (или документированная ссылка G-01 → A-01), без дублирования логики проверки.

### Почему это важно (риск)
REQ-39 §Zone G ссылается на `test_story_select_fields_covered_by_bootstrap`; фактически та же семантика уже в `test_story_select_fields_all_in_bootstrap_sql` (A-01, ~L75) — AC-трассировка ломается.

### Факты из кода
1. [`test_supabase_bootstrap_schema.py`](../../../../../../../tests/test_supabase_bootstrap_schema.py) — `test_story_select_fields_all_in_bootstrap_sql` покрывает `_STORY_SELECT_FIELDS` vs bootstrap SQL.
2. Аудит **Вариант A (рекомендуется):** thin alias test calling A-01.

### Gap / Проблема
**AUDIT-GAP-39-G01:** naming / traceability gap (не функциональный дефект).

### AC/DoD
- [ ] (P0) Добавить `test_story_select_fields_covered_by_bootstrap` — alias/wrapper на существующую проверку A-01.
- [ ] (P1) Либо (Вариант B): одна строка в REQ-39 §Zone G «G-01 covered by A-01» — только если оператор выберет docs-only path.
- [ ] (P0) `pytest tests/test_supabase_bootstrap_schema.py -q` green.

### Где менять код
- [`tests/test_supabase_bootstrap_schema.py`](../../../../../../../tests/test_supabase_bootstrap_schema.py)
- Опционально: [`39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) §Zone G (docs-only)

### Out of scope
- Bootstrap SQL / runtime schema changes.
- `pkg-000020` edits.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_supabase_bootstrap_schema.py -k 'g01 or story_select_fields'
```
