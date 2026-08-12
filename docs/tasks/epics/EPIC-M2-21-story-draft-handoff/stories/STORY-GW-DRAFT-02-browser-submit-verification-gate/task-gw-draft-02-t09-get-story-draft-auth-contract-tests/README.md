# task-gw-draft-02-t09-get-story-draft-auth-contract-tests

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000044)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_02_audit_followup`)
- **Depends on:** T08
- **Audit ref:** [`audit-gw-draft-02-browser-submit-verification-gate-2026-07-03`](../../../../../../analysis/audit-gw-draft-02-browser-submit-verification-gate-2026-07-03.md) **G1**

## Purpose
Контракт-тесты GET auth: закрыть G1 evidence — без Bearer нельзя читать черновик; active session → 200; fail-closed 401/503.

## Code Facts
- Existing GET tests без auth — [`test_gw_draft_01_story_draft_stash_contract.py:88-104`](../../../../../../../tests/test_gw_draft_01_story_draft_stash_contract.py) `test_get_story_drafts_returns_saved_payload` (no Bearer today)
- Submit contract pattern — [`test_gw_draft_02_story_draft_submit_contract.py`](../../../../../../../tests/test_gw_draft_02_story_draft_submit_contract.py) (`_patch_fetch_me`, `_browser_headers`)
- P6 choice: extend draft-01 file **or** new `test_gw_draft_02_get_auth_contract.py` (document choice in acceptance)

## Acceptance / DoD
- GET без Bearer → **401**
- Inactive `/me` (`active=false`) → **401**
- Identity `/me` down → **503**
- Valid active session → **200** (existing happy-path updated to send Bearer)
- **No** 403 `verification_required` on GET (unverified `phone_verified=false` still → **200** if session active)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`tests/test_gw_draft_01_story_draft_stash_contract.py`](../../../../../../../tests/test_gw_draft_01_story_draft_stash_contract.py) and/or new `tests/test_gw_draft_02_get_auth_contract.py`

## Out of scope
Implementation (T08); runtime docs (T10); submit contract tests (`test_gw_draft_02_story_draft_submit_contract.py`)

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py
# and/or:
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_02_get_auth_contract.py
```
