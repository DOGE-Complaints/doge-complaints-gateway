# task-gw-gauth-04-t05

## Meta
- **Story:** [STORY-GW-GAUTH-04](../STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000042
- **Skill declared:** python-pro
- **Depends on:** T02, T03

## Purpose
Contract tests: при introspection автор = `sub`; при расхождении payload ↔ sub побеждает `sub`; fail-closed — без introspection / rejected gate нет истории с payload-автором (регрессия GAUTH-02/03).

## Code Facts
- Pattern — [`test_gw_gauth_03_verification_gate_contract.py`](../../../../../../../tests/test_gw_gauth_03_verification_gate_contract.py)
- GAUTH-02 introspection mocks — [`test_gw_gauth_02_user_token_introspection_contract.py`](../../../../../../../tests/test_gw_gauth_02_user_token_introspection_contract.py)
- Repository fetch for submitter — [`test_story_repository_lifecycle.py`](../../../../../../../tests/test_story_repository_lifecycle.py)

## Acceptance / DoD
- Traces parent AC #1: happy path persisted `submitter_external_user_id` == introspected `sub`
- Traces parent AC #2: mismatch test — sub wins
- Traces parent AC #4: no story with payload-only author when introspection missing/rejected
- New file `tests/test_gw_gauth_04_authoritative_author_contract.py` — all tests PASS
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`tests/test_gw_gauth_04_authoritative_author_contract.py`](../../../../../../../tests/test_gw_gauth_04_authoritative_author_contract.py) (new)
- Reuse fixtures from GAUTH-02/03 contract tests where applicable

## Out of scope
- Supabase live integration tests
- req-19 doc content assertions (T04)

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_04_authoritative_author_contract.py
```
