# task-gw-draft-05-t04-contract-and-draft-regression-tests

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000049
- **Skill declared:** python-pro
- **Depends on:** T01–T03

## Purpose
Backlog T04: update intake contract and GW-DRAFT-01/02 regression tests — remove magic placeholder asserts; assert `StoryDraftStashRequest` stash path; submit bridge with `/me`.

## Code Facts
- Placeholder assert — [`test_story_intake_contract.py:9,49`](../../../../../../../../tests/test_story_intake_contract.py)
- Draft stash contract — [`test_gw_draft_01_story_draft_stash_contract.py`](../../../../../../../../tests/test_gw_draft_01_story_draft_stash_contract.py)
- Draft submit contract — [`test_gw_draft_02_story_draft_submit_contract.py`](../../../../../../../../tests/test_gw_draft_02_story_draft_submit_contract.py)
- PUBLIC-01 contrast (unchanged scope) — [`test_gw_public_01_public_issues_regression.py`](../../../../../../../../tests/test_gw_public_01_public_issues_regression.py)

## Acceptance / DoD
- [ ] Traces parent AC #6: no assert on `STASH_PENDING_EXTERNAL_USER_ID`; GW-DRAFT-01/02 + intake contract green
- [ ] Stash tests use payload without submitter; submit tests verify authoritative author from introspection
- [ ] `pytest -q -m "not live_integration"` green
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-05-t04.md`](./acceptance-verification-gw-draft-05-t04.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/tests/test_story_intake_contract.py`
- `doge-complaints-gateway/tests/test_gw_draft_01_story_draft_stash_contract.py`
- `doge-complaints-gateway/tests/test_gw_draft_02_story_draft_submit_contract.py`

## Out of scope
- OpenAPI/docs (T05–T06); `POST /intake/stories` removal → GW-DRAFT-06

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_story_intake_contract.py tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py
cd doge-complaints-gateway && rg 'STASH_PENDING|__stash_pending' tests/ || test $? -eq 1
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```
