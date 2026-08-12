# Acceptance verification — task-gw-draft-05-t04-contract-and-draft-regression-tests

- **Task:** T04 contract and draft regression tests
- **Status:** PASS
- **Date:** 2026-07-11T07:52:43Z

## Checklist

- [x] No assert on `STASH_PENDING_EXTERNAL_USER_ID`; GW-DRAFT-01/02 + intake contract green
- [x] Stash tests use payload without submitter; submit tests verify authoritative author from introspection
- [x] `pytest -q -m "not live_integration"` green

## Evidence

```
cd doge-complaints-gateway && rg 'STASH_PENDING|__stash_pending' tests/ || test $? -eq 1 → ok
python3 -m pytest -q tests/test_story_intake_contract.py tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py tests/test_gw_draft_02_get_auth_contract.py → 42 passed
python3 -m pytest -q -m "not live_integration" → 569 passed, 12 skipped
```
