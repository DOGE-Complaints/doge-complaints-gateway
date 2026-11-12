# task-gw-req11-03-t02-pool-bootstrap-m20

## Task: implement — admin-bootstrap pool M=20 (T02)

## Meta
- **Story:** [STORY-GW-REQ11-03](../STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Package:** pkg-000102
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-29T14:13:56Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md`

## Purpose
Admin-bootstrap pool **M=20** verified users for multi-submitter replay. Scope #2 · AC-GW-REQ1103-03. Design at P3; env refs; **no invent public resident APIs**.

## Code Facts
1. Single Bearer legacy path: `resolve_user_bearer_token` — `tests/simulation_intake_http.py` (still present for canvas mode).
2. 403 messaging assumes `phone_verified`.
3. Operator lock: pool M=20 admin-bootstrapped verified users (INDEX).
4. **As-of-Done (P3/P6):** `tests/sandbox/life_sim_pool_m20.json` — 20 slots; env refs `LIFE_SIM_POOL_NN_EMAIL`/`PASSWORD` only; no secrets in git.
5. **Historical (pre-P3):** Multi-fixture submitters / pool manifest **Absent**.

## Gap
**As-of-Done (P3):** closed — pool M=20 manifest + env-ref design; see gate + run-summary.  
**Historical:** No admin-bootstrapped pool of 20 verified users for replay submitters.

## Acceptance / DoD
- [x] Pool of M=20 verified users obtainable for replay (AC-GW-REQ1103-03 prep)
- [x] Secrets/credentials via env refs only (no secrets in git)
- [x] No invent public resident login APIs
- [x] BULLRUN phases complete when closed

## Where to change
- Tests/tooling bootstrap helper (P3 design); env template refs only
- Do not invent undocumented public HTTP for resident SPA login

## Out of scope
Map 200→pool (T03); wipe→replay (T04); SPA login product path; backdate.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000102.
  - No secrets in git.

## Verification commands
```bash
rg -n 'pool|M=20|bootstrap|phone_verified|GATEWAY_USER' doge-complaints-gateway/tests doge-complaints-gateway/docs --glob '*req11*' --glob '*sim*' | head -40
```
