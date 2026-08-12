# task-gw-cab-02-t05-tests-draft-current-auth-scoping-and-contract

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** test
- **Status:** 🟢 Done
- **Package:** pkg-000053
- **Skill declared:** python-pro
- **Depends on:** T04

## Purpose
Тесты: изоляция (owner-A не видит draft owner-B), null при отсутствии, latest-by-created_at, TTL-expired исключён, ассоциация при read, 401 без Bearer (backlog T05 list).

## Code Facts
- Pattern from [`tests/test_gw_cab_01_story_activity_api.py`](../../../../../../../../tests/test_gw_cab_01_story_activity_api.py)
- Draft helpers — [`tests/story_draft_intake_helpers.py`](../../../../../../../../tests/story_draft_intake_helpers.py)
- `require_story_draft_read_user` auth pattern — GW-DRAFT-02

## Acceptance / DoD
- [x] Traces parent AC-1: current returns draft or null
- [x] Traces parent AC-2: cross-device association via read
- [x] Traces parent AC-3: isolation test (user A ≠ user B draft)
- [x] Traces parent AC-4: expired/submitted excluded from current
- [x] Traces parent AC-5: `last_edited_at` = `updated_at`
- [x] 401 without Bearer
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-02-t05.md`](./acceptance-verification-gw-cab-02-t05.md) signed

## Where to change
- [`tests/test_gw_cab_02_current_draft_discovery.py`](../../../../../../../../tests/test_gw_cab_02_current_draft_discovery.py) (new)

## Out of scope
- Story acceptance gate (T06)
- Runtime implementation (T01–T04)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_gw_cab_02_current_draft_discovery.py -m "not live_integration"
```
