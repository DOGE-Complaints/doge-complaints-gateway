# Story acceptance gate — STORY-GW-REQ11-05

- **Story:** Provision 200 fixture users (Identity + secrets file)
- **Package:** `pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml`
- **Result:** PASS* (code + offline tests + docs; live signup smoke blocked by Supabase email rate limit)
- **Date:** 2026-09-29T18:15:05Z

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1105-01: Script creates/updates verified accounts for 200 (or `--limit`) | PASS* | `life_sim_provision_users.py` + Make; *live `--limit 1` → Supabase HTTP 429 email rate limit |
| AC-GW-REQ1105-02: CSPRNG ≥24; gitignored secrets + generation_id | PASS | lib + `.gitignore` `tests/sandbox/.secrets/`; unit tests |
| AC-GW-REQ1105-03: password grant → Bearer → GET /me phone_verified=true | PASS* | code path file-OTP; *live blocked upstream by signup 429 |
| AC-GW-REQ1105-04: replay uses own Bearer from secrets (not pool %20) | PASS | runner 1:1 wire + dry-run secrets-1:1; pool deprecated |
| AC-GW-REQ1105-05: docs preconditions (file SMS, outbox, Supabase, pacing, never commit) | PASS | `note-gw-req11-05-provision-fixture-users-identity-2026-09-29.md` |
| AC-GW-REQ1105-06: offline unit tests; live `--limit` smoke when env available | PASS* | 10 pytest passed; live smoke attempted — 429 blocker documented |

## Operator blocker (live provision smoke)

| Fact | Value |
|------|-------|
| Identity `http://127.0.0.1:8100/health` | **200** (`SMS_PROVIDER=file` in identity `.env`) |
| File outbox | Present `doge-identity-service/var/sms-outbox` |
| Supabase signup `--limit 1` | **HTTP 429** `over_email_send_rate_limit` |
| Invent OTP HTTP | **Not done** (forbidden) |
| Secrets committed | **No** (`git check-ignore` covers `.secrets/`) |

## Commands (live verification 2026-09-29T18:15:05Z)

```text
--verify ok 7 (pkg-000104)
.venv/bin/python -m pytest -q tests/test_gw_req11_05_provision_fixture_users.py → 10 passed
.venv/bin/python tests/sandbox/life_sim_provision_users.py --dry-run --limit 3 → ok
.venv/bin/python tests/simulation_runner.py --life-sim --wipe-confirmed --dry-run --profile local --max 3 → 3/3 secrets-1:1
.venv/bin/python tests/sandbox/life_sim_provision_users.py --limit 1 → FAIL Supabase 429 (blocker)
utc_now: 2026-09-29T18:15:05Z
branch: dev
no invent GET /dev/last-otp; §Актуальная точка untouched; no push
```
