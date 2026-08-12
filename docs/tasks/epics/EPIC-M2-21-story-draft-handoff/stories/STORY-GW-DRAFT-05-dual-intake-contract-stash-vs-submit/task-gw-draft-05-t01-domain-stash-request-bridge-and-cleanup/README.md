# task-gw-draft-05-t01-domain-stash-request-bridge-and-cleanup

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000049
- **Skill declared:** python-pro
- **Depends on:** GW-DRAFT-01/02 Done; GW-PUBLIC-01 Done

## Purpose
Backlog T01 + Scope A (items 1–5) + exports C: introduce `StoryDraftStashRequest`, shared `_parse_story_envelope_body`, submit-bridge `intake_request_from_stash_and_submitter`; remove placeholder constant and `require_submitter` flag from domain layer.

## Code Facts
- Placeholder — [`contracts.py:18`](../../../../../../../../src/core/intake/contracts.py#L18) `STASH_PENDING_EXTERNAL_USER_ID`
- `require_submitter` — [`contracts.py:212,227,244`](../../../../../../../../src/core/intake/contracts.py)
- Stash parser returns intake today — [`contracts.py:396-398`](../../../../../../../../src/core/intake/contracts.py)
- Exports — [`intake/__init__.py:17,49`](../../../../../../../../src/core/intake/__init__.py)
- Authoritative submitter (bridge consumer) — [`authoritative_submitter.py`](../../../../../../../../src/core/identity/authoritative_submitter.py)

## Acceptance / DoD
- [ ] Traces parent AC #1: `STASH_PENDING_EXTERNAL_USER_ID` and `require_submitter` removed from `contracts.py` and `intake/__init__.py`
- [ ] Traces parent AC #2: `parse_story_draft_stash_request` returns `StoryDraftStashRequest`
- [ ] `StoryDraftStashRequest` frozen dataclass without `submitter`; `StoryIntakeRequest` always requires submitter
- [ ] `intake_request_from_stash_and_submitter(stash, submitter=...)` implemented
- [ ] `_parse_story_envelope_body` shared by both parsers (DRY)
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-05-t01.md`](./acceptance-verification-gw-draft-05-t01.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/src/core/intake/contracts.py`
- `doge-complaints-gateway/src/core/intake/__init__.py`

## Out of scope
- Handler wiring (T02); tests (T04); OpenAPI/docs (T05–T06)
- Hosted Supabase migration pipeline для `story_drafts` — ops follow-up, не блокирует
- GPT UI instructions changes

## Verification commands
```bash
cd doge-complaints-gateway && rg 'STASH_PENDING|require_submitter' src/core/intake/
cd doge-complaints-gateway && python3 -m pytest -q tests/test_story_intake_contract.py -k stash 2>/dev/null || true
cd doge-complaints-gateway && python3 -c "from core.intake.contracts import StoryDraftStashRequest, intake_request_from_stash_and_submitter"
```
