# BULLRUN Phase Log — TASK-M2-02-10-T01

- [x] Phase 0 — Analysis: factы README сверены с `API_REFERENCE.md` L276 (table cell) и L287 (`language` vs `session_language` paragraph); подтверждено отсутствие маркеров verbatim/provenance до правки. `src/core/intake/contracts.py:30-40` — `Narrative.original_text: str` без verbatim/raw-wrapper.
- [x] Phase 1 — Implement: 2 локальные правки в `docs/runtime-docs/api-reference/API_REFERENCE.md`:
  - L276 — расширена колонка Normalization для `original_text` (REQ-44 §3.1).
  - После L287 — вставлен новый абзац **`original_text` provenance** (REQ-44 §3.2).
- [x] Phase 2 — Verify: `grep` подтверждает строки 276 + 289; `git diff HEAD -- API_REFERENCE.md` показывает обе правки внутри §6.3, без затрагивания других секций; `openapi.yaml`, `contracts.py`, `services.py` — мной не изменялись (пред-существующие diff относятся к незакоммиченным wave REQ-37…REQ-43, статус «Done (Awaiting Commits)» в bullrun-launch-index).
