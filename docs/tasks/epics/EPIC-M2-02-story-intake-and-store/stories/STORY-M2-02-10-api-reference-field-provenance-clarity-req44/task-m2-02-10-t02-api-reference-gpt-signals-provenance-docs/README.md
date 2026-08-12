## Task workspace — `task-m2-02-10-t02-api-reference-gpt-signals-provenance-docs`

- Story: [`../STORY-M2-02-10-api-reference-field-provenance-clarity-req44.md`](../STORY-M2-02-10-api-reference-field-provenance-clarity-req44.md)
- Decision Ref: [`../../../../../../requirements/44-api-reference-field-provenance-clarity.md`](../../../../../../requirements/44-api-reference-field-provenance-clarity.md) §3.3
- Audit Ref: [`../../../../../../../../GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../../../../../GPT%20UI/docs/audit-field-provenance-2026-05-24.md) §3.7 — FINDING-02

---
**Приоритет:** P3
**Сложность:** S
**Статус:** todo
**Wave:** `pkg-000024`
---

## Task: docs — API_REFERENCE §6.3 `gpt_signals` provenance note

### Цель
Сделать явным, что три поля `gpt_signals` (`severity`, `impact_estimation`, `problem_status`) — это **GPT classifier outputs** (inference из контекста интервью), а не user-declared атрибуты. Одна локальная правка в `API_REFERENCE.md §6.3`, без изменения кода/контрактов.

### Факты из кода
1. [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L348–362 — текущая секция `#### gpt_signals — object, optional (REQ-42)`; описание ограничено wire-уровнем (когда блок present/absent, валидация enum), без объяснения **семантики источника**.
2. [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L360 — текущая строка:
   ```
   Persisted `signals_json` always includes `"source": "gpt_intake_v1"`. A failure to persist signals is logged and does **not** change HTTP `202` for the intake.
   ```
   Маркер `gpt_intake_v1` присутствует, но не интерпретирован как «это инференс, не user input».
3. [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) — `GPT_CLASSIFIER_POLICY_VERSION = "gpt.story_classifier.v1"`, `_persist_gpt_classifier_signals(...)` — три поля сохраняются под policy_version `gpt.story_classifier.v1`, что подтверждает классификатор-источник.
4. [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py) — `GptSignalsBlock` parsed from GPT payload; intake-валидация не проверяет, что пользователь произносил эти значения вслух.
5. [`GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../../../../../GPT UI/docs/audit-field-provenance-2026-05-24.md) §3.7 — `severity` и `impact_estimation` классифицированы как **GPT_INFERRED**; `problem_status` — **CONDITIONAL** (USER_DIRECT или GPT_INFERRED, distinction not preserved at wire level).

### Gap / Проблема
Раздел `gpt_signals` в `API_REFERENCE.md §6.3` оставляет впечатление, что эти три поля приходят от пользователя через GPT-каркас (как `narrative.title`/`description`). На деле — это машинные метки GPT-классификатора. Downstream аналитика на `story_signals` может ошибочно трактовать их как user-declared (REQ-44 §1 bullet 2–3).

### AC/DoD (REQ-44 §5)
- [ ] (P0) После строки `Persisted \`signals_json\` always includes ... HTTP \`202\` for the intake.` (`API_REFERENCE.md` L360) добавлен абзац **«Provenance note»** — формулировка из REQ-44 §3.3 «целевое состояние»:
  ```
  **Provenance note**: all three `gpt_signals` fields are GPT classifier outputs — they represent the GPT's inference from interview context, not values explicitly stated by the user. `severity` and `impact_estimation` are fully inferred; `problem_status` may reflect a direct user statement or GPT inference — the distinction is not preserved at the wire level. Downstream analytics on `story_signals` should treat these as `gpt_intake_v1` machine labels, not user-declared attributes.
  ```
  (AC-3).
- [ ] (P1) Таблица `gpt_signals` (severity / impact_estimation / problem_status) с enum-значениями — не меняется.
- [ ] (P1) Строка про `gpt_intake_v1` (`API_REFERENCE.md` L360) — не удаляется и не переписывается, новый абзац добавляется **под ней**.
- [ ] (P1) Source-строка (`contracts.py (GptSignalsBlock, ...)`, `services.py (...)` — L362) — не меняется.

### Где менять код
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) — §6.3, после L360.

### Out of scope
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) (REQ-44 §6).
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py), [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) (REQ-44 §6).
- `narrative.original_text` секция — отдельный T01.
- `GPT UI/instructions/**` (REQ-44 §6).
- `story_signals` schema / DB layer.

### Команды проверки
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
rg -n "Provenance note|GPT classifier outputs|machine labels" docs/runtime-docs/api-reference/API_REFERENCE.md

git diff -- docs/runtime-docs/api-reference/API_REFERENCE.md | rg -nE "^\+.*gpt_signals|classifier"
```
