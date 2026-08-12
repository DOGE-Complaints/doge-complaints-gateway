# task-gw-draft-04-t01-change-propagation-audit

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** analyze
- **Status:** 🟢 Done
- **Package:** pkg-000046
- **Skill declared:** python-pro
- **Depends on:** GW-DRAFT-03 (canon superseded)

## Purpose
Backlog T01: перечислить **все** файлы-потребители удаляемого (`IdentityIntrospectionClient`, `require_user_token`, `IDENTITY_INTROSPECT_URL`, `_PUBLIC_CONTENT_WRITE_DEPS`); зафиксировать план правок и решение по `/tallinn/issues` + `/intake/stories`.

**P1 default decision:** оба роута → `[Depends(require_public_content_service_auth)]` only; OAuth `require_user_token` снимается полностью. Browser user auth остаётся на `/story-drafts*` (GW-DRAFT-02).

## Code Facts
- `require_user_token` — [`asgi_app.py:303-334`](../../../../../../../src/core/api/asgi_app.py#L303)
- `_PUBLIC_CONTENT_WRITE_DEPS` — [`asgi_app.py:337-340`](../../../../../../../src/core/api/asgi_app.py#L337) на [`/tallinn/issues:525`](../../../../../../../src/core/api/asgi_app.py#L525), [`/intake/stories:541`](../../../../../../../src/core/api/asgi_app.py#L541)
- `IdentityIntrospectionClient` DI — [`dependencies.py:38,93-95`](../../../../../../../src/core/api/dependencies.py#L38)
- Env — [`schema.py`](../../../../../../../src/core/config/schema.py) `IDENTITY_INTROSPECT_URL`, `IDENTITY_SERVICE_TOKEN`
- Test hooks — [`tests/conftest.py`](../../../../../../../tests/conftest.py)
- Simulation — [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py)

## Acceptance / DoD
- Traces parent AC #4: user-слой на `/intake/stories` и `/tallinn/issues` явно разрешён (service-only)
- Artifact `change-propagation-inventory-gw-draft-04.md` lists all consumers + planned edits per file
- Route decision documented with rationale vs GW-DRAFT-02 `/story-drafts*`
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- Task artifact only: [`change-propagation-inventory-gw-draft-04.md`](./change-propagation-inventory-gw-draft-04.md)

## Out of scope
Prod code changes (T02–T06); удаление истории (D-DRAFT-6)

## Verification commands
```bash
rg -l 'IdentityIntrospectionClient|require_user_token|IDENTITY_INTROSPECT_URL|_PUBLIC_CONTENT_WRITE_DEPS' \
  doge-complaints-gateway/src doge-complaints-gateway/tests
```
