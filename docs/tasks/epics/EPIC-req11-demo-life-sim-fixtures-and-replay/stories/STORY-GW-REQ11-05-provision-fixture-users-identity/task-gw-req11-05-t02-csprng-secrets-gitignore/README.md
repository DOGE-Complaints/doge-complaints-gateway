# task-gw-req11-05-t02-csprng-secrets-gitignore

## Task: implement / tooling — CSPRNG secrets + gitignore (T02)

## Meta
- **Story:** [STORY-GW-REQ11-05](../STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-29T18:15:05Z
- **Package:** pkg-000104
- **Skill declared:** python-pro
- **Depends on:** T01 (or same P3 wave after signup loop exists)
- **Scaffolded:** 2026-09-29T18:09:49Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md`

## Purpose
CSPRNG passwords ≥24 (`secrets`); write gitignored `tests/sandbox/.secrets/life_sim_users_creds_<generation_id>.json`; never commit. Scope #2,#6 · AC-GW-REQ1105-02.

## Code Facts
1. CSPRNG `generate_password` ≥24 Present in `life_sim_provision_lib.py`.
2. Secrets path: `tests/sandbox/.secrets/life_sim_users_creds_<generation_id>.json`.
3. Gitignore: `tests/sandbox/.secrets/` in gateway `.gitignore` + nested ignore.
4. **As-of-Done (P3):** unit tests cover strength + path hygiene; secrets never staged.

## Gap
**As-of-Done (P3):** closed.

## Acceptance / DoD
- [x] Passwords via Python `secrets`, length ≥24 (AC-02)
- [x] Creds only under gitignored `.secrets/` with `generation_id`
- [x] No secrets staged/committed
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/.secrets/` + gateway/root `.gitignore` (P3)
- Provision script secrets writer

## Out of scope
OTP verify (T03); replay wire (T04); invent OTP HTTP; commit credentials.
- Overlay bans:
  - Stay `dev`.
  - 200 users 1:1; CSPRNG ≥24; gitignored secrets; supersede pool M=20; rate-limit pacing; K1 no SPA resident login.
  - OTP via Identity `SMS_PROVIDER=file` disk outbox — **no invent** `GET /dev/last-otp`.
  - Pointer pkg-000104; do not mutate pkg-000100…103.
  - No invent OTP HTTP; no pilot Telnyx; no regenerate fixtures; never commit secrets.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
rg -n '\.secrets' doge-complaints-gateway/.gitignore /Users/eslinko/Development/DOGEstonia/.gitignore || true
# after P3: git check-ignore -v doge-complaints-gateway/tests/sandbox/.secrets/life_sim_users_creds_example.json || true
# git status --ignored | head -20
```
