# Acceptance verification — task-gw-draft-05-t02-handlers-stash-submit-intake-wiring

- **Task:** T02 handlers stash/submit/intake wiring
- **Status:** PASS
- **Date:** 2026-07-11T07:52:43Z

## Checklist

- [x] Backward-compat decision artifact signed before handler code
- [x] `handle_story_draft_create` stores `stash.as_dict()` without submitter/placeholder
- [x] `handle_story_draft_submit` uses bridge → `handle_story_intake` (no `stash_pending`)
- [x] `handle_story_intake` always requires submitter via `parse_story_intake_request`

## Evidence

```
cd doge-complaints-gateway && rg 'stash_pending|STASH_PENDING' src/core/api/handlers.py || test $? -eq 1 → ok
python3 -m pytest -q tests/test_gw_draft_02_story_draft_submit_contract.py → 8 passed
```
