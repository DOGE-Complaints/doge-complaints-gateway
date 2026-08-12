# BULLRUN Phase Log — TASK-M2-02-10-T02

- [x] Phase 0 — Analysis: `API_REFERENCE.md` §6.3 `gpt_signals` секция (L350–362 после T01-смещения) подтверждена; маркер `gpt_intake_v1` присутствует, но семантика «classifier outputs vs user-declared» не объяснена. `src/core/application/services.py:69` — `GPT_CLASSIFIER_POLICY_VERSION = "gpt.story_classifier.v1"`; `services.py:93` — `_persist_gpt_classifier_signals` — подтверждает machine-label источник.
- [x] Phase 1 — Implement: 1 локальная правка в `docs/runtime-docs/api-reference/API_REFERENCE.md` §6.3 — добавлен абзац **«Provenance note»** между строкой `gpt_intake_v1` и Source-строкой (REQ-44 §3.3).
- [x] Phase 2 — Verify: `grep` подтверждает строку 364; `git diff HEAD -- API_REFERENCE.md` — единственная новая `+` строка с «Provenance note ... GPT classifier outputs»; `openapi.yaml`, `services.py`, `contracts.py` — T02 правками не задеты; таблица `gpt_signals` (severity/impact_estimation/problem_status) и Source-строка не изменены.
