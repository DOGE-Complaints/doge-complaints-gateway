# task-gw-gauth-02-t05

## Meta
- **Story:** [STORY-GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000040
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Контрактные тесты introspection-слоя с mock identity HTTP: active+verified → проброс `{sub, phone_verified}`; `active=false` → отказ; identity down (timeout) → отказ; подтвердить, что `phone_verified` **не** читается из тела пользовательского JWT.

## Code Facts
- GAUTH-01 test harness — [`tests/conftest.py`](../../../../../../../tests/conftest.py) (`gauth_intake_headers`, auto-inject)
- GAUTH-01 contract pattern — [`tests/test_gw_gauth_01_two_layer_auth_contract.py`](../../../../../../../tests/test_gw_gauth_01_two_layer_auth_contract.py)
- Identity response contract — [`introspection.py`](../../../../../../../../../doge-identity-service/src/core/oauth/introspection.py)

## Acceptance / DoD
- Traces parent AC: active introspection → `{sub, phone_verified}` available / request proceeds (handler may still gate in GAUTH-03)
- Traces parent AC: `active=false` → request rejected, no story
- Traces parent AC: identity timeout/down → request rejected (fail-closed)
- Traces parent AC: no local JWT decode for verification status
- Traces parent AC: outbound request includes service token to identity mock
- Mock-based tests green in CI (`not live_integration`)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_gauth_02_user_token_introspection_contract.py` (new)
- [`tests/conftest.py`](../../../../../../../tests/conftest.py) — mock identity URL / respx or TestClient hook fixtures

## Out of scope
- Live identity E2E (`live_integration` optional, not gate blocker)
- GAUTH-03 `verification_required` 403 tests

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_02_user_token_introspection_contract.py
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q -m 'not live_integration'
```
