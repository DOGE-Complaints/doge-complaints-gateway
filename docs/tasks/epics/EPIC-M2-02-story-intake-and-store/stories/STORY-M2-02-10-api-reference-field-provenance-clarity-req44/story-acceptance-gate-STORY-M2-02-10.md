# Story acceptance gate — STORY-M2-02-10

- **Story:** API_REFERENCE field provenance clarity (REQ-44)
- **Package:** `pkg-000024-20260525-req44-api-reference-field-provenance.yaml`
- **Result:** PASS
- **Date:** 2026-05-25 (P3)

## AC checklist (REQ-44 §5)

| AC | Status | Evidence |
|----|--------|----------|
| AC-1: `original_text` row Normalization содержит «Not verbatim user input» + REQ-22 §2 | PASS | T01 — `API_REFERENCE.md` L276 содержит маркер и ссылку на REQ-22 §2; см. [`task-m2-02-10-t01-.../acceptance-verification-m2-02-10-t01.md`](./task-m2-02-10-t01-api-reference-original-text-provenance-docs/acceptance-verification-m2-02-10-t01.md) |
| AC-2: §6.3 содержит абзац «`original_text` provenance» (GPT-reframed `description[session_language]`) | PASS | T01 — `API_REFERENCE.md` L289 содержит абзац с формулировкой REQ-44 §3.2; ссылка на `canonical_payload.description[session_language]` |
| AC-3: §6.3 `gpt_signals` содержит «Provenance note: all three ... GPT classifier outputs» | PASS | T02 — `API_REFERENCE.md` L364 содержит абзац с формулировкой REQ-44 §3.3; см. [`task-m2-02-10-t02-.../acceptance-verification-m2-02-10-t02.md`](./task-m2-02-10-t02-api-reference-gpt-signals-provenance-docs/acceptance-verification-m2-02-10-t02.md) |
| AC-4: остальные секции `API_REFERENCE.md` (§1–5, §7+) не затронуты — нет регрессий | PASS | `git diff HEAD -- API_REFERENCE.md` показывает 2 хунка от T01/T02 в §6.3 narrative+gpt_signals (`@@ -241,6 +286,8 @@`, `@@ -314,6 +361,8 @@`); прочие хунки (L24, L48, L110, L228, L553, L562) — pre-existing diff от незакоммиченных wave REQ-37…REQ-43 («Done (Awaiting Commits)»), к STORY-M2-02-10 не относятся |

## Verification commands

### 1. Queue verify (immutable pkg-000024)
```bash
cd /Users/eslinko/Development/DOGEstonia
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
# expected: ok 2 paths
```

### 2. AC-1..AC-3 — содержимое §6.3
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
rg -n "Not verbatim user input|original_text\` provenance|Provenance note|GPT classifier outputs" \
   docs/runtime-docs/api-reference/API_REFERENCE.md
```

### 3. AC-4 — regression scope (правки только в §6.3)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
git diff -- docs/runtime-docs/api-reference/API_REFERENCE.md | head -100

# Список изменённых строк должен лежать между разделом §6.3 (narrative + gpt_signals)
# и не задевать §1..§5, §7+. Никаких изменений в openapi.yaml, contracts.py, services.py.
git diff --stat -- docs/runtime-docs/api-reference/openapi.yaml \
                   src/core/intake/contracts.py \
                   src/core/application/services.py
# expected: empty
```

### 4. Runtime sanity (docs-only, не должно ломать тесты)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest -q tests/test_openapi_runtime_compliance.py
# expected: no regression — openapi.yaml не менялся
```
Результат (2026-05-25 P3): `2 passed in 0.05s`.

## Outcome

**STORY-M2-02-10 PASS** — все AC (1..4) подтверждены; runtime-тесты openapi compliance не сломаны; immutable `pkg-000024` без изменений; out-of-scope зоны (`openapi.yaml`, `contracts.py`, `services.py`, `GPT UI/**`) не задеты T01/T02.

## Cross-references

- Requirement: [`../../../../../requirements/44-api-reference-field-provenance-clarity.md`](../../../../../requirements/44-api-reference-field-provenance-clarity.md)
- Audit: [`../../../../../../../GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../../../../GPT%20UI/docs/audit-field-provenance-2026-05-24.md) §3.4, §3.7
- Parent decisions: REQ-22 §2 (intentional design `original_text`), REQ-42 (`gpt_signals` intake)
- Operative queue: [`../../../../gateway-active-packages/pkg-000024-20260525-req44-api-reference-field-provenance.yaml`](../../../../gateway-active-packages/pkg-000024-20260525-req44-api-reference-field-provenance.yaml)
