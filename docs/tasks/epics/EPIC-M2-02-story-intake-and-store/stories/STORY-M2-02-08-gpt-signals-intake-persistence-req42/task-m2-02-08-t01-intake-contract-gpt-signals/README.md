## Task workspace — `task-m2-02-08-t01-intake-contract-gpt-signals`

- Story: [`../STORY-M2-02-08-gpt-signals-intake-persistence-req42.md`](../STORY-M2-02-08-gpt-signals-intake-persistence-req42.md)
- Decision Ref: [`../../../../../../requirements/42-gpt-signals-story-intake-extension.md`](../../../../../../requirements/42-gpt-signals-story-intake-extension.md) §2.1, §3.1

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000022`  
---

## Task: implement — intake contract `gpt_signals` block

### Цель
Добавить опциональный блок `gpt_signals` в intake v2: парсинг, enum-валидация, поле на `StoryIntakeRequest`.

### Факты из кода
1. [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py) — `StoryIntakeRequest` (L60–67): `schema_version`, `submitter`, `narrative`, `origin`, `privacy`, `live_story_context`; нет `gpt_signals`.
2. `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v2"` (L14) — блок добавляется в v2 envelope.
3. Невалидный narrative.language уже даёт `IntakeValidationError` — тот же паттерн для enum-полей gpt_signals.

### Gap / Проблема
GPT шлёт `non_wire_metadata` → wire `gpt_signals` ([`GPT UI/instructions/api-orchestrator.md`](../../../../../../../GPT UI/instructions/api-orchestrator.md)); gateway парсер блок отбрасывает — данные не доходят до persist.

### AC/DoD
- [ ] (P0) `GptSignalsBlock` frozen dataclass: `severity`, `impact_estimation`, `problem_status` — все `str | None`.
- [ ] (P0) `StoryIntakeRequest.gpt_signals: GptSignalsBlock | None`.
- [ ] (P0) Если ключ `gpt_signals` передан — валидировать только присутствующие поля по enum (REQ-42 §2.1); неизвестное значение → `IntakeValidationError`.
- [ ] (P0) Отсутствие ключа `gpt_signals` — `None`, intake без изменений.
- [ ] (P1) Экспорт в [`src/core/intake/__init__.py`](../../../../../../../src/core/intake/__init__.py).

### Где менять код
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py)
- [`src/core/intake/__init__.py`](../../../../../../../src/core/intake/__init__.py)

### Out of scope
- Persist в `story_signals` (T02).
- OpenAPI (T04).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_story_intake_contract.py tests/test_gpt_signals_intake.py -k parse -q
```
