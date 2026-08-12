# task-gw-cab-01-t05-tests-story-activity-auth-scoping-and-contract

## Meta
- **Story:** [STORY-GW-CAB-01](../STORY-GW-CAB-01-story-activity-api.md)
- **Type:** test
- **Status:** 🟢 Done
- **Package:** pkg-000052
- **Skill declared:** python-pro
- **Depends on:** T02–T04

## Purpose
Regression coverage: auth scoping (user A ≠ user B), MVP contract shape, metrics/status mapping, negative cases (401, empty list).

## Code Facts
- Test patterns — [`tests/story_draft_intake_helpers.py`](../../../../../../../../tests/story_draft_intake_helpers.py), [`tests/test_gw_public_01_public_issues_regression.py`](../../../../../../../../tests/test_gw_public_01_public_issues_regression.py)
- Identity me patch — `patch_identity_me_verified` in story draft helpers
- Parent AC — pipeline story §Acceptance Criteria AC-1..AC-4

## Acceptance / DoD
- [x] Traces AC-1: contract shape asserted in tests
- [x] Traces AC-2: cross-user isolation (submitter scoping)
- [x] Traces AC-4 negative: no write/pagination/issue-detail fields in response
- [x] Offline suite green (`-m "not live_integration"`)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-01-t05.md`](./acceptance-verification-gw-cab-01-t05.md) signed

## Where to change
- [`tests/test_gw_cab_01_story_activity_api.py`](../../../../../../../../tests/test_gw_cab_01_story_activity_api.py) (new)

## Out of scope
- Live integration / hosted smoke (operator follow-up)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_gw_cab_01_story_activity_api.py
python3 -m pytest -q -m "not live_integration"
```
