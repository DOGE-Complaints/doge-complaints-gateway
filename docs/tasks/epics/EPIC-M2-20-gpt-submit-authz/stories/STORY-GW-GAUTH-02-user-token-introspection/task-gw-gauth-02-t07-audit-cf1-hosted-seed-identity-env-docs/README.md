# task-gw-gauth-02-t07

## Meta
- **Story:** [STORY-GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection.md)
- **Type:** docs
- **Status:** 🟢 Done (2026-06-25) — `IDENTITY_*` + verified user-токен задокументированы в server-env-quickstart + seed runbook + runner-manual (docs-only, suite 548 без регрессий). Live hosted seed-прогон — P6 операторская задача.
- **Package:** — (audit override, вне pkg-000040)
- **Skill declared:** python-pro
- **Depends on:** T01–T06 (Done); GW-GAUTH-03 Done (phone_verified gate)
- **Wave:** audit override (`run_mode=gw_gauth_02_audit_cf1_followup`)
- **Decision Ref:** [`audit-gw-gauth-02-user-token-introspection-2026-06-25.md`](../../../../../../analysis/audit-gw-gauth-02-user-token-introspection-2026-06-25.md) §3 CF-1; углубление [`audit-gw-gauth-03-verification-gate-403-2026-06-25.md`](../../../../../../analysis/audit-gw-gauth-03-verification-gate-403-2026-06-25.md) §3 CF-1

## Purpose
Задокументировать для hosted seed цепочку после live introspection (GW-GAUTH-02) и verify-гейта (GW-GAUTH-03): gateway **должен** иметь `IDENTITY_INTROSPECT_URL` + `IDENTITY_SERVICE_TOKEN` на сервере; загрузчик — **реальный verified** OAuth user token в `GATEWAY_USER_TOKEN` (не дефолт `GATEWAY_API_TOKEN`). Закрывает CF-1: без этого intake на реальном gateway = **503** (identity unconfigured/down) или **403** `verification_required` (active, но `phone_verified=false`), не успешный приём истории.

## Code Facts
- `identity_introspection=None` при unset `IDENTITY_INTROSPECT_URL` → **503** `UserTokenIntrospectionUnavailableError` — [`asgi_app.py:306-310`](../../../../../../../src/core/api/asgi_app.py#L306)
- Identity introspect failure → **503** (fail-closed, не verification_required) — [`asgi_app.py:311-316`](../../../../../../../src/core/api/asgi_app.py#L311)
- `phone_verified is not True` → **403** `verification_required` + `verify_url` — [`asgi_app.py:318-326`](../../../../../../../src/core/api/asgi_app.py#L318), [`verification_gate.py:19-25`](../../../../../../../src/core/identity/verification_gate.py#L19)
- EnvSpec `IDENTITY_INTROSPECT_URL` / `IDENTITY_SERVICE_TOKEN` — [`schema.py`](../../../../../../../src/core/config/schema.py); `SPA_VERIFY_BASE_URL` для ответа 403 — [`verify_url.py`](../../../../../../../src/core/identity/verify_url.py)
- Loader default `X-User-Token = GATEWAY_API_TOKEN` — [`simulation_runner.py:172`](../../../../../../../tests/simulation_runner.py#L172); identity отвергнет сервисный токен как user OAuth
- T06 (G3, Done) задокументировал client-side `GATEWAY_USER_TOKEN` — [`task-gw-gauth-01-t06`](../../STORY-GW-GAUTH-01-two-layer-auth-on-submit/task-gw-gauth-01-t06-audit-g3-seed-docs-user-token/README.md); **нет** server-side `IDENTITY_*` в runtime-docs (grep 0 matches pre-T07)

## Acceptance / DoD
- Traces audit CF-1: hosted-seed runbooks описывают gateway `IDENTITY_INTROSPECT_URL` + `IDENTITY_SERVICE_TOKEN`
- Traces audit CF-1: явно — нужен **реальный verified** user OAuth token в `GATEWAY_USER_TOKEN` (`phone_verified=true` у identity; не подставлять `GATEWAY_API_TOKEN`)
- Traces GAUTH-03 CF-1 deepening: runbook объясняет 403 `verification_required` vs 503 vs 401
- Кросс-ссылка на GW-GAUTH-02 + GW-GAUTH-03 + T06 (G3 client layer)
- `rg IDENTITY_INTROSPECT_URL|IDENTITY_SERVICE_TOKEN` в seed/server runtime-docs
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`seed-demo-data-runbook-ru.md`](../../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md) — предусловия hosted gateway env + verified user token
- [`simulation-runner-manual.md`](../../../../../../../runtime-docs/testing/simulation-runner-manual.md) — опциональная ссылка на server `IDENTITY_*` (не дублировать SSOT)
- [`server-env-quickstart.md`](../../../../../../../runtime-docs/manuals/server-env-quickstart.md) — `IDENTITY_*` для deployed gateway

## Out of scope
- `src/core/**` implementation
- pytest / live hosted seed run
- Demo-bypass policy code

## Verification commands
```bash
rg -n 'IDENTITY_INTROSPECT_URL|IDENTITY_SERVICE_TOKEN|phone_verified|verification_required' \
  doge-complaints-gateway/docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md \
  doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md \
  doge-complaints-gateway/docs/runtime-docs/testing/simulation-runner-manual.md
```
