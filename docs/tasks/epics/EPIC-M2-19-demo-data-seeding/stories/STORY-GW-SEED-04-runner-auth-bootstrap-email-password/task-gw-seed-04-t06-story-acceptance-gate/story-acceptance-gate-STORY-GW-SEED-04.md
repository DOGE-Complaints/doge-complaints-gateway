# Story acceptance gate — STORY-GW-SEED-04

- **Story:** Runner auth bootstrap (email+password → Supabase token)
- **Package:** `pkg-000051-20260711-gw-seed-04-runner-auth-bootstrap-email-password.yaml`
- **Result:** PASS
- **Date:** 2026-07-11T19:17:48Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `.env.test` uses `GATEWAY_USER_EMAIL`+`GATEWAY_USER_PASSWORD`+`SUPABASE_URL`+`SUPABASE_ANON_KEY`; `GATEWAY_USER_TOKEN`/`SMOKE_USER_BEARER_TOKEN` removed (grep=0 in active code+docs) | PASS | T03 `.env.test.example`; T05 smoke migration; grep 0 in src/tests/runtime-docs |
| Runner on start exchanges email+password → Supabase access_token and submits without manual token | PASS | T01 `simulation_intake_http.py`; T05 unit tests |
| Unverified / bad creds / missing env → explicit error (fail-closed), no auto-provision | PASS | T02 `format_submit_failure` + Supabase login errors |
| Token in-memory only (not written to disk/log) | PASS | T01 `_cached_user_bearer_token` module cache |
| Runbook + simulation-runner-manual + `.env.test.example` aligned | PASS | T03 + T04 runtime docs |
| Full offline suite (`-m "not live_integration"`) green | PASS | 573 passed, 12 skipped (2026-07-11) |

## Commands (live verification 2026-07-11)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
rg 'GATEWAY_USER_TOKEN|SMOKE_USER_BEARER_TOKEN' doge-complaints-gateway/src doge-complaints-gateway/tests doge-complaints-gateway/docs/runtime-docs
# Operator hosted smoke (follow-up): runbook §Шаг2 with .env.test email+password
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
