## Task workspace — `task-m2-02-09-t05-institution-intake-acceptance-tests`

- Story: [`../STORY-M2-02-09-institution-json-story-column-req43.md`](../STORY-M2-02-09-institution-json-story-column-req43.md)
- Decision Ref: [`../../../../../../requirements/43-institution-json-story-column.md`](../../../../../../requirements/43-institution-json-story-column.md) §5

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000023`  
---

## Task: tests — REQ-43 acceptance for institution intake

### Цель
End-to-end acceptance: intake → `stories.institution_json` → issue `payload_json.institution` (i18n dict).

### Факты из кода
1. Паттерн: [`tests/test_gpt_signals_intake.py`](../../../../../../../tests/test_gpt_signals_intake.py) — sqlite `TestClient`, idempotency headers.
2. REQ §5 — 202/400, NULL column, promotion roundtrip.
3. Нет `tests/test_institution_intake.py` в репо (создать).

### Gap / Проблема
Нет regression suite для institution wire path.

### AC/DoD
- [ ] (P0) `tests/test_institution_intake.py` (new): valid `narrative.institution` → 202 + sqlite `institution_json` row.
- [ ] (P0) Без institution → 202, column NULL.
- [ ] (P0) Incomplete i18n (missing `en`) → 400.
- [ ] (P0) Roundtrip: intake → `create_issue` / cluster path → `payload_json.institution` dict matches story.
- [ ] (P1) Parse unit tests for `parse_optional_i18n_dict` institution branch.

### Где менять код
- `tests/test_institution_intake.py` (new)
- [`tests/intake_v2_fixtures.py`](../../../../../../../tests/intake_v2_fixtures.py) (helper payload if needed)

### Out of scope
- GPT UI tests.
- OpenAPI compliance (T06 may add cross-check).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_institution_intake.py
```
