# task-gw-req11-01-t06-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G1)

## Meta
- **Story:** [STORY-GW-REQ11-01](../STORY-GW-REQ11-01-fixtures-users-stories-scale.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000100 (parent product AC Done); wave `run_mode=gw_req11_01_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-REQ11-01
- **Depends on:** T01–T05 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-01-fixtures-users-stories-scale-2026-09-29.md`](../../../../../../analysis/audit-gw-req11-01-fixtures-users-stories-scale-2026-09-29.md) **G1**
- **Scaffolded:** 2026-09-29T13:48:54Z
- **Completed:** 2026-09-29T13:50:53Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_01_gap_20260929T134755Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog §Verified + T01–T04 README Code Facts/Gap still present-tense pre-P3 («Absent» / Gap open) while fixtures+note live. Docs-only As-of-Done vs Historical. No product reopen. G2 WAIVED operator (no §Актуальная точка rewrite).

## Code Facts
1. Audit G1 — backlog §Verified + T01–T04 present-tense absence (pre-P6).
2. Live product — users 200 / stories 1661 / mean 8.305 / langs 0.602·0.2926·0.1054 / mass 0.2498·0.7502; note on disk.
3. Pipeline §Verified already As-of-Done + Historical.
4. **As-of-Done (P6 2026-09-29T13:50:53Z):** G1 CLOSED — backlog + T01–T04 split As-of-Done vs Historical.
5. Pointer stays pkg-000100; product Story Done (AC-01…04 under gate framing).

## Gap
**G1 CLOSED:** present-tense pre-P3 absence only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (cite live fixture paths; no present-tense «Absent»)
- [x] T01 README Code Facts/Gap: Historical absence vs As-of-Done fixtures on disk
- [x] T02 README Code Facts/Gap: Historical vs As-of-Done measurable 60/30/10
- [x] T03 README Code Facts/Gap: Historical vs As-of-Done 2026 curve / mass
- [x] T04 README Gap: Historical vs As-of-Done canvas relation note path
- [x] T05 product gate **не** reopen
- [x] Product fixtures/tests not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000100
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-req11-01-t06.md` signed (P6)

## Where to change
- backlog §Verified; T01–T04 Code Facts/Gap (done)
- Bullrun T06 row + P6 registry (on close)

## Out of scope
Product reopen; regenerate fixtures; invent APIs; profiles/replay/backdate; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000100 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|Absent|life_sim' \
  doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/task-gw-req11-01-t01-users-stories-scale-fixtures/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/task-gw-req11-01-t02-language-mix-60-30-10/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/task-gw-req11-01-t03-timestamps-2026-exp-curve/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/task-gw-req11-01-t04-canvas-relation-doc/README.md
ls doge-complaints-gateway/tests/sandbox/dogestonia_life_sim_*_v0_1.json
```
