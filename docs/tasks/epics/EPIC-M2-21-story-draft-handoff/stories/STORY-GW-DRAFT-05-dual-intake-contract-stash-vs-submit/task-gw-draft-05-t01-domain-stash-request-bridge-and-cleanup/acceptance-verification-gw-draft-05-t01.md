# Acceptance verification — task-gw-draft-05-t01-domain-stash-request-bridge-and-cleanup

- **Task:** T01 domain stash request + bridge + cleanup
- **Status:** PASS
- **Date:** 2026-07-11T07:52:43Z

## Checklist

- [x] `StoryDraftStashRequest` + `intake_request_from_stash_and_submitter` in contracts
- [x] `STASH_PENDING_EXTERNAL_USER_ID` / `require_submitter` removed from intake package
- [x] `parse_story_draft_stash_request` → `StoryDraftStashRequest`

## Evidence

```
cd doge-complaints-gateway && rg 'STASH_PENDING|require_submitter' src/core/intake/ || test $? -eq 1 → ok
python3 -m pytest -q tests/test_story_intake_contract.py::test_parse_story_draft_stash_request_omits_submitter → pass
```
