# task-gw-req11-05-t05-operator-docs-preconditions

## Task: docs — operator docs preconditions (T05)

## Meta
- **Story:** [STORY-GW-REQ11-05](../STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-09-29T18:15:05Z
- **Package:** pkg-000104
- **Skill declared:** python-pro
- **Depends on:** T01–T04 soft (can draft alongside)
- **Scaffolded:** 2026-09-29T18:09:49Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md`

## Purpose
Docs: Identity `SMS_PROVIDER=file`, outbox path, Supabase env, rate-limit pacing, secrets hygiene; pool M=20 deprecated for new Pass. Scope #5,#10 · AC-GW-REQ1105-05.

## Code Facts
1. Note Present: `docs/analysis/note-gw-req11-05-provision-fixture-users-identity-2026-09-29.md`.
2. Documents SMS_PROVIDER=file, outbox, Supabase, pacing, secrets hygiene, pool deprecated, 429 blocker.

## Gap
**As-of-Done (P3):** closed.

## Acceptance / DoD
- [x] Docs list SMS_PROVIDER=file, outbox, Supabase env, pacing, never-commit secrets (AC-05)
- [x] Pool M=20 marked deprecated for new Pass
- [x] BULLRUN phases complete when closed

## Where to change
- `docs/analysis/` note (P3); soft INDEX/bullrun pointers only as needed

## Out of scope
Implement provision; invent OTP HTTP; rewrite §Актуальная точка.
- Overlay bans:
  - Stay `dev`.
  - 200 users 1:1; CSPRNG ≥24; gitignored secrets; supersede pool M=20; rate-limit pacing; K1 no SPA resident login.
  - OTP via Identity `SMS_PROVIDER=file` disk outbox — **no invent** `GET /dev/last-otp`.
  - Pointer pkg-000104; do not mutate pkg-000100…103.
  - No invent OTP HTTP; no pilot Telnyx; no regenerate fixtures; never commit secrets.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
ls doge-complaints-gateway/docs/analysis/note-gw-req11-0*.md | tail -5
# after P3: rg -n 'SMS_PROVIDER=file|FILE_SMS_OUTBOX|generation_id|deprecated' doge-complaints-gateway/docs/analysis/note-gw-req11-05*.md | head -40
```
