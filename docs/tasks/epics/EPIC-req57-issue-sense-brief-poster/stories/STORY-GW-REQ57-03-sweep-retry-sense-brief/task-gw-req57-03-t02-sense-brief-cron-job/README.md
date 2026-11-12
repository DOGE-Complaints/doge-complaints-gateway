# task-gw-req57-03-t02-sense-brief-cron-job

## Task: implement — sense-brief cron job (T02)

## Meta
- **Story:** [STORY-GW-REQ57-03](../STORY-GW-REQ57-03-sweep-retry-sense-brief.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:03:07Z
- **Package:** pkg-000115
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-10-15T11:57:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md`
- **AC trace:** arch 02 §2.4; AC-GW-REQ5703-01

## Purpose
Cron-class (precedent `ClusterCronJob`) — re-nudge via client from 02

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:03:07Z
1. `SenseBriefSweepService.run_once` re-nudges eligible via `SenseBriefNudgeService` (same `generation_version`).
2. `SenseBriefSweepCronJob` Present — ClusterCronJob-style thread loop.
3. Paths: `sense_brief_sweep.py`, `scheduler/sense_brief_sweep_cron.py`.

## Gap
**Closed P3 2026-10-15T12:03:07Z.**

## Acceptance / DoD
- [x] Cron-class job selects eligible Issues (T01) and re-nudges via 02 client
- [x] Reuses locked env / fail-closed nudge behavior; no invent peer URL
- [x] Prefer same `generation_version` re-nudge (idempotent); no silent version bump for 04
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-03-t02.md` signed (P3)

## Where to change
- `src/core/application/sense_brief_sweep.py`
- `src/core/scheduler/sense_brief_sweep_cron.py`

## Out of scope
ASGI start/stop (T03); ready overwrite guard detail (T04); tests (T05); gate (T06)

## Verification commands
```bash
rg -n "SenseBriefSweepCronJob|SenseBriefSweepService" doge-complaints-gateway/src/core
```
