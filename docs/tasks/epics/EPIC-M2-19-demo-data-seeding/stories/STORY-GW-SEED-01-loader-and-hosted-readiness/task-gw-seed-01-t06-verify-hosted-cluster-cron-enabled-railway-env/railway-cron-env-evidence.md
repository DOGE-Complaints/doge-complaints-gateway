# Railway CLUSTER_CRON_ENABLED — evidence (hosted)

**Captured:** 2026-06-22T08:56:56Z  
**Target:** `https://dogestonia-tallinn.up.railway.app`  
**Audit gap:** R1 MEDIUM ([`audit-gw-seed-01-loader-and-hosted-readiness-2026-06-22.md`](../../../../../../analysis/audit-gw-seed-01-loader-and-hosted-readiness-2026-06-22.md) §2)

## Verification attempts (this run)

| Method | Result | Notes |
|--------|--------|-------|
| `railway whoami` | **BLOCKED** | `Unauthorized. Please run railway login again.` — CLI cannot read Variables or deploy logs |
| `railway logs` | **BLOCKED** | `No linked project found` (no valid session) |
| `GET /ready` (public) | OK | `status=ready`, `db.backend=supabase`, `db.ready=true` — **does not expose** `CLUSTER_CRON_ENABLED` |
| `GET /metrics` (auth) | 401 | Token from `.env.test` rejected on hosted (token/env mismatch for protected routes) |
| Schema default inference | **Rejected** | Audit R1 explicitly disallows PASS on default-only; local `.env` has `CLUSTER_CRON_ENABLED=false` proving override |

## Hosted startup log (`cron_enabled=`)

**Not captured in this run.** Requires operator with Railway access:

```bash
railway login
cd doge-complaints-gateway && railway link   # select dogestonia-tallinn service
railway variables | grep CLUSTER_CRON
railway logs --lines 200 | grep 'startup.config.*cron_enabled'
```

Expected PASS line (example format from [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)):

```
startup.config db_backend=supabase ... cron_enabled=True cron_interval_s=...
```

If `CLUSTER_CRON_ENABLED` is missing or `false` in Railway Variables → set `CLUSTER_CRON_ENABLED=true`, redeploy, re-grep logs.

## Operator checklist (to close R1)

1. Railway dashboard → service **dogestonia-tallinn** → Variables → confirm `CLUSTER_CRON_ENABLED=true` (explicit, not assumed default).
2. Redeploy if changed.
3. Copy deploy log line with `cron_enabled=True` into this file § «Hosted startup log».
4. Re-run T06 acceptance + update T01 `hosted-readiness-checklist.md` (remove R1 qualifier).

## Status

**BLOCKED** — autonomous verify/fix cannot complete without `railway login` + Variables or deploy-log evidence.
