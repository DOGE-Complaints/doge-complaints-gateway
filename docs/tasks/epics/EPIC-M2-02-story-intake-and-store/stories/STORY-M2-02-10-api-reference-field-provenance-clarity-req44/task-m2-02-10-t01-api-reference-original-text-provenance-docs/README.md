## Task workspace — `task-m2-02-10-t01-api-reference-original-text-provenance-docs`

- Story: [`../STORY-M2-02-10-api-reference-field-provenance-clarity-req44.md`](../STORY-M2-02-10-api-reference-field-provenance-clarity-req44.md)
- Decision Ref: [`../../../../../../requirements/44-api-reference-field-provenance-clarity.md`](../../../../../../requirements/44-api-reference-field-provenance-clarity.md) §3.1, §3.2
- Audit Ref: [`../../../../../../../../GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../../../../../GPT%20UI/docs/audit-field-provenance-2026-05-24.md) §3.4 — FINDING-01

---
**Приоритет:** P3
**Сложность:** S
**Статус:** todo
**Wave:** `pkg-000024`
---

## Task: docs — API_REFERENCE §6.3 `original_text` provenance (table cell + paragraph)

### Цель
Сделать явным, что `narrative.original_text` хранит **GPT-переформулированное** civic-описание на языке сессии, а **не дословный** ввод пользователя. Две локальные правки в `API_REFERENCE.md §6.3`, без изменения кода и контрактов.

### Факты из кода
1. [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L276 — текущая строка narrative table:
   ```
   | `original_text` | string | **yes** | Non-empty after `.strip()` | stored as-is (stripped) |
   ```
   Колонка Normalization не упоминает GPT-reframing.
2. [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L287 — единственный пояснительный абзац под narrative table говорит только про `language` vs `session_language`; нет уточнения семантики `original_text`.
3. [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L299 — Source строка после блока: `contracts.py:30-40`, `narrative_i18n.py`, `parse_story_intake_request:135-196`. Эти источники подтверждают, что валидация intake просто `.strip()`, но **не доказывают** verbatim-семантику для оператора, читающего БД.
4. [`GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../../../../../GPT%20UI/docs/audit-field-provenance-2026-05-24.md) §3.4 — `narrative.original_text` классифицирован как **GPT_REFRAMED**, источник = `canonical_payload.description[session_language]`; явный ⚠ flag «поле называется `original_text`, но содержит НЕ дословные слова пользователя».
5. [`doge-complaints-gateway/docs/requirements/22-m2-demo-story-intake-interview-ssot-v1.md`](../../../../../../requirements/22-m2-demo-story-intake-interview-ssot-v1.md) §2 — intentional design: verbatim capture out of scope demo M2.

### Gap / Проблема
В `API_REFERENCE.md §6.3` нет ни единого упоминания, что `original_text` — это civic-restatement от GPT. Операторы / интеграторы / downstream-аналитика читают «original text» как verbatim user input и могут принимать на этом ошибочные решения (правовые/надзорные контексты — REQ-44 §1 bullet 3).

### AC/DoD (REQ-44 §5)
- [ ] (P0) В таблице narrative (`API_REFERENCE.md` L276) колонка Normalization для `original_text` заменена на:
  ```
  stored as-is (stripped). **Not verbatim user input** — contains GPT-reframed description in `session_language` (REQ-22 §2 intentional design; verbatim capture is out of scope).
  ```
  (REQ-44 §3.1, AC-1).
- [ ] (P0) Под существующим абзацем «`language` vs `session_language`» (`API_REFERENCE.md` L287) добавлен второй абзац **«`original_text` provenance»** — формулировка из REQ-44 §3.2 «целевое состояние» (AC-2).
- [ ] (P1) Тип `original_text` в таблице остался `string`, required `**yes**`, validation `Non-empty after \`.strip()\`` — не меняется.
- [ ] (P1) Прочие строки narrative table (`language`, `session_language`, `title`, `description`, `summary`, `institution`, `location_query`, `canonical_type`, `canonical_labels`) — не модифицированы.

### Где менять код
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) — §6.3 (две локальные правки: L276 и после L287).

### Out of scope
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) (REQ-44 §6).
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py) (REQ-44 §6).
- `gpt_signals` секция — отдельный T02.
- `GPT UI/instructions/**` (REQ-44 §6).

### Команды проверки
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
rg -n "Not verbatim user input|original_text\` provenance|GPT-reframed description" docs/runtime-docs/api-reference/API_REFERENCE.md

git diff -- docs/runtime-docs/api-reference/API_REFERENCE.md | rg -nE "^\+.*original_text|verbatim"
```
