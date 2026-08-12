## Task workspace — `task-m2-02-08-t04-runtime-openapi-api-reference`

- Story: [`../STORY-M2-02-08-gpt-signals-intake-persistence-req42.md`](../STORY-M2-02-08-gpt-signals-intake-persistence-req42.md)
- Decision Ref: [`../../../../../../requirements/42-gpt-signals-story-intake-extension.md`](../../../../../../requirements/42-gpt-signals-story-intake-extension.md) §3.4, §4

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000022`  
---

## Task: docs — API_REFERENCE + OpenAPI `gpt_signals`

### Цель
Синхронизировать публичную документацию gateway intake с runtime v2 и блоком `gpt_signals`.

### Факты из кода
1. [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) L198–214 — `StoryIntakeRequest` enum v1 only; нет `gpt_signals`.
2. [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L415+ — ссылается на intake contracts; нужен § про `gpt_signals`.
3. Эталон enum: REQ-42 §2.1; GPT OpenAPI [`GPT UI/docs/custom-gpt-story-intake-actions.openapi.yaml`](../../../../../../../GPT UI/docs/custom-gpt-story-intake-actions.openapi.yaml) schema `GptSignals`.

### Gap / Проблема
Операторы и GPT Actions видят устаревший v1 OpenAPI — расхождение с [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py) v2.

### AC/DoD
- [ ] (P0) `openapi.yaml`: component `GptSignals`; property `gpt_signals` on `StoryIntakeRequest`; `schema_version` enum includes `m2.story_intake_envelope.v2`.
- [ ] (P0) `API_REFERENCE.md`: описание опционального блока, enums, отсутствие в `StoryRecord`.
- [ ] (P1) [`tests/test_openapi_runtime_compliance.py`](../../../../../../../tests/test_openapi_runtime_compliance.py) green after schema update (if asserts schema_version).

### Где менять код
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml)
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md)

### Out of scope
- `GPT UI/instructions/*` (REQ-23 Done).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_openapi_runtime_compliance.py
```
