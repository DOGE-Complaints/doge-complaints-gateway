# task-gw-draft-01-t05-story-draft-contract-tests

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000043
- **Skill declared:** python-pro
- **Depends on:** T03, T04

## Purpose
Contract tests: service token → `{draft_id}` + no issue; 401; 400 VALIDATION_ERROR; GET payload/404; TTL expiry → 404 (pattern `test_gw_*`).

## Code Facts
- Contract pattern — [`tests/test_gw_gauth_04_authoritative_author_contract.py`](../../../../../../../tests/test_gw_gauth_04_authoritative_author_contract.py)
- Fixtures — [`tests/conftest.py`](../../../../../../../tests/conftest.py), [`tests/intake_v2_fixtures.py`](../../../../../../../tests/intake_v2_fixtures.py)

## Acceptance / DoD
- Traces parent AC #1–#5
- New file e.g. `tests/test_gw_draft_01_story_draft_stash_contract.py`
- All contract cases green in P3
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `tests/test_gw_draft_01_story_draft_stash_contract.py` (new)

## Out of scope
Story gate rollup (T07); runtime-docs (T06)

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py
```
