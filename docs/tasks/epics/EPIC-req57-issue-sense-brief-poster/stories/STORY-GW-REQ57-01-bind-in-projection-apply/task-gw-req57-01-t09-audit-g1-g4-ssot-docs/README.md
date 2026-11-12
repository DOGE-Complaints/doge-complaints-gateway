# task-gw-req57-01-t09-audit-g1-g4-ssot-docs

## Task: docs — backlog SSOT As-of-Done + T06 Where align (G1+G4)

## Meta
- **Story:** [STORY-GW-REQ57-01](../STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000113 (parent product AC Done); wave `run_mode=gw_req57_01_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ57-01
- **Depends on:** T01–T08 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req57-01-bind-in-projection-apply-2026-10-15.md`](../../../../../../analysis/audit-gw-req57-01-bind-in-projection-apply-2026-10-15.md) **G1, G4**
- **Scaffolded:** 2026-10-15T11:21:05Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req57_01_gap_20261015T111932Z.plan.md` G1, G4 TASKED follow_up=none

## Purpose
Close G1+G4 (LOW): backlog story §Verified still Absent/Planned vs Meta Done; Nested tasks Planned; Code touchpoints still cite extraction_policy for brief-wins. T06 README §Where to change still extraction_policy while As-of-Done is sense_brief_bind + issue_create. Mirror pipeline As-of-Done/Historical. Product T01–T08 AC **не** reopen. G2 WAIVED operator.

## Code Facts
### Live (post-P6 close) — 2026-10-15T11:24:48Z
1. Backlog STORY-GW-REQ57-01 Meta Status → As-of-Done (Historical); Nested Status → Done; touchpoints include sense_brief_bind.py (claims: backlog file).
2. Nested STORY + T06 Where/Verification → sense_brief_bind.py + issue_create.py (claims: nested README/story).
3. Product code/tests unchanged by T09 (docs-only).
## Gap
Closed in P6 (docs SSOT).

## Acceptance / DoD
- [x] Backlog §Verified As-of-Done vs Historical; Nested T01–T08 Done; Code touchpoints match product paths
- [x] T06 README Where + verify cmd → sense_brief_bind / issue_create (not extraction_policy brief-wins)
- [x] T01–T08 product gate **не** reopen; no invent AC
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] current.yaml stays pkg-000113
- [x] BULLRUN phases complete when closed
- [x] acceptance-verification-gw-req57-01-t09.md signed (P6)

## Done
- **Closed:** 2026-10-15T11:25:34Z (P6 `gw_req57_01_audit_followup`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md`
- `…/task-gw-req57-01-t06-brief-wins-guard/README.md`

## Out of scope
Rewrite §Актуальная точка (G2); mutate pkg-000113; reopen product AC; implement G3/G5 tests (T10/T11)

## Verification commands
```bash
rg -n "Absent|Planned|extraction_policy|sense_brief_bind|Where to change" doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md doge-complaints-gateway/docs/tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-01-bind-in-projection-apply/task-gw-req57-01-t06-brief-wins-guard/README.md | head -40
```
