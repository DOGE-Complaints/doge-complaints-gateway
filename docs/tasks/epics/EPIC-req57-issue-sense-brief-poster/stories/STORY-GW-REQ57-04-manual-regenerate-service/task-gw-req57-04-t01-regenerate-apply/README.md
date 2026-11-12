# task-gw-req57-04-t01-regenerate-apply

## Task: implement — regenerate apply (T01)

## Meta
- **Story:** [STORY-GW-REQ57-04](../STORY-GW-REQ57-04-manual-regenerate-service.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:23:00Z
- **Package:** pkg-000116
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-15T12:17:03Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md`
- **AC trace:** arch 02 §2.5; AC-GW-REQ5704-01

## Purpose
Bump `generation_version` → pending; keep brief title/summary until new bind; omit public `poster_url` while not ready

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:23:00Z
1. `bump_generation_version` / `mark_regenerate_pending` / `SenseBriefRegenerateService.regenerate` Present.
2. Path: `src/core/application/sense_brief_regenerate.py`.
3. Brief title/summary kept; public `poster_url` omitted while pending (operator lock).

## Gap
**Closed P3 2026-10-15T12:23:00Z.**

## Acceptance / DoD
- [x] Bump `generation_version` and set `generation_status=pending`
- [x] Keep brief title/summary until new bind; public poster omit while not ready
- [x] No invent AC; no citizen regenerate
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-04-t01.md` signed (P3)

## Where to change
- `src/core/application/sense_brief_regenerate.py`

## Out of scope
HTTP route (T02); nudge call (T03); authz reject (T04); tests (T05); gate (T06)

## Verification commands
```bash
rg -n "bump_generation_version|mark_regenerate_pending|SenseBriefRegenerateService" doge-complaints-gateway/src/core/application/sense_brief_regenerate.py
```
