# Acceptance verification — TASK-M2-02-10-T01

- **Task:** docs — API_REFERENCE §6.3 `original_text` provenance (table cell + paragraph)
- **Result:** PASS
- **Date:** 2026-05-25
- **Decision Ref:** [`../../../../../../requirements/44-api-reference-field-provenance-clarity.md`](../../../../../../requirements/44-api-reference-field-provenance-clarity.md) §3.1, §3.2, §5 (AC-1, AC-2)
- **Wave:** `pkg-000024-20260525-req44-api-reference-field-provenance.yaml`

## AC table

| AC | Уровень | Формулировка (REQ-44 §5) | Реализация | Статус |
|----|---------|---------------------------|------------|--------|
| AC-1 | P0 | `original_text` row в narrative table содержит «Not verbatim user input» + REQ-22 §2 | [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L276 — колонка Normalization дополнена: `stored as-is (stripped). **Not verbatim user input** — contains GPT-reframed description in \`session_language\` (REQ-22 §2 intentional design; verbatim capture is out of scope).` | PASS |
| AC-2 | P0 | §6.3 содержит абзац, объясняющий что `original_text` = GPT-reframed `description[session_language]` | [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L289 — добавлен абзац **`original_text` provenance** с формулировкой из REQ-44 §3.2: "GPT-reframed civic description in `session_language` (the `canonical_payload.description[session_language]` produced by the GPT normalizer), not the verbatim words the user spoke" | PASS |
| AC-инвариант | P1 | Тип `original_text` остаётся `string`, required `**yes**`, validation `Non-empty after .strip()` | L276 — поля Type / Required / Validation не изменены | PASS |
| AC-инвариант | P1 | Прочие строки narrative table (L277–L285) не модифицированы | Diff показывает изменение только в L276 + новый абзац L289; строки `language`, `session_language`, `title`, `description`, `summary`, `institution`, `location_query`, `canonical_type`, `canonical_labels` не тронуты | PASS |
| AC-инвариант | P1 | Out of scope (REQ-44 §6): `openapi.yaml`, `contracts.py`, `services.py`, `GPT UI/**` | `git diff HEAD --stat` не показывает мoих правок в этих файлах (pre-existing diff от незакоммиченных wave REQ-37…REQ-43 — не часть T01) | PASS |

## Verification commands

### 1. AC-1 — table cell warning
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
grep -n "Not verbatim user input" docs/runtime-docs/api-reference/API_REFERENCE.md
# expected: L276 содержит «Not verbatim user input» + «GPT-reframed description» + «REQ-22 §2»
```
Результат:
```
276:| `original_text` | string | **yes** | Non-empty after `.strip()` | stored as-is (stripped). **Not verbatim user input** — contains GPT-reframed description in `session_language` (REQ-22 §2 intentional design; verbatim capture is out of scope). |
```

### 2. AC-2 — provenance paragraph
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
grep -nE "original_text\` provenance|GPT-reframed civic description" docs/runtime-docs/api-reference/API_REFERENCE.md
# expected: новый абзац с формулировкой §3.2
```
Результат:
```
289:**`original_text` provenance**: this field contains the GPT-reframed civic description in `session_language` (the `canonical_payload.description[session_language]` produced by the GPT normalizer), not the verbatim words the user spoke. This is intentional per REQ-22 §2. Operators reading this field from the database should treat it as a structured civic restatement, not a literal quote.
```

### 3. Scope check (T01 не задевает out-of-scope)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
git diff HEAD -- docs/runtime-docs/api-reference/API_REFERENCE.md | grep -nE "^\+.*(verbatim|original_text\` provenance|GPT-reframed)"
# expected: только две новые строки T01
```
Результат:
```
84:+| `original_text` | string | **yes** | Non-empty after `.strip()` | stored as-is (stripped). **Not verbatim user input** — contains GPT-reframed description in `session_language` (REQ-22 §2 intentional design; verbatim capture is out of scope). |
92:+**`original_text` provenance**: this field contains the GPT-reframed civic description in `session_language` (the `canonical_payload.description[session_language]` produced by the GPT normalizer), not the verbatim words the user spoke. This is intentional per REQ-22 §2. Operators reading this field from the database should treat it as a structured civic restatement, not a literal quote.
```

## Out of scope (REQ-44 §6) — подтверждение неизменения

- `docs/runtime-docs/api-reference/openapi.yaml` — pre-existing diff от REQ-37…REQ-43, T01 правки **не внесены**.
- `src/core/intake/contracts.py`, `src/core/application/services.py` — нет diff от T01.
- `GPT UI/**` — нет изменений (Python/код или инструкции).

## Outcome

T01 закрыта: оба AC (AC-1, AC-2 из REQ-44 §5) — PASS; out-of-scope инварианты соблюдены; pre-existing diff от незакоммиченных wave не относится к T01.
