# task-gw-req11-09-t03-secrets-actors-handoff-seed

## Task: implement / tooling — secrets actors + handoff + seed call (T03)

## Meta
- **Story:** [STORY-GW-REQ11-09](../STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:52:44Z
- **Package:** pkg-000107
- **Skill declared:** python-pro
- **Depends on:** T01, T02
- **Scaffolded:** 2026-10-01T10:45:33Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md`

## Purpose
Actors from secrets by `fixture_user_id`; handoff `issue_id`+`density`; call Present `seed_representative_issues`; never pack JSON write; never service-token actors. Scope #4–#7 · AC-02/03/04/06.

## Code Facts
**As-of-Done (P3 2026-10-01T10:52:44Z):**
1. Handoff parse: `handoffs_from_issue_rows` / `density_from_issue_row` (`density`|`story_count`|`len(story_ids)`|None).
2. Actors: `load_users_creds_index` + `resolve_fixture_user_bearer_token`; `refuse_service_token_as_actor`.
3. Live seed path: `closed.seed_representative_issues(httpx.Client(threads), handoffs, actors)`.
4. Import via file path (avoid gateway `core` shadow). Never mutates pack JSON.
5. **Leftover:** live full seed not run — local `GET /node/issues` empty after cluster wait; documented fail-closed (no invent cluster).

### Historical (scaffold / pre-P3)
Operator wiring Absent.

## Gap
**As-of-Done:** closed for implement; live full seed leftover until non-empty issues.

## Acceptance / DoD
- [x] Calls Present `seed_representative_issues` (AC-02)
- [x] Actors = Bearer from secrets by `fixture_user_id`; not service token (AC-03)
- [x] Handoff `issue_id` + `density` from node/issues (AC-04)
- [x] Never writes pack JSON (AC-06)
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_seed_threads.py` · `life_sim_seed_threads_lib.py`

## Out of scope
Invent Closed APIs / force-cluster; Auth provision; pack mutate.

## Verification commands
```bash
rg -n 'seed_representative_issues|refuse_service_token|fixture_user_id' doge-complaints-gateway/tests/sandbox/life_sim_seed_threads*.py
```
