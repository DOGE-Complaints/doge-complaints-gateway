# Acceptance — TASK-GW-GAUTH-02-T07

- **Result:** PASS
- **Date:** 2026-06-25

| AC (audit CF-1) | Status | Evidence |
|-----------------|--------|----------|
| Gateway `IDENTITY_*` documented for hosted deploy | PASS | [`server-env-quickstart.md` §3](../../../../../../../runtime-docs/manuals/server-env-quickstart.md) — таблица `IDENTITY_INTROSPECT_URL`/`IDENTITY_SERVICE_TOKEN`/`SPA_VERIFY_BASE_URL` + поведение 401/403/503; [`seed-demo-data-runbook-ru.md`](../../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md) предусловие «серверная сторона». |
| Real active user OAuth token required for loader | PASS | seed runbook: `GATEWAY_USER_TOKEN` = настоящий OAuth-токен, не дефолтный `GATEWAY_API_TOKEN`; runner-manual `GATEWAY_USER_TOKEN`-строка обновлена. |
| Verified user token (`phone_verified=true`) documented | PASS | seed runbook + runner-manual: без `phone_verified=true` → **403** `verification_required`; цит. GAUTH-03 verify-гейт. |
| `rg IDENTITY_` in runtime-docs | PASS | `rg IDENTITY_INTROSPECT_URL\|IDENTITY_SERVICE_TOKEN docs/runtime-docs/` → 3 файла (runbook, quickstart, runner-manual). |

**Verification:**
```
rg -c 'IDENTITY_INTROSPECT_URL|IDENTITY_SERVICE_TOKEN' \
  docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md \
  docs/runtime-docs/manuals/server-env-quickstart.md \
  docs/runtime-docs/testing/simulation-runner-manual.md
# → runbook:1, quickstart:2, runner-manual:2
/usr/local/bin/python3.11 -m pytest tests/ -q  # 548 passed (доки-only, без регрессий)
```
Закрывает CF-1 ([`audit-gw-gauth-02 §3`](../../../../../../analysis/audit-gw-gauth-02-user-token-introspection-2026-06-25.md) + углубление [`audit-gw-gauth-03 §3`](../../../../../../analysis/audit-gw-gauth-03-verification-gate-403-2026-06-25.md)). Прод-код не тронут (docs-only). Live hosted seed-прогон — операторская задача (P6, вне репо).
