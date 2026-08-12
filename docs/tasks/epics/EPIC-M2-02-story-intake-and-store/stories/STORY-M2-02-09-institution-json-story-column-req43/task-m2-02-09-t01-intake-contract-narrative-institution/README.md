## Task workspace — `task-m2-02-09-t01-intake-contract-narrative-institution`

- Story: [`../STORY-M2-02-09-institution-json-story-column-req43.md`](../STORY-M2-02-09-institution-json-story-column-req43.md)
- Decision Ref: [`../../../../../../requirements/43-institution-json-story-column.md`](../../../../../../requirements/43-institution-json-story-column.md) §2.1, §3.1

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000023`  
---

## Task: implement — intake `narrative.institution` (i18n)

### Цель
Добавить опциональное поле `narrative.institution` в intake v2 с валидацией полного `{et, ru, en}`.

### Факты из кода
1. [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py) L29–39 — `Narrative` без `institution`; `summary` уже через `parse_optional_i18n_dict` (L238–240).
2. [`src/core/domain/narrative_i18n.py`](../../../../../../../src/core/domain/narrative_i18n.py) L30–42 — `parse_optional_i18n_dict` / `parse_required_i18n_dict`.
3. Отсутствие ключа → `None`; неполный объект → `ValueError` → `IntakeValidationError` (паттерн summary).

### Gap / Проблема
GPT может отдавать `canonical_payload.institution`, но gateway intake не парсит `narrative.institution` — данные не попадают в story layer ([`43-institution-json-story-column.md`](../../../../../../requirements/43-institution-json-story-column.md) §1).

### AC/DoD
- [ ] (P0) `Narrative.institution: dict[str, str] | None`.
- [ ] (P0) `parse_story_intake_request()` — `parse_optional_i18n_dict(..., field_name="institution", parent="narrative")`.
- [ ] (P0) Неполный `{et, ru, en}` → `IntakeValidationError` → HTTP 400.
- [ ] (P0) Ключ отсутствует → `institution is None`.

### Где менять код
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py)

### Out of scope
- `StoryRecord` / DB (T02–T03).
- Issue projection (T04).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_institution_intake.py -k parse
```
