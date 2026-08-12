# Acceptance verification — TASK-M2-02-10-T02

- **Task:** docs — API_REFERENCE §6.3 `gpt_signals` provenance note
- **Result:** PASS
- **Date:** 2026-05-25
- **Decision Ref:** [`../../../../../../requirements/44-api-reference-field-provenance-clarity.md`](../../../../../../requirements/44-api-reference-field-provenance-clarity.md) §3.3, §5 (AC-3)
- **Wave:** `pkg-000024-20260525-req44-api-reference-field-provenance.yaml`

## AC table

| AC | Уровень | Формулировка (REQ-44 §5) | Реализация | Статус |
|----|---------|---------------------------|------------|--------|
| AC-3 | P0 | §6.3 `gpt_signals` содержит provenance note: «all three fields are GPT classifier outputs, not user-declared attributes» | [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L364 — добавлен абзац **«Provenance note»** с формулировкой REQ-44 §3.3 («GPT classifier outputs — they represent the GPT's inference ...; `severity` and `impact_estimation` are fully inferred; `problem_status` may reflect a direct user statement or GPT inference ...; machine labels, not user-declared attributes») | PASS |
| AC-инвариант | P1 | Таблица `gpt_signals` (severity / impact_estimation / problem_status enum-значения) не меняется | Diff не показывает изменения L358–360 (таблица) | PASS |
| AC-инвариант | P1 | Строка про `gpt_intake_v1` (бывш. L360, теперь L362) не удаляется, новый абзац — **под ней** | L362 сохранена (`Persisted \`signals_json\` always includes ...`); L364 — новый абзац | PASS |
| AC-инвариант | P1 | Source-строка (`contracts.py (GptSignalsBlock, ...)`, `services.py (...)`) не меняется | L366 сохранена | PASS |
| AC-инвариант | P1 | Out of scope (REQ-44 §6): `openapi.yaml`, `contracts.py`, `services.py`, `GPT UI/**`, `story_signals` schema/DB | `git diff HEAD --stat` — мои правки T02 затрагивают **только** `API_REFERENCE.md` | PASS |

## Verification commands

### 1. AC-3 — provenance note
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
grep -nE "Provenance note|GPT classifier outputs|machine labels" docs/runtime-docs/api-reference/API_REFERENCE.md
# expected: L364 содержит «Provenance note», «GPT classifier outputs», «machine labels»
```
Результат:
```
364:**Provenance note**: all three `gpt_signals` fields are GPT classifier outputs — they represent the GPT's inference from interview context, not values explicitly stated by the user. `severity` and `impact_estimation` are fully inferred; `problem_status` may reflect a direct user statement or GPT inference — the distinction is not preserved at the wire level. Downstream analytics on `story_signals` should treat these as `gpt_intake_v1` machine labels, not user-declared attributes.
```

### 2. Scope check (T02 не задевает out-of-scope)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
git diff HEAD -- docs/runtime-docs/api-reference/API_REFERENCE.md | grep -nE "^\+.*(Provenance note|classifier outputs|machine labels)"
# expected: единственная новая строка T02
```
Результат:
```
101:+**Provenance note**: all three `gpt_signals` fields are GPT classifier outputs — they represent the GPT's inference from interview context, not values explicitly stated by the user. `severity` and `impact_estimation` are fully inferred; `problem_status` may reflect a direct user statement or GPT inference — the distinction is not preserved at the wire level. Downstream analytics on `story_signals` should treat these as `gpt_intake_v1` machine labels, not user-declared attributes.
```

### 3. Source-строка и таблица не задеты
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
grep -nE "^Source: \`contracts.py\` \(\`GptSignalsBlock\`" docs/runtime-docs/api-reference/API_REFERENCE.md
grep -nE "severity.*LOW.*MEDIUM.*HIGH.*CRITICAL" docs/runtime-docs/api-reference/API_REFERENCE.md
# expected: обе строки на своих местах, не модифицированы
```

## Code facts (claims из кода)

1. [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) L69 — `GPT_CLASSIFIER_POLICY_VERSION = "gpt.story_classifier.v1"` (machine-label, не user-declared).
2. [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) L93–109 — `_persist_gpt_classifier_signals(...)` сохраняет три поля под policy_version `gpt.story_classifier.v1` (classifier-source).
3. [`GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../../../../../GPT UI/docs/audit-field-provenance-2026-05-24.md) §3.7 — `severity` / `impact_estimation` классифицированы как **GPT_INFERRED**; `problem_status` — **CONDITIONAL** (USER_DIRECT или GPT_INFERRED, wire-level distinction отсутствует).

Эти три факта точно отражены в новом абзаце «Provenance note» (REQ-44 §3.3).

## Out of scope (REQ-44 §6) — подтверждение неизменения

- `docs/runtime-docs/api-reference/openapi.yaml` — T02 правок нет.
- `src/core/intake/contracts.py`, `src/core/application/services.py` — T02 правок нет.
- `GPT UI/**` — нет изменений.
- `story_signals` schema / DB layer — нет изменений.

## Outcome

T02 закрыта: AC-3 (REQ-44 §5) — PASS; инварианты (таблица enum, Source-строка, out-of-scope файлы) соблюдены.
