# task-gw-gauth-03-t05

## Meta
- **Story:** [STORY-GW-GAUTH-03](../STORY-GW-GAUTH-03-verification-gate-403.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000041
- **Skill declared:** python-pro
- **Depends on:** T04

## Purpose
Contract tests всех веток гейта (backlog черновик T05): verified → 200; unverified → 403 + verify_url; inactive → 401; identity down → отказ ≠ verification_required; no story on reject.

## Code Facts
- GAUTH-02 harness — [`tests/conftest.py`](../../../../../../../tests/conftest.py) autouse introspection mock
- GAUTH-02 contract pattern — [`tests/test_gw_gauth_02_user_token_introspection_contract.py`](../../../../../../../tests/test_gw_gauth_02_user_token_introspection_contract.py)
- Intake fixture — [`tests/intake_v2_fixtures.py`](../../../../../../../tests/intake_v2_fixtures.py)

## Acceptance / DoD
- Traces all 6 parent AC via contract tests
- `phone_verified=false` → 403 + verify_url in body
- `active=false` → 401, not verification_required
- Identity unreachable → fail-closed, not verification_required
- Happy verified path → intake succeeds
- No story row / side-effect on reject paths
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- **CREATE** [`tests/test_gw_gauth_03_verification_gate_contract.py`](../../../../../../../tests/test_gw_gauth_03_verification_gate_contract.py)
- **UPDATE** [`tests/conftest.py`](../../../../../../../tests/conftest.py) — `phone_verified=false` cases without breaking GAUTH-02

## Out of scope
- Story gate artifact (T06)
- E2E hosted seed

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_03_verification_gate_contract.py
```
