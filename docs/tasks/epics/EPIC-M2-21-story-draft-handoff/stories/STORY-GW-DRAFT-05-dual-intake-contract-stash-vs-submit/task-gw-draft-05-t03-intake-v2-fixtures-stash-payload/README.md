# task-gw-draft-05-t03-intake-v2-fixtures-stash-payload

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000049
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Backlog T03: add `valid_v2_stash_payload()` without submitter in test fixtures; keep `valid_v2_intake_payload()` with submitter for legacy/intake-bridge tests.

## Code Facts
- Intake fixture with submitter — [`intake_v2_fixtures.py`](../../../../../../../../tests/intake_v2_fixtures.py) `valid_v2_intake_payload()`
- Stash helper absent today — same file (no `valid_v2_stash_payload` yet)
- GPT OpenAPI stash shape — [`GPT UI/docs/custom-gpt-story-intake-actions.openapi.yaml`](../../../../../../../../../GPT%20UI/docs/custom-gpt-story-intake-actions.openapi.yaml) `StoryDraftStashRequest`

## Acceptance / DoD
- [ ] `valid_v2_stash_payload()` returns dict without `submitter` key
- [ ] `valid_v2_intake_payload()` unchanged (still includes submitter for intake/legacy paths)
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-05-t03.md`](./acceptance-verification-gw-draft-05-t03.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/tests/intake_v2_fixtures.py`

## Out of scope
- Contract test rewrites (T04); prod code (T01–T02)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -c "
from tests.intake_v2_fixtures import valid_v2_stash_payload, valid_v2_intake_payload
s = valid_v2_stash_payload()
assert 'submitter' not in s
assert 'submitter' in valid_v2_intake_payload()
print('ok')
"
```
