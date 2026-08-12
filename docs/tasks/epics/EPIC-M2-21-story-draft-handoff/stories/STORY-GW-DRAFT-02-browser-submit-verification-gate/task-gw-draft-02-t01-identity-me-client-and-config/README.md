# task-gw-draft-02-t01-identity-me-client-and-config

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000044
- **Skill declared:** python-pro
- **Depends on:** GW-DRAFT-01 (draft store live)

## Purpose
Конфиг+клиент: EnvSpec `IDENTITY_BASE_URL` в [`schema.py`](../../../../../../../src/core/config/schema.py); `identity/me_client.py` (`GET {IDENTITY_BASE_URL}/me` с Bearer форвардом; парсинг ответа → `IntrospectionResult(active=True, sub=supabase_user_id, phone_verified=…)`; timeout; ошибки → fail-closed `IdentityMeError`).

## Code Facts
- HTTP client pattern — [`introspection_client.py`](../../../../../../../src/core/identity/introspection_client.py)
- Env today — `IDENTITY_INTROSPECT_URL` / `IDENTITY_SERVICE_TOKEN` in [`schema.py`](../../../../../../../src/core/config/schema.py); **no** `IDENTITY_BASE_URL`
- Identity `/me` payload — [`me_response.py:19-45`](../../../../../../../../doge-identity-service/src/core/api/me_response.py) — `supabase_user_id`, `phone_verified`
- Value object — [`IntrospectionResult`](../../../../../../../src/core/identity/introspection_client.py#L16)

## Acceptance / DoD
- Traces parent AC #6: user check via identity `/me`, gateway does not validate Supabase JWT locally
- `IDENTITY_BASE_URL` in EnvSpec + `AppConfig`
- `IdentityMeClient.fetch_me(bearer_token) -> IntrospectionResult` with fail-closed on transport/parse errors
- Maps `supabase_user_id` → `IntrospectionResult.sub` (operator P1 decision)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- `src/core/identity/me_client.py` (new)
- [`src/core/identity/__init__.py`](../../../../../../../src/core/identity/__init__.py) (exports if needed)

## Out of scope
Route wiring (T02); `evaluate_verification_gate` (T03)

## Open question (implementation)
`IDENTITY_BASE_URL` separate env vs derive host from `IDENTITY_INTROSPECT_URL`.

## Verification commands
```bash
cd doge-complaints-gateway && rg 'IDENTITY_BASE_URL|IdentityMeClient|me_client' src/core/
```
