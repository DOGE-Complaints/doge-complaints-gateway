## Task workspace — `task-m2-02-09-t04-issue-projection-institution-propagation`

- Story: [`../STORY-M2-02-09-institution-json-story-column-req43.md`](../STORY-M2-02-09-institution-json-story-column-req43.md)
- Decision Ref: [`../../../../../../requirements/43-institution-json-story-column.md`](../../../../../../requirements/43-institution-json-story-column.md) §2.4, §3.6

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000023`  
---

## Task: implement — institution propagation to `payload_json`

### Цель
Заполнять `doge_issues.payload_json.institution` как `{et, ru, en}` из dominant story `narrative_institution`; обновить read filter для i18n payload.

### Факты из кода
1. [`src/core/projection/extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py) L146–167 — `build_projection_input_from_draft` не передаёт `institution`.
2. [`src/core/projection/input.py`](../../../../../../../src/core/projection/input.py) L19 — `institution: str | None` (scalar).
3. [`src/core/projection/dto.py`](../../../../../../../src/core/projection/dto.py) L18 — `DOGEIssue.institution: str | None`.
4. [`src/core/projection/read_filters.py`](../../../../../../../src/core/projection/read_filters.py) L159 — сравнение `payload.get("institution")` со строкой query param.
5. [`select_dominant_story`](../../../../../../../src/core/projection/extraction_policy.py) L26–32 — выбор dominant story для кластера (REQ-40/36 pattern).
6. [`story-persistence-model.md`](../../../../../../../docs/runtime-docs/story-persistence-model.md) L341 — пример scalar institution (устарел vs REQ-43).

### Gap / Проблема
Institution теряется до issue creation: сейчас в payload попадает только через paths без story column; после T01–T03 нужен wire в promotion bridge.

### AC/DoD
- [ ] (P0) `ProjectionInput.institution` и `DOGEIssue.institution` → `dict[str, str] | None`; `to_public_dict()` emits object.
- [ ] (P0) `build_projection_input_from_draft` / bridge: `institution = dominant_story.narrative_institution` (document in code comment).
- [ ] (P0) `read_filters`: institution query param matches primary locale via `primary_i18n_text()` (or documented et/ru/en equality).
- [ ] (P1) Не ломать существующие contract tests — обновить fixtures где institution был string.

### Где менять код
- [`src/core/projection/input.py`](../../../../../../../src/core/projection/input.py)
- [`src/core/projection/dto.py`](../../../../../../../src/core/projection/dto.py)
- [`src/core/projection/mapper.py`](../../../../../../../src/core/projection/mapper.py)
- [`src/core/projection/extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py)
- [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py) (bridge path if needed)
- [`src/core/projection/read_filters.py`](../../../../../../../src/core/projection/read_filters.py)

### Out of scope
- SPA UI.
- GPT orchestrator.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_institution_intake.py tests/test_filter_projection_rows_contract.py -k institution
```
