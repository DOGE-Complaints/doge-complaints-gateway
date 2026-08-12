# task-gw-draft-02-t05-story-draft-submit-contract-tests

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000044
- **Skill declared:** python-pro
- **Depends on:** T04

## Purpose
Контракт-тесты (unit): verified→202+`submitter=sub`; `phone_verified=false`→403+`verify_url`; нет/битый токен→401; identity down→503; повтор `draft_id`→идемпотентно; unknown draft→404.

## Code Facts
- Draft-01 test pattern — [`tests/test_gw_draft_01_story_draft_stash_contract.py`](../../../../../../../tests/test_gw_draft_01_story_draft_stash_contract.py)
- GAUTH gate tests — `tests/test_gw_gauth_03_*` (403 verify_url pattern)

## Acceptance / DoD
- Traces all 6 parent AC via contract tests
- New file `tests/test_gw_draft_02_story_draft_submit_contract.py`
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `tests/test_gw_draft_02_story_draft_submit_contract.py` (new)

## Out of scope
Story gate doc (T07); runtime docs (T06)

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_02_story_draft_submit_contract.py
```
