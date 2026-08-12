# STORY-M2-02-10: API_REFERENCE field provenance clarity (REQ-44)

## Meta
- Key: `STORY-M2-02-10`
- Parent Epic: [`../../../EPIC-M2-02-story-intake-and-store.md`](../../../EPIC-M2-02-story-intake-and-store.md)
- Type: Documentation Story
- Status: Done (Awaiting Commits)
- Stream: M2 Intake / docs cascade
- Decision Ref: [`../../../../../requirements/44-api-reference-field-provenance-clarity.md`](../../../../../requirements/44-api-reference-field-provenance-clarity.md)
- Audit source: [`../../../../../../../GPT UI/docs/audit-field-provenance-2026-05-24.md`](../../../../../../../GPT%20UI/docs/audit-field-provenance-2026-05-24.md) — FINDING-01 (`narrative.original_text` = GPT_REFRAMED, not verbatim), FINDING-02 (`gpt_signals.*` = GPT classifier outputs)
- Depends on: STORY-M2-02-07 (REQ-33 multilingual narrative — Done), STORY-M2-02-08 (REQ-42 gpt_signals — Done)
- Cross-ref (not deliverable): REQ-22 §2 (GPT UI intentional design for `original_text`), REQ-42 (gpt_signals intake)
- Operative queue: [`../../../../gateway-active-packages/pkg-000024-20260525-req44-api-reference-field-provenance.yaml`](../../../../gateway-active-packages/pkg-000024-20260525-req44-api-reference-field-provenance.yaml)
- Skill declared: `python-pro` (docs-only; no Python edits)

## Story Goal
Закрыть два информационных зазора в [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6.3: явно отметить, что (1) `narrative.original_text` содержит GPT-переформулированное civic-описание, а не verbatim ввод пользователя; (2) три поля `gpt_signals` — это GPT classifier outputs, а не user-declared атрибуты. Никаких изменений в runtime / контрактах / OpenAPI.

## Product decisions (fixed)
- Изменения **только** в [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6.3 (REQ-44 §4); `openapi.yaml` не трогается (out of scope REQ-44 §6).
- Базовая семантика провенанса — из [`audit-field-provenance-2026-05-24.md`](../../../../../../../GPT%20UI/docs/audit-field-provenance-2026-05-24.md) §3.4 (`narrative.original_text` = **GPT_REFRAMED**) и §3.7 (gpt_signals classifier outputs).
- Ссылка на REQ-22 §2 как «intentional design» — обязательна в формулировке для `original_text` (REQ-44 §3.1).
- Сервер-сайд (`src/core/intake/contracts.py`, `src/core/application/services.py`, DB layer) **не** изменяется.

## Scope
- T01 — провенанс `narrative.original_text` в §6.3 (table cell + paragraph).
- T02 — провенанс `gpt_signals` (severity / impact_estimation / problem_status) в §6.3.
- Story acceptance gate — verification AC-1..AC-4 + regression check.

## Out of scope (REQ-44 §6)
- Изменения в [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py), [`src/core/application/services.py`](../../../../../../../src/core/application/services.py), любых Python-файлах.
- Изменения в [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml).
- Новое поле `verbatim_text` / raw capture (продуктовый backlog, R-03 из аудита).
- GPT UI instructions (`GPT UI/instructions/**` — scope REQ-28, REQ-29).
- Прочие секции `API_REFERENCE.md` (§1–5, §7+).

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-02-10-t01-api-reference-original-text-provenance-docs`](./task-m2-02-10-t01-api-reference-original-text-provenance-docs/README.md) | pkg-000024 |
| 2 | [`task-m2-02-10-t02-api-reference-gpt-signals-provenance-docs`](./task-m2-02-10-t02-api-reference-gpt-signals-provenance-docs/README.md) | pkg-000024 |

## AC / DoD (story level — REQ-44 §5)
- [ ] `API_REFERENCE.md §6.3` row `original_text` в narrative table содержит предупреждение «Not verbatim user input» с ссылкой на REQ-22 §2 (AC-1).
- [ ] `API_REFERENCE.md §6.3` содержит абзац, объясняющий что `original_text` = GPT-reframed `description[session_language]` (AC-2).
- [ ] `API_REFERENCE.md §6.3` секция `gpt_signals` содержит provenance note: «all three fields are GPT classifier outputs, not user-declared attributes» (AC-3).
- [ ] Остальные разделы [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) (§1–5, §7+) не затронуты — нет регрессий (AC-4).
- [ ] `python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify` → `ok 2 paths` (pkg-000024).
- [ ] Story gate: [`story-acceptance-gate-STORY-M2-02-10.md`](./story-acceptance-gate-STORY-M2-02-10.md) — PASS после P3.

## Verification command (story-level)
```bash
cd /Users/eslinko/Development/DOGEstonia
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify

git -C doge-complaints-gateway diff -- docs/runtime-docs/api-reference/API_REFERENCE.md | rg -n "verbatim|provenance|GPT classifier"
```
