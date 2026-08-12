# task-gw-draft-04-t03-remove-oauth-introspection-client-and-env

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000046
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Backlog T03 (part 1): удалить `IdentityIntrospectionClient`, `build_identity_introspection_from_config`, поле `identity_introspection` из `ApiDependencies`, env `IDENTITY_INTROSPECT_URL`/`IDENTITY_SERVICE_TOKEN` из schema, exports из `identity/__init__.py`. Удалить или gut `introspection_client.py` (client only; `IntrospectionResult` already in T02 module).

## Code Facts
- Client — [`introspection_client.py`](../../../../../../../src/core/identity/introspection_client.py)
- DI wiring — [`dependencies.py:16,38,93-95`](../../../../../../../src/core/api/dependencies.py)
- Env — [`schema.py`](../../../../../../../src/core/config/schema.py) lines ~130,139
- `/me` path must remain — [`me_client.py`](../../../../../../../src/core/identity/me_client.py), `IDENTITY_BASE_URL`

## Acceptance / DoD
- Traces parent AC #1: OAuth client + env removed; grep consumers = 0 in `src/`
- Traces parent AC #2: `identity_me` / `/me` path intact
- No dangling `IDENTITY_INTROSPECT_URL` in EnvSpec or deploy docs touched in this task
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- [`src/core/identity/introspection_client.py`](../../../../../../../src/core/identity/introspection_client.py) (delete or reduce)
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py)
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- [`src/core/identity/__init__.py`](../../../../../../../src/core/identity/__init__.py)

## Out of scope
`require_user_token` / route deps (T04); tests (T05)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'IdentityIntrospectionClient|IDENTITY_INTROSPECT_URL|IDENTITY_SERVICE_TOKEN' src/
rg 'identity_introspection' src/
```
