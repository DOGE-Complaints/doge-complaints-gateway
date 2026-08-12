## Task workspace — `task-m2-02-07-t01-intake-contract-v2-parse-and-validation`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: [`../../../../../../requirements/33-multilingual-story-intake-contract-v2.md`](../../../../../../requirements/33-multilingual-story-intake-contract-v2.md) §2; [`../../../../../../analysis/gap-interview-decisions-2026-05-13.md`](../../../../../../analysis/gap-interview-decisions-2026-05-13.md) G-01

## Task: implement — intake contract v2 parse and validation

### Цель
Перевести `parse_story_intake_request` на `m2.story_intake_envelope.v2`: dict `{et, ru, en}` для `title` и `description`, опциональный `summary`, обязательные `session_language` и `submitter.identity_issuer`; отклонять v1 с понятной ошибкой.

### Факты из кода
1. [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py) — `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v1"`; `Narrative` с `title_hint` и `title_hint_et/ru/en`; `Submitter.identity_issuer: str | None`.
2. Парсер требует `narrative.title_hint` (L133–135); `description` и `session_language` отсутствуют; `summary` уже как object → `summary_languages` (L172–184).

### Gap / Проблема
GPT шлёт dict-поля по `story-data-model.md`; gateway принимает v1 flat — потеря данных и несовместимость с demo (REQ-33 §1).

### AC/DoD
- [ ] (P0) `INTAKE_SCHEMA_VERSION` → `m2.story_intake_envelope.v2`; v1 payload → `IntakeValidationError` с указанием ожидаемой версии.
- [ ] (P0) Обязательные `narrative.title`, `narrative.description`, `narrative.session_language` (`et`|`ru`|`en`); опциональный `summary` dict.
- [ ] (P0) `submitter.identity_issuer` обязателен (не пустая строка).
- [ ] (P1) Удалены из `Narrative`: `title_hint`, `title_hint_et/ru/en`, `summary_languages` tuple (заменены v2-полями).

### Где менять код
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_intake_contract.py -q --tb=short
```
