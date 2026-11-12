# Run summary — REQ-44 API_REFERENCE field provenance clarity (Gateway Builder)

- **Story:** STORY-M2-02-10
- **Package:** `pkg-000024-20260525-req44-api-reference-field-provenance.yaml` (2 tasks T01, T02)
- **Build window:** `gateway-cursor-build-window--STORY-M2-02-10.md`
- **Decision ref:** [`docs/requirements/44-api-reference-field-provenance-clarity.md`](../../requirements/44-api-reference-field-provenance-clarity.md)
- **Audit source:** [`GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../GPT%20UI/docs/audit-field-provenance-2026-05-24.md) — FINDING-01, FINDING-02
- **Status:** Story gate PASS — Done (Awaiting Commits)
- **Date:** 2026-05-25
- **Type:** documentation-only (no runtime/contracts/openapi change)
- **gateway_input_package:** `doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000024-20260525-req44-api-reference-field-provenance.yaml`
- **source_mode:** `explicit_package`

## Tasks closed

| Task | AC (REQ-44 §5) | Outcome |
|------|----------------|---------|
| T01 | AC-1 + AC-2 | [`API_REFERENCE.md`](../../runtime-docs/api-reference/API_REFERENCE.md) §6.3 — L276 (table cell `original_text` Normalization дополнена «Not verbatim user input» + REQ-22 §2); L289 (новый абзац `original_text` provenance — GPT-reframed `description[session_language]`) |
| T02 | AC-3 | [`API_REFERENCE.md`](../../runtime-docs/api-reference/API_REFERENCE.md) §6.3 — L364 (новый абзац `Provenance note`: все три `gpt_signals` — GPT classifier outputs, не user-declared; машинные метки `gpt_intake_v1`) |

## AC summary (REQ-44 §5)

- AC-1: PASS — `original_text` row warning + REQ-22 §2 cross-ref.
- AC-2: PASS — `original_text` provenance paragraph (GPT-reframed `description[session_language]`).
- AC-3: PASS — `gpt_signals` provenance note (GPT classifier outputs).
- AC-4: PASS — `git diff HEAD -- API_REFERENCE.md` показывает T01/T02 хунки только в §6.3 (`@@ -241,6 +286,8 @@`, `@@ -314,6 +361,8 @@`); прочие хунки — pre-existing diff от незакоммиченных wave REQ-37…REQ-43, не относятся к T01/T02.

## Test evidence

- `python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify` → **ok 2 paths** (from workspace root, step 0 before P3).
- `cd doge-complaints-gateway && python3 -m pytest -q tests/test_openapi_runtime_compliance.py` → **2 passed in 0.05s** (openapi.yaml не менялся T01/T02 → compliance не сломан).
- `grep -n "Not verbatim user input|original_text\` provenance|Provenance note|GPT classifier outputs"` → 4 матча в `API_REFERENCE.md` (L276, L289, L364 — две темы провенанса).

## Code facts (claims из кода)

- [`src/core/intake/contracts.py`](../../../src/core/intake/contracts.py) L31 — `Narrative.original_text: str` (без verbatim/raw маркера) → подтверждает, что field хранит только то, что GPT передал в payload.
- [`src/core/application/services.py`](../../../src/core/application/services.py) L69 — `GPT_CLASSIFIER_POLICY_VERSION = "gpt.story_classifier.v1"`, L93 `_persist_gpt_classifier_signals` → подтверждает classifier-source `gpt_signals`.
- [`GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../GPT%20UI/docs/audit-field-provenance-2026-05-24.md) §3.4 (`original_text` = **GPT_REFRAMED**) и §3.7 (`gpt_signals` = **GPT_INFERRED** / **CONDITIONAL**).

## Out of scope (REQ-44 §6) — подтверждение неизменения

- `docs/runtime-docs/api-reference/openapi.yaml` — pre-existing diff от REQ-37…REQ-43, REQ-44 правок нет.
- `src/core/intake/contracts.py`, `src/core/application/services.py`, любые Python-файлы — REQ-44 правок нет.
- Новое поле `verbatim_text` / raw capture — продуктовый backlog (audit R-03).
- `GPT UI/instructions/**` — out of scope (REQ-28, REQ-29).
- Прочие секции `API_REFERENCE.md` (§1–5, §7+) — не задеты T01/T02.

## Immutable preserved

- `pkg-000024-20260525-req44-api-reference-field-provenance.yaml` — без изменений после P1 создания.
- `gateway-active-package.current.yaml` — указатель `package_file:` на pkg-000024 (P1 переключение).
- pkg-000023 (REQ-43) и старше — immutable history, не задеты.

## Next operator steps

- P4 (optional) — full audit по REQ-44 §5 (если оператор инициирует Claude clause audit).
- P8 — commits per [`docs/methodology/git-commit.md`](../../../../docs/methodology/git-commit.md): API_REFERENCE.md правки + task artifacts (BULLRUN-PHASE-LOG, acceptance-verification, story gate, run-summary); push только по явному разрешению.
- Опционально cross-team coordination (REQ-22 §2 GPT UI design intentional — справочная связка).
