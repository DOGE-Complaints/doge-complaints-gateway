# task-gw-gauth-03-t02

## Meta
- **Story:** [STORY-GW-GAUTH-03](../STORY-GW-GAUTH-03-verification-gate-403.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000041
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Чистая функция гейта: по `IntrospectionResult` из GAUTH-02 решить `allow | verification_required | unauthorized | unavailable` (backlog черновик T01).

## Code Facts
- `IntrospectionResult` — [`introspection_client.py:15-19`](../../../../../../../src/core/identity/introspection_client.py)
- Сейчас только `active` enforced — [`asgi_app.py:287-290`](../../../../../../../src/core/api/asgi_app.py)
- D-GAUTH-4 fail-closed — [`interview-gpt-submit-authz-2026-06-24`](../../../../../../backlog-stories/gpt-submit-authz/interview-gpt-submit-authz-2026-06-24.md)

## Acceptance / DoD
- Traces parent AC #3, #4, #5, #6: correct branch per `{active, phone_verified}` + unavailable when verify config missing (policy documented)
- `active=true && phone_verified=true` → allow
- `active=false` → unauthorized (401 path in T04)
- `active=true && phone_verified=false` → verification_required (403 path in T04)
- Introspection transport/config failure → unavailable (not verification_required)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- New module e.g. [`src/core/identity/verification_gate.py`](../../../../../../../src/core/identity/verification_gate.py) or [`src/core/api/security.py`](../../../../../../../src/core/api/security.py)

## Out of scope
- HTTP response shaping (T03)
- Wiring into `require_user_token` (T04)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'verification_gate|VerificationGate' src/core/
```
