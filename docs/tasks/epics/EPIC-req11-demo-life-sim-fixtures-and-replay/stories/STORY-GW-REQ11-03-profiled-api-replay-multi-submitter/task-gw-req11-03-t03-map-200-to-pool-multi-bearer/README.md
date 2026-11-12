# task-gw-req11-03-t03-map-200-to-pool-multi-bearer

## Task: implement — map 200 fixtures → pool + multi-Bearer (T03)

## Meta
- **Story:** [STORY-GW-REQ11-03](../STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Package:** pkg-000102
- **Skill declared:** python-pro
- **Depends on:** T01 (fixtures), T02 (pool)
- **Scaffolded:** 2026-09-29T14:13:56Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md`

## Purpose
Map **200** fixture users → pool M=20; extend Bearer resolve beyond single `GATEWAY_USER_EMAIL`/`PASSWORD`. Scope #2 · AC-GW-REQ1103-03.

## Code Facts
1. Single Bearer legacy: `resolve_user_bearer_token` (canvas path).
2. **As-of-Done (P3/P6):** `life_sim_fixture_to_pool_map_v0_1.json` (200→20, 10/slot); `resolve_pool_slot_bearer_token`; `--life-sim` multi-Bearer.
3. Lock: map 200 → pool 20 (INDEX).
4. **Historical (pre-P3):** Multi-fixture submitters / pool map **Absent**; runner assumed one user token only.

## Gap
**As-of-Done (P3):** closed — map + multi-Bearer; see gate + run-summary.  
**Historical:** No deterministic map from 200 fixture users to 20 pool identities; no multi-Bearer path.

## Acceptance / DoD
- [x] 200 fixture users map onto pool M=20 (AC-GW-REQ1103-03)
- [x] Replay can obtain Bearer per mapped pool user (not only one env pair)
- [x] BULLRUN phases complete when closed

## Where to change
- Extend `tests/simulation_intake_http.py` / runner helpers (P3)
- On-disk map artifact under `tests/sandbox/` if needed (P3)

## Out of scope
Pool bootstrap itself (T02); wipe→replay orchestration (T04); SPA login; invent APIs.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000102.
  - No secrets in git.

## Verification commands
```bash
rg -n 'map|pool|fixture_user|Bearer|resolve_user' doge-complaints-gateway/tests --glob '*sim*' --glob '*req11*' | head -40
```
