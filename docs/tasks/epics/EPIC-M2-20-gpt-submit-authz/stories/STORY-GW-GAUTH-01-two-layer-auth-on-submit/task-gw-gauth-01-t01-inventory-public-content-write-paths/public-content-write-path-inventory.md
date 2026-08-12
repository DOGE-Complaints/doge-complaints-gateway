# Public content write-path inventory — STORY-GW-GAUTH-01 T01

**Status:** COMPLETE

**Date:** 2026-06-25

## Scope

Inventory all HTTP write mutations in [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) and classify per D-GAUTH-2 (public content affecting board).

Evidence:

```bash
cd doge-complaints-gateway && rg '@app\.(post|put|patch|delete)' src/core/api/asgi_app.py -n
```

Result (2026-06-25): only `POST` handlers — `/tallinn/issues`, `/intake/stories`, `/telemetry/label-misses`.

## Matrix

| Route | Method | Public content (D-GAUTH-2) | Service gate (before) | Service gate (after T02/T03) | User gate (after T02) |
|-------|--------|---------------------------|----------------------|------------------------------|------------------------|
| `/intake/stories` | POST | **Yes** — story intake affects public board pipeline | none (no-op) | `require_public_content_service_auth` (mandatory) | `require_user_token` stub → GAUTH-02 |
| `/tallinn/issues` | POST | **Yes** — issue creation on Tallinn board | `require_service_auth` (optional when token unset) | `require_public_content_service_auth` (mandatory) | `require_user_token` stub → GAUTH-02 |
| `/telemetry/label-misses` | POST | **No** — operational telemetry, not public content mutation | none | **Out of scope** (not D-GAUTH-2) | N/A |

## Non-write routes (reference)

| Route | Method | Notes |
|-------|--------|-------|
| `/health`, `/readiness` | GET | Liveness — no auth |
| `/protected/status`, `/metrics` | GET | Optional service auth (`mandatory=False`) |
| `/tallinn/issues` | GET | Read API — no write gate |
| `/issues` | POST | Legacy path — 404 in current app |

## Policy notes (T03)

- `build_service_auth_from_env()` returns `ServiceTokenAuth.mandatory_channel()` when `SERVICE_API_TOKEN` is unset — public-content POSTs reject with 401, not silent no-op.
- `APP_PROFILE=pilot` still requires `SERVICE_API_TOKEN` at config load ([`schema.py:463-466`](../../../../../../../src/core/config/schema.py#L463-L466)).
- Demo profile: config may omit token, but gated routes still enforce mandatory service layer at runtime.

## Dependency bundle

Public-content writes use `_PUBLIC_CONTENT_WRITE_DEPS` in [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py):

1. `require_public_content_service_auth` — channel trust (service token)
2. `require_user_token` — end-user token stub (`X-User-Token`; introspection in GW-GAUTH-02)
