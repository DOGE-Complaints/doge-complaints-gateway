# task-gw-draft-06-t05-migrate-pipeline-tests-and-conftest

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000050
- **Skill declared:** python-pro
- **Depends on:** T01, T04

## Purpose
Backlog T04 (part 2): migrate remaining tests using HTTP `"/intake/stories"` to stash→submit helper or internal fixtures; update [`conftest.py`](../../../../../../../../tests/conftest.py) `_SERVICE_WRITE_PATH_SUFFIXES`; smoke tests. Target: **`rg '"/intake/stories"' tests/` = 0**.

## Code Facts
- Service write suffixes — [`conftest.py:16`](../../../../../../../../tests/conftest.py) `("/intake/stories", "/tallinn/issues")`
- Blast radius — 25+ test files (e2e, pipeline, cluster, smoke) grep `"/intake/stories"`
- Stash/submit pattern — GW-DRAFT-01/02 contract tests + `valid_v2_stash_payload()`

## Acceptance / DoD
- [ ] Traces parent AC #5: `rg '"/intake/stories"' tests/` = 0
- [ ] Shared helper (e.g. `tests/story_draft_intake_helpers.py`) for tests needing story creation
- [ ] `_SERVICE_WRITE_PATH_SUFFIXES` drops `/intake/stories`
- [ ] GW-DRAFT-01/02 contract tests green
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-06-t05.md`](./acceptance-verification-gw-draft-06-t05.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/tests/conftest.py`
- `doge-complaints-gateway/tests/story_draft_intake_helpers.py` (new)
- Remaining `tests/test_*.py`, `tests/smoke/*.py`, `tests/integration/**/*.py` with intake HTTP path

## Out of scope
- Dedicated route test files (T04)
- Production code changes beyond test helpers

## Verification commands
```bash
cd doge-complaints-gateway && rg '"/intake/stories"' tests/ || test $? -eq 1
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```
