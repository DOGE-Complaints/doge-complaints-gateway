# acceptance-verification — GW-REQ9-01 T02

- **Date:** 2026-09-26T12:06:30Z
- **Package:** pkg-000096 (immutable)
- **Result:** PASS
- **Evidence:** `AppConfig.spa_base_url`; load `_get_value(..., "SPA_BASE_URL")` in `schema.py`. `rg SPA_VERIFY|spa_verify` under `src/` → 0 hits. AC-GW-REQ901-03.
