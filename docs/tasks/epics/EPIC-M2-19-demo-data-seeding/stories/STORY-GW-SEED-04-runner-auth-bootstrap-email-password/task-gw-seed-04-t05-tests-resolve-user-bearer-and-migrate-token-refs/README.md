# task-gw-seed-04-t05

## Meta
- **Story:** [STORY-GW-SEED-04](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000051
- **Skill declared:** python-pro
- **Depends on:** T01, T02

## Purpose
Backlog T05: unit tests on `resolve_user_bearer_token` with mocked Supabase token endpoint (success / bad creds / missing env); migrate existing `GATEWAY_USER_TOKEN` references in tests.

## Code Facts
- Token resolver — [`simulation_intake_http.py`](../../../../../../../tests/simulation_intake_http.py)
- SEED-03 tests — [`test_gw_seed_03_simulation_runner_submit.py`](../../../../../../../tests/test_gw_seed_03_simulation_runner_submit.py) (`GATEWAY_USER_TOKEN` asserts)
- Smoke conftest — [`tests/smoke/conftest.py:81-104`](../../../../../../../tests/smoke/conftest.py) `smoke_browser_bearer_token()`
- Offline suite marker — `-m "not live_integration"` per parent AC#6

## Acceptance / DoD
- Traces parent AC#1, AC#2, AC#6
- New [`tests/test_gw_seed_04_runner_auth_bootstrap.py`](../../../../../../../tests/test_gw_seed_04_runner_auth_bootstrap.py): mock Supabase `/auth/v1/token` — success, bad creds, missing env
- `test_gw_seed_03_simulation_runner_submit.py` updated for email+password path (or superseded scenarios)
- `tests/smoke/conftest.py` uses shared resolver (no raw `GATEWAY_USER_TOKEN` env reads)
- `pytest -m "not live_integration"` green after migration

## Where to change
- [`tests/test_gw_seed_04_runner_auth_bootstrap.py`](../../../../../../../tests/test_gw_seed_04_runner_auth_bootstrap.py) (new)
- [`tests/test_gw_seed_03_simulation_runner_submit.py`](../../../../../../../tests/test_gw_seed_03_simulation_runner_submit.py)
- [`tests/smoke/conftest.py`](../../../../../../../tests/smoke/conftest.py)

## Out of scope
- Live hosted smoke (T06 gate operator step)
- `src/core/` changes

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_gw_seed_04_runner_auth_bootstrap.py tests/test_gw_seed_03_simulation_runner_submit.py
python3 -m pytest -q -m "not live_integration"
```
