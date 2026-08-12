# task-gw-draft-05-t09-audit-g1-honest-legacy-placeholder-ac

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000049)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_05_audit_followup`)
- **Depends on:** T01–T07 (P3 Done)
- **Audit ref:** [`audit-gw-draft-05-dual-intake-contract-stash-vs-submit-2026-07-11`](../../../../../../analysis/audit-gw-draft-05-dual-intake-contract-stash-vs-submit-2026-07-11.md) **G1**

## Purpose
Закрыть audit **G1 (MEDIUM):** убрать gate-gaming `"".join(("__stash_", "pending_author__"))` в [`contracts.py:18-20`](../../../../../../../src/core/intake/contracts.py); заменить на честный литерал legacy-константы с комментарием «tolerant-read strip only». Синхронизировать AC1 / story gate grep с реальным состоянием: нет **активного** placeholder-контракта; legacy value допустим только в `_normalize_stored_draft_payload`. Добавить unit test tolerant-read legacy payload.

## Code Facts
- Obfuscated placeholder — [`contracts.py:18-20`](../../../../../../../src/core/intake/contracts.py) `_LEGACY_STASH_PLACEHOLDER_EXTERNAL_USER_ID = "".join(...)`
- Tolerant read — [`contracts.py:445`](../../../../../../../src/core/intake/contracts.py) `_normalize_stored_draft_payload`; [`parse_stored_draft_stash_request`](../../../../../../../src/core/intake/contracts.py)
- T02 decision — [`backward-compat-decision-gw-draft-05-t02.md`](../task-gw-draft-05-t02-handlers-stash-submit-intake-wiring/backward-compat-decision-gw-draft-05-t02.md) tolerant read on submit
- Gate drift — [`story-acceptance-gate-STORY-GW-DRAFT-05.md`](../task-gw-draft-05-t08-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-05.md) AC1 row still implies full literal removal via grep

## Acceptance / DoD
- [x] Traces audit G1: `_LEGACY_STASH_PLACEHOLDER_EXTERNAL_USER_ID` — явный литерал `"__stash_pending_author__"` (не `"".join`)
- [x] `rg 'STASH_PENDING|require_submitter|\bstash_pending\b' src/ tests/` = 0 (active paths; legacy value in constant excluded)
- [x] Legacy literal appears **only** in `_LEGACY_STASH_PLACEHOLDER_EXTERNAL_USER_ID` + `_normalize_stored_draft_payload` (documented in AC1 / gate)
- [x] Unit test: `parse_stored_draft_stash_request` strips legacy placeholder submitter and returns `StoryDraftStashRequest`
- [x] AC1 revised in backlog, pipeline story, T08 gate/README (honest grep criteria)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-05-t09.md`](./acceptance-verification-gw-draft-05-t09.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/src/core/intake/contracts.py`
- `doge-complaints-gateway/tests/test_story_intake_contract.py` (or adjacent contract test)
- `doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md` — AC1
- `doge-complaints-gateway/docs/tasks/epics/.../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md` — AC1
- `doge-complaints-gateway/docs/tasks/epics/.../task-gw-draft-05-t08-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-05.md`
- `doge-complaints-gateway/docs/tasks/epics/.../task-gw-draft-05-t08-story-acceptance-gate/README.md`

## Out of scope
- G2 double-parse round-trip on submit (`activation: none`)
- Hosted smoke (T08 gate)
- GW-DRAFT-06 legacy route removal

## Verification commands
```bash
cd doge-complaints-gateway && rg 'STASH_PENDING|require_submitter|\bstash_pending\b' src/ tests/ || test $? -eq 1
cd doge-complaints-gateway && rg '__stash_pending_author__' src/core/intake/contracts.py
# expect 1–2 hits: constant + _normalize compare only
cd doge-complaints-gateway && python3 -m pytest -q tests/test_story_intake_contract.py -k legacy
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```
