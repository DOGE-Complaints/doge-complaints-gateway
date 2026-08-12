# Acceptance — TASK-GW-SEED-04-T03

- **Result:** PASS
- **Date:** 2026-07-11

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| `.env.test.example` uses 4 Supabase auth vars | PASS | `GATEWAY_USER_EMAIL`, `GATEWAY_USER_PASSWORD`, `SUPABASE_URL`, `SUPABASE_ANON_KEY` in `.env.test.example` |
| Old token vars removed | PASS | `rg GATEWAY_USER_TOKEN\|SMOKE_USER_BEARER_TOKEN .env.test.example` → 0 |
