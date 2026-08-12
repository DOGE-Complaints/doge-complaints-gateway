## Task workspace — `task-m2-02-07-t08-gap33-03-test-unsupported-session-language`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: [`../../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md`](../../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md) GAP-33-03; REQ-33 §2.5

## Task: tests — reject unsupported `session_language`

### Цель
Верифицировать AC REQ-33 §2.5: `session_language` вне `et|ru|en` → `IntakeValidationError` (и HTTP 400 на уровне endpoint).

### Факты из кода
1. Есть `test_parse_story_intake_request_rejects_unsupported_language` для `narrative.language="de"`.
2. Аналогичного теста для `session_language="de"` нет (GAP-33-03).

### Gap / Проблема
**GAP-33-03 (P2):** код корректен, AC не покрыт тестом.

### AC/DoD
- [x] (P2) Unit-тест: `session_language="de"` → `IntakeValidationError`, match `Supported values: et, ru, en`.
- [x] (P2) HTTP 400: `test_intake_stories_endpoint_returns_400_for_unsupported_session_language`.

### Где менять код
- [`tests/test_story_intake_contract.py`](../../../../../../../tests/test_story_intake_contract.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_intake_contract.py::test_parse_story_intake_request_rejects_unsupported_session_language -q
```
