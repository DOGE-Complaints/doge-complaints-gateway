# BULLRUN Phase Log — TASK-M2-02-07-T01

## Phase 1–3 — Implementation
- [x] `INTAKE_SCHEMA_VERSION` → `m2.story_intake_envelope.v2`
- [x] `Narrative`: `title`, `description`, `session_language`, optional `summary` (dict)
- [x] Reject v1 with explicit migrate message; `identity_issuer` required
- [x] `core/domain/narrative_i18n.py` — shared i18n parse helpers

## Phase 4 — Verification
- [x] `pytest tests/test_story_intake_contract.py -q`
