## Task workspace — `task-m2-02-09-t06-runtime-docs-openapi-persistence-model`

- Story: [`../STORY-M2-02-09-institution-json-story-column-req43.md`](../STORY-M2-02-09-institution-json-story-column-req43.md)
- Decision Ref: [`../../../../../../requirements/43-institution-json-story-column.md`](../../../../../../requirements/43-institution-json-story-column.md) §4 (docs cascade)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000023`  
---

## Task: docs — API_REFERENCE, OpenAPI, story persistence model

### Цель
Синхронизировать публичную документацию gateway с `narrative.institution` и i18n `payload_json.institution`.

### Факты из кода
1. [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6.3 — narrative fields; добавить `institution`.
2. [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) — `Narrative` schema без `institution`.
3. [`docs/runtime-docs/story-persistence-model.md`](../../../../../../../docs/runtime-docs/story-persistence-model.md) L341 — scalar institution example (обновить на i18n object + Layer 1 column).

### Gap / Проблема
Operators и GPT integrators не видят institution в runtime contract docs.

### AC/DoD
- [ ] (P0) `API_REFERENCE.md`: `narrative.institution` optional `{et,ru,en}`; persistence note `institution_json`.
- [ ] (P0) `openapi.yaml`: property `institution` on Narrative (i18n object).
- [ ] (P0) `story-persistence-model.md`: `stories.institution_json` + `payload_json.institution` as dict.
- [ ] (P1) `pytest tests/test_openapi_runtime_compliance.py -q` green after schema change.

### Где менять код
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md)
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml)
- [`docs/runtime-docs/story-persistence-model.md`](../../../../../../../docs/runtime-docs/story-persistence-model.md)

### Out of scope
- `GPT UI/` docs.
- `docs/tasks/**` (task artifacts).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_openapi_runtime_compliance.py
```
