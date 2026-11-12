# task-gw-req57-03-t08-audit-g4-t03-asgi-line-refs

## Task: docs — T03 ASGI line-ref SSOT (G4)

## Meta
- **Story:** [STORY-GW-REQ57-03](../STORY-GW-REQ57-03-sweep-retry-sense-brief.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000115 (parent product AC Done); wave `run_mode=gw_req57_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ57-03
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`../../../../../../analysis/audit-gw-req57-03-sweep-retry-sense-brief-2026-10-15.md`](../../../../../../analysis/audit-gw-req57-03-sweep-retry-sense-brief-2026-10-15.md) **G4**
- **Scaffolded:** 2026-10-15T12:08:59Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req57_03_gap_20261015T120749Z.plan.md` G4 TASKED follow_up=none

## Purpose
Close G4 (LOW): T03 Meta AC-trace / Purpose still cite `asgi_app.py` ~194–220 (cluster cron band) while sweep wire is **~229–265** + nudge-enabled gate. Align T03 README (+ backlog Nested T03 Arch/AC if same drift). Product T01–T06 AC **не** reopen. G2/G3 WAIVED.

## Code Facts
### Live (post-P6 close) — 2026-10-15T12:11:38Z
1. T03 AC-trace/Purpose → ~229–265 nudge-enabled gate.
2. Backlog Nested T03 Arch/AC → ~229–265.
3. Product code/tests unchanged by T08 (docs-only beyond suite from T07).

## Gap
Closed in P6 (docs SSOT).

## Acceptance / DoD
- [x] T03 Meta AC-trace / Purpose / Verification cite sweep band ~229–265 + nudge-enabled gate
- [x] Backlog Nested T03 Arch/AC aligned if drifted
- [x] No invent AC; product gate T01–T06 **не** reopen
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] current.yaml stays pkg-000115
- [x] BULLRUN phases complete when closed
- [x] acceptance-verification-gw-req57-03-t08.md signed (P6)

## Done
- **Closed:** 2026-10-15T12:11:38Z (P6 `gw_req57_03_audit_followup`)

## Where to change
- `…/task-gw-req57-03-t03-asgi-cron-wire/README.md`
- `…/backlog-stories/…/STORY-GW-REQ57-03-sweep-retry-sense-brief.md` (Nested T03 row)

## Out of scope
Lifespan test (T07); mutate pkg-000115; rewrite §Актуальная точка

## Verification commands
```bash
rg -n "194–220|229–265|nudge-enabled|SenseBriefSweep" doge-complaints-gateway/docs/tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/task-gw-req57-03-t03-asgi-cron-wire/README.md doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md | head -40
```
