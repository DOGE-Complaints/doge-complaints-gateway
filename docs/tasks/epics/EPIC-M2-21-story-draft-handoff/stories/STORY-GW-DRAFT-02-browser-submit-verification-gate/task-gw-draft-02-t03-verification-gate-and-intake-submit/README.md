# task-gw-draft-02-t03-verification-gate-and-intake-submit

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000044
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Гейт: реюз `evaluate_verification_gate` → 202 (создать историю через `StoryIntakeService.create_story`, автор=`sub` via `authoritative_submitter_from_introspection`) / 403 `verification_required` + `verify_url` / 401 / 503 fail-closed; при отказе история **не** создаётся.

## Code Facts
- Gate — [`verification_gate.py:19-25`](../../../../../../../src/core/identity/verification_gate.py)
- Author resolver — [`authoritative_submitter.py`](../../../../../../../src/core/identity/authoritative_submitter.py)
- Intake path — [`handlers.py:145+`](../../../../../../../src/core/api/handlers.py), [`services.py:146+`](../../../../../../../src/core/application/services.py)
- 403 envelope — [`envelope.py:93-99`](../../../../../../../src/core/api/envelope.py), `VerificationRequiredError` handlers in [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)
- Pattern — `require_user_token` + gate in [`asgi_app.py:301-332`](../../../../../../../src/core/api/asgi_app.py)

## Acceptance / DoD
- Traces parent AC #1: `phone_verified=true` → **202**, `submitter=sub`
- Traces parent AC #2: `phone_verified=false` → **403** + `verify_url`
- Traces parent AC #3: no/bad token → **401**; identity down → **503**, no story created
- Story not created on any auth/gate failure (fail-closed)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py) — `handle_story_draft_submit` intake branch
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — dependency / exception mapping

## Out of scope
Idempotency key + draft cleanup (T04); contract tests (T05)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'evaluate_verification_gate|authoritative_submitter_from_introspection' src/core/api/handlers.py
```
