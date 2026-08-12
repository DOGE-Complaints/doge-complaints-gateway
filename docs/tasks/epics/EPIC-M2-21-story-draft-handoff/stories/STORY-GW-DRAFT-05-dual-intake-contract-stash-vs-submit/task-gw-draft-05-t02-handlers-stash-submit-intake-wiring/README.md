# task-gw-draft-05-t02-handlers-stash-submit-intake-wiring

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000049
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Backlog T02 + Scope B: wire `handle_story_draft_create`, `handle_story_draft_submit`, `handle_story_intake` to dual-contract model; remove `stash_pending` branch; resolve backward-compat for legacy placeholder drafts in DB (document decision before code).

## Code Facts
- Stash create stores raw dict — [`handlers.py:539-546`](../../../../../../../../src/core/api/handlers.py)
- `stash_pending` branch — [`handlers.py:181-191`](../../../../../../../../src/core/api/handlers.py)
- Submit calls intake with record payload — [`handlers.py:686-692`](../../../../../../../../src/core/api/handlers.py)
- `STASH_PENDING` import in handlers — [`handlers.py:29`](../../../../../../../../src/core/api/handlers.py)

## Acceptance / DoD
- [ ] Traces parent AC #3: `handle_story_draft_create` stores `stash.as_dict()` without submitter/placeholder
- [ ] Traces parent AC #4: submit uses `intake_request_from_stash_and_submitter` with authoritative submitter from introspection only
- [ ] `handle_story_intake` always `parse_story_intake_request` (submitter required); no `stash_pending`
- [ ] Backward-compat decision documented in [`backward-compat-decision-gw-draft-05-t02.md`](./backward-compat-decision-gw-draft-05-t02.md)
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-05-t02.md`](./acceptance-verification-gw-draft-05-t02.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/src/core/api/handlers.py`
- Task artifact: [`backward-compat-decision-gw-draft-05-t02.md`](./backward-compat-decision-gw-draft-05-t02.md)

## Out of scope
- Domain types (T01); contract test updates (T04); OpenAPI/docs (T05–T06)
- `POST /intake/stories` removal → GW-DRAFT-06

## Verification commands
```bash
cd doge-complaints-gateway && rg 'stash_pending|STASH_PENDING' src/core/api/handlers.py || test $? -eq 1
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py
```
