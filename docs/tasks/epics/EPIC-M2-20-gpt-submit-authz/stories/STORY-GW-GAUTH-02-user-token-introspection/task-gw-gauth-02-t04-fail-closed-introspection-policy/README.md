# task-gw-gauth-02-t04

## Meta
- **Story:** [STORY-GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000040
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Единая fail-closed политика (D-GAUTH-4): timeout, 5xx, invalid JSON, `active=false` → безопасный отказ; история **не** создаётся; без degraded-режима и без fallback на `payload.submitter`.

## Code Facts
- D-GAUTH-4 — [`interview-gpt-submit-authz-2026-06-24`](../../../../../../backlog-stories/gpt-submit-authz/interview-gpt-submit-authz-2026-06-24.md)
- Inactive token shape — identity returns `{"active": false}` HTTP 200 — [`introspection.py:17-22`](../../../../../../../../../doge-identity-service/src/core/oauth/introspection.py)
- Payload submitter trust today — [`intake/contracts.py`](../../../../../../../src/core/intake/contracts.py) (must not bypass introspection failure)
- GAUTH-03 owns `verification_required` 403 — story Out of scope

## Acceptance / DoD
- Traces parent AC: Identity недоступен/ответ невалиден/`active=false` → безопасный отказ (fail-closed, D-GAUTH-4)
- No story persisted on any fail-closed path before handler body runs
- No silent success when identity unreachable
- No fallback to submitter fields from request body when introspection fails
- HTTP response code for fail-closed: 401 Unauthorized (until GAUTH-03 adds 403 for unverified)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Introspection client error mapping (T02)
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — `require_user_token` / dependency exception handling
- [`src/core/api/security.py`](../../../../../../../src/core/api/security.py) — error types if needed

## Out of scope
- `verification_required` (403) for `phone_verified=false` — GW-GAUTH-03
- Retry/circuit-breaker beyond single-request timeout

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_02_user_token_introspection_contract.py -k 'fail_closed or inactive or timeout' 2>/dev/null || true
```
