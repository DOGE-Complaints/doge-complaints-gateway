# Change propagation inventory — GW-DRAFT-04

- **Task:** T01 change-propagation audit
- **Status:** Done
- **Date:** 2026-07-03

## Route decision (operator default)

| Route | Current deps | Target |
|-------|--------------|--------|
| `POST /intake/stories` | `_PUBLIC_CONTENT_WRITE_DEPS` (service + OAuth user) | `[Depends(require_public_content_service_auth)]` only |
| `POST /tallinn/issues` | `_PUBLIC_CONTENT_WRITE_DEPS` | `[Depends(require_public_content_service_auth)]` only |
| `POST /story-drafts/{id}/submit` | browser `/me` (GW-DRAFT-02) | unchanged |

**Rationale:** GPT direct submit superseded (GW-DRAFT-03); legacy intake/tallinn writes are trusted-service only. Browser user auth + `phone_verified` gate remain on `/story-drafts*`.

## Consumer inventory (`src/` + `tests/`)

| Symbol / artifact | Paths | Action |
|-------------------|-------|--------|
| `IdentityIntrospectionClient` | `introspection_client.py`, `dependencies.py:16,38,93-95`, `identity/__init__.py` | REMOVE (T03) |
| `build_identity_introspection_from_config` | `introspection_client.py`, `dependencies.py`, `identity/__init__.py` | REMOVE (T03) |
| `IdentityIntrospectionError` | `introspection_client.py`, `asgi_app.py:47`, `identity/__init__.py` | REMOVE with client (T03–T04) |
| `IDENTITY_INTROSPECT_URL` / `IDENTITY_SERVICE_TOKEN` | `schema.py` EnvSpec + `load_config_from_env` | REMOVE (T03) |
| `identity_introspect_url` / `identity_service_token` fields | `AppConfig` in `schema.py` | REMOVE (T03) |
| `require_user_token` | `asgi_app.py:303-334` | REMOVE (T04) |
| `_PUBLIC_CONTENT_WRITE_DEPS` | `asgi_app.py:337-340,525,541` | REPLACE → `[Depends(require_public_content_service_auth)]` (T04) |
| `extract_user_token` import | `asgi_app.py:45` | REMOVE unused import (T04) |
| `IntrospectionResult` | `introspection_client.py:16-19` | EXTRACT → `introspection_result.py` (T02) |
| KEEP imports | `verification_gate.py`, `authoritative_submitter.py`, `me_client.py` | Point to `introspection_result.py` (T02) |
| `handlers.py` issuer fallback | `identity_introspect_url` in `authoritative_submitter_from_introspection` call | Use `identity_base_url` only (T03) |
| `tests/conftest.py` | auto `X-User-Token`, `IDENTITY_INTROSPECT_*` env, `IdentityIntrospectionClient` mock | CLEANUP (T05) |
| `test_gw_gauth_02_*` | OAuth client + intake introspection HTTP tests | REMOVE OAuth-specific (T05) |
| `test_gw_gauth_03_*` | intake route introspection tests | KEEP gate unit tests only (T05) |
| `test_gw_gauth_04_*` | intake route author tests | KEEP unit tests; drop intake HTTP (T05) |
| `test_gw_gauth_01_*` | two-layer intake/tallinn | UPDATE → service-only contract (T05) |
| `tests/simulation_runner.py` | `GATEWAY_USER_TOKEN`, `X-User-Token` on `/intake/stories` | REMOVE (T06) |
| Seed/simulation docs | `simulation-runner-manual.md`, `seed-demo-data-runbook-ru.md` | Align service-only (T06) |

## Verify commands (baseline grep)

```bash
rg -l 'IdentityIntrospectionClient|require_user_token|IDENTITY_INTROSPECT_URL|_PUBLIC_CONTENT_WRITE_DEPS' \
  doge-complaints-gateway/src doge-complaints-gateway/tests
```

Post T07 expect **0** hits in `src/` for removed symbols.
