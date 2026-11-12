# task-gw-req11-04-t03-replay-apply-fixture-timestamps

## Task: implement / tooling — replay apply fixture timestamps (T03)

## Meta
- **Story:** [STORY-GW-REQ11-04](../STORY-GW-REQ11-04-backdate-and-clustering-handoff.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-29T14:39:37Z
- **Package:** pkg-000103
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-09-29T14:33:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md`

## Purpose
Extend life-sim / simulation helpers so fixture `created_at` survives via lock-B after stash→submit. Scope #1 · AC-GW-REQ1104-01. Depends on T02.

## Code Facts
1. REQ11-03 `--life-sim` + `post_stash_and_submit_http` Present.
2. Fixture stories carry `created_at` in life-sim JSON (REQ11-01).
3. **As-of-Done (P3):** Replay applies fixture timestamps via B — `patch_story_created_at_http` after stash→submit in `simulation_runner.main_life_sim`.
4. **Historical (pre-P3):** Replay apply fixture timestamps via B Absent.

## Gap
**As-of-Done (P3):** closed — runner applies fixture times via lock B after submit (live E2E still pool-blocker).  
**Historical:** Runner does not apply fixture timestamps via lock B after submit.

## Acceptance / DoD
- [x] After stash→submit, fixture times applied via B (or documented blocker)
- [x] Extends existing runner/HTTP helpers where fit
- [x] No invent public intake fields
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/simulation_runner.py`, `tests/simulation_intake_http.py`, life_sim helpers (P3)

## Out of scope
Threads seed; spa verify; public intake timestamp invent; SQL dump Pass; invent public/cluster APIs; reopen REQ11-01…03 product.
- Overlay bans:
  - Stay `dev`.
  - Lock **B**: service-auth after stash→submit; **no invent** public intake timestamp fields.
  - Pointer pkg-000103; do not mutate pkg-000100…102.
  - No threads seed / spa verify / SQL dump Pass; no invent public/cluster APIs.
  - No secrets in git.

## Verification commands
```bash
rg -n 'created_at|life_sim|backdate|--life-sim' doge-complaints-gateway/tests --glob '*sim*' | head -40
```
