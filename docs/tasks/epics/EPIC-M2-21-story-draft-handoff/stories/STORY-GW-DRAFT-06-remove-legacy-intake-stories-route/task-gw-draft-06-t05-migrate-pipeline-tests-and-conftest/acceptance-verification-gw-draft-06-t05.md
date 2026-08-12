# Acceptance verification — task-gw-draft-06-t05-migrate-pipeline-tests-and-conftest

- **Task:** T05 migrate pipeline tests and conftest
- **Status:** PASS
- **Date:** 2026-07-11T10:15:42Z

## Checklist

- [x] `rg '"/intake/stories"' tests/` = 0 (except negative openapi assert)
- [x] Shared helper `tests/story_draft_intake_helpers.py`
- [x] `_SERVICE_WRITE_PATH_SUFFIXES` drops `/intake/stories`
- [x] GW-DRAFT-01/02 contract tests green

## Evidence

```
cd doge-complaints-gateway && rg '"/intake/stories"' tests/ → 1 hit (negative assert in test_openapi_runtime_compliance.py)
python3 -m pytest -q -m "not live_integration" → 565 passed, 12 skipped
python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py → pass
```
