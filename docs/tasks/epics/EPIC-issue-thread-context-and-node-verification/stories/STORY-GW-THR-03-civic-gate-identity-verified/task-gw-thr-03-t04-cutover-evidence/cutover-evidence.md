# Cutover evidence — STORY-GW-THR-03 (AC-GW-THR03-04)

- **Date:** 2026-09-21T21:05:11Z
- **Package:** pkg-000095
- **Branch:** `semantic-schema-runtime`

## Ordered deploy (operator FACT)

1. **Identity VB-01 Done** — pkg-000050 — persist `profiles.identity_verified`  
   Migration on disk: `doge-identity-service/supabase/migrations/20260921000001_profiles_identity_verified.sql`
2. **Identity VB-02 Done** — pkg-000051 — `/me` exposes wire `identity_verified`
3. **Backfill** — `doge-identity-service/supabase/migrations/20260921000002_profiles_identity_verified_backfill.sql`  
   (`phone_verified OR eid_verified` → `identity_verified=true` one-shot)
4. **Gateway gate cutover (this wave)** — ALLOW only on opaque `identity_verified is True`  
   - `src/core/identity/verification_gate.py` — no `phone_verified` allow path  
   - `src/core/identity/me_client.py` — parse opaque; no dual-read for allow  
   - **No** feature flag / phone fallback

## Claims (code)

| Claim | Path |
|-------|------|
| Gate ignores phone for allow | `verification_gate.py` uses `identity_verified is not True` only |
| Legacy phone may still parse | `me_client._parse_me_body` optional `phone_verified`; never used by gate |
| Phone-only stub not allow | pytest `test_gate_phone_only_stub_must_not_allow` |

## Ops note

Apply identity migrations + backfill **before** deploying this gateway cutover to any environment that still has only method flags. Soft: VB-03 (live verify→set opaque) not required for this story DoD.
