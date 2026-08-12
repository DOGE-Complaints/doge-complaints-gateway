# task-gw-gauth-01-t06

## Meta
- **Story:** [STORY-GW-GAUTH-01](../STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Type:** docs
- **Status:** 🟢 Done (2026-06-25) — seed SSOT задокументировал `GATEWAY_USER_TOKEN`/`X-User-Token`
- **Package:** — (audit override, вне pkg-000039)
- **Skill declared:** python-pro
- **Depends on:** T01–T05
- **Wave:** audit override (`run_mode=gw_gauth_01_audit_g3_followup`)
- **Decision Ref:** [`audit-gw-gauth-01-two-layer-auth-on-submit-2026-06-25.md`](../../../../../../analysis/audit-gw-gauth-01-two-layer-auth-on-submit-2026-06-25.md) §3 G3

## Purpose
Задокументировать в seed SSOT переменную `GATEWAY_USER_TOKEN` и HTTP-заголовок `X-User-Token`, чтобы оператор не полагался на дефолт «user token = service token» после включения реального introspection в GW-GAUTH-02.

## Code Facts
- Runner уже шлёт оба заголовка — [`simulation_runner.py`](../../../../../../../tests/simulation_runner.py) `_post_json` (`Authorization: Bearer`, `X-User-Token`); `gateway_user_token = getenv("GATEWAY_USER_TOKEN", gateway_api_token)` ([`:172`](../../../../../../../tests/simulation_runner.py#L172))
- Gateway читает user token из `X-User-Token` — [`security.py:16-19`](../../../../../../../src/core/api/security.py#L16)
- GAUTH-01 user gate = presence stub only — [`asgi_app.py:266-269`](../../../../../../../src/core/api/asgi_app.py#L266)
- SSOT загрузки без `GATEWAY_USER_TOKEN` — [`simulation-runner-manual.md`](../../../../../../../runtime-docs/testing/simulation-runner-manual.md)
- E2E runbook без user-token layer — [`seed-demo-data-runbook-ru.md`](../../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md)

## Acceptance / DoD
- Traces audit G3: оба мануала описывают `GATEWAY_USER_TOKEN` и `X-User-Token`
- Явная пометка: при GAUTH-01 достаточно presence stub; после GW-GAUTH-02 нужен **реальный** user access token (не подставлять `GATEWAY_API_TOKEN`)
- Кросс-ссылка на [GW-GAUTH-02 backlog](../../../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-02-user-token-introspection.md)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`simulation-runner-manual.md`](../../../../../../../runtime-docs/testing/simulation-runner-manual.md) — env table + быстрый старт
- [`seed-demo-data-runbook-ru.md`](../../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md) — предусловия / шаг загрузки (кратко, без дублирования SSOT runner-manual)

## Out of scope
- Introspection client (GW-GAUTH-02)
- Изменения [`simulation_runner.py`](../../../../../../../tests/simulation_runner.py) (уже обновлён в GAUTH-01 P3)
- Правки `src/core/api/*`

## Verification commands
```bash
rg -n 'GATEWAY_USER_TOKEN|X-User-Token' doge-complaints-gateway/docs/runtime-docs/testing/simulation-runner-manual.md
rg -n 'GATEWAY_USER_TOKEN|X-User-Token' doge-complaints-gateway/docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md
```
