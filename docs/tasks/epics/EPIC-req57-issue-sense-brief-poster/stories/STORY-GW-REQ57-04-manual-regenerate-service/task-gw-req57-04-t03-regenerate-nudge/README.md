# task-gw-req57-04-t03-regenerate-nudge

## Task: implement — regenerate nudge (T03)

## Meta
- **Story:** [STORY-GW-REQ57-04](../STORY-GW-REQ57-04-manual-regenerate-service.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:23:00Z
- **Package:** pkg-000116
- **Skill declared:** python-pro
- **Depends on:** T01, T02
- **Scaffolded:** 2026-10-15T12:17:03Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md`
- **AC trace:** arch 02 §2.5; AC-GW-REQ5704-01; AC-GW-REQ5704-04

## Purpose
Call nudge client 02 with new `generation_version` (new peer idempotency key)

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:23:00Z
1. `SenseBriefRegenerateService.regenerate` calls `nudge_service.nudge(..., generation_version=new_version)`.
2. Reuses `sense_brief_nudge.py` from REQ57-02.

## Gap
**Closed P3 2026-10-15T12:23:00Z.**

## Acceptance / DoD
- [x] After version bump + pending, call nudge with new `generation_version`
- [x] New version is distinct peer idempotency key (AC-5704-04)
- [x] Reuse 02 client; no invent peer path
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-04-t03.md` signed (P3)

## Where to change
- `src/core/application/sense_brief_regenerate.py` · reuse `sense_brief_nudge.py`

## Out of scope
Route auth (T02); citizen reject tests (T04); suite (T05); gate (T06)

## Verification commands
```bash
rg -n "nudge_service.nudge|generation_version" doge-complaints-gateway/src/core/application/sense_brief_regenerate.py
```
