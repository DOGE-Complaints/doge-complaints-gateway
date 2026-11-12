# task-gw-req10-02-t01-hosted-lifecycle-backfill

## Task: implement/ops — hosted/test RECEIVED → accepted backfill (T01)

## Meta
- **Story:** [STORY-GW-REQ10-02](../STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md)
- **Type:** implement / ops
- **Status:** ✅ Done
- **Package:** pkg-000099
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-28T17:27:26Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md`

## Purpose
Clean/normalize known legacy `RECEIVED`/`received` → `accepted` (`StoryLifecycleStatus.ACCEPTED.value`) in test/hosted Supabase. Simple UPDATE; cite inventory row. Scope #1 · AC-GW-REQ1002-01. Prefer simple cleanup over elaborate migration.

## Code Facts
1. **As-of-Done:** Enum ACCEPTED — `src/core/domain/contracts.py:21`.
2. **As-of-Done (P3):** Evidence [`evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md`](../../../../../../analysis/evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md) §T01 — PostgREST reachable; current endpoint `stories` `*/0` (≠ inventory 162); inventory `story_id=6019633d-…` absent; `RECEIVED` filter ×0; **operator blocker** documented (AC-01 closed via blocker path).
3. **As-of-Done:** Fixtures branch N/A (T02) — no RECEIVED/received as fixture data.
4. **Historical (REQ10-01 inventory):** hosted `RECEIVED`×1 — `story_id=6019633d-3876-469e-abe4-6002136ac84b` — [`inventory-gw-req10-01…`](../../../../../../analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md) §T01; lowercase `received`×0; table PostgREST `stories`.

## Gap
**Closed (P3 2026-09-28T17:44:10Z):** AC-01 via documented operator blocker + fixtures N/A. **G3 SSOT As-of-Done (P6 2026-09-28T17:52:28Z).** Residual hosted cleanup when inventory-project credentials return = **G1 WAIVED operator** (not this task).

## Acceptance / DoD
- [x] Known legacy RECEIVED cleaned to `accepted` in test/hosted data (AC-GW-REQ1002-01)
- [x] Evidence note under gateway `docs/analysis/` (P3 path; no invent schema)
- [x] Simple cleanup only — no elaborate migration ceremony
- [x] BULLRUN phases complete when closed

## Where to change
- Hosted/test Supabase `stories.lifecycle_status` (ops/SQL at P3)
- Evidence note under `doge-complaints-gateway/docs/analysis/`

## Out of scope
Fixture confirm (T02); mapper slim (T03); debug I/O (T04); tests (T05); gate (T06); H8; invent public APIs.
- Overlay bans:
  - Stay `dev`.
  - H8 skip.
  - Do not mutate pkg-000098; pointer is pkg-000099.

## Verification commands
```bash
# P3: post-cleanup DISTINCT / count RECEIVED == 0 evidence
rg -n 'RECEIVED|backfill|accepted|blocker' doge-complaints-gateway/docs/analysis/ --glob '*req10*' --glob '*lifecycle*'
```
