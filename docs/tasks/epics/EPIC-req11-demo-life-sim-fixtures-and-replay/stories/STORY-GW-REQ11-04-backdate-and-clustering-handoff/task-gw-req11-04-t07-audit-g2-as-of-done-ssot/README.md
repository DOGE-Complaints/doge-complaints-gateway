# task-gw-req11-04-t07-audit-g2-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G2)

## Meta
- **Story:** [STORY-GW-REQ11-04](../STORY-GW-REQ11-04-backdate-and-clustering-handoff.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000103 (parent product AC Done); wave `run_mode=gw_req11_04_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-REQ11-04
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md`](../../../../../../analysis/audit-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md) **G2**
- **Scaffolded:** 2026-09-29T14:44:38Z
- **Completed:** 2026-09-29T14:46:20Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_04_gap_20260929T144351Z.plan.md` G2 TASKED follow_up=none

## Purpose
Закрыть G2 (LOW): T01–T05 README Code Facts / Gap still present-tense «Absent» while Status/DoD = Done and product lock-B + docs shipped. Docs-only As-of-Done vs Historical. No product reopen. G1/G3 WAIVED operator (no invent pool secrets; no §Актуальная точка rewrite).

## Code Facts
1. Audit G2 — T01–T05 Code Facts present-tense Absent (pre-P6).
2. Live product — `PATCH /ops/stories/{id}/created-at`; `update_created_at`; `patch_story_created_at_http`; `--life-sim` backdate; wait script + note T04/T05.
3. Gate PASS 2026-09-29T14:39:37Z; live pool env 0/20 = G1 WAIVED operator.
4. **As-of-Done (P6 2026-09-29T14:46:20Z):** G2 CLOSED — T01–T05 split As-of-Done vs Historical.
5. Pointer stays pkg-000103; product Story Done (AC-01…03 under gate framing + blocker).

## Gap
**G2 CLOSED:** present-tense pre-P3 «Absent» only in Historical rows of T01–T05.

## Acceptance / DoD
- [x] T01 README Code Facts/Gap: Historical absence vs As-of-Done stamp evidence note
- [x] T02 README Code Facts/Gap: Historical vs As-of-Done lock-B `PATCH /ops/stories/{id}/created-at`
- [x] T03 README Code Facts/Gap: Historical vs As-of-Done runner `patch_story_created_at_http`
- [x] T04 README Code Facts/Gap: Historical vs As-of-Done clustering wait note/script
- [x] T05 README Code Facts/Gap: Historical vs As-of-Done K3 note
- [x] T06 product gate **не** reopen
- [x] Product tooling/tests not reopened; no invent `LIFE_SIM_POOL_*` secrets (G1 WAIVED)
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] `current.yaml` stays pkg-000103
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-04-t07.md` signed (P6)

## Where to change
- T01–T05 Code Facts/Gap (done)
- Bullrun T07 row + P6 registry (on close)

## Out of scope
Product reopen; invent pool secrets / live bootstrap (G1 WAIVED); invent APIs; §Актуальная точка rewrite (G3 WAIVED); G4 note pointer (T08).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000103 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|Absent|created-at|lock.B|life_sim_wait' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/task-gw-req11-04-t01-created-at-stamp-evidence/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/task-gw-req11-04-t02-lock-b-service-auth-backdate/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/task-gw-req11-04-t03-replay-apply-fixture-timestamps/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/task-gw-req11-04-t04-clustering-wait-runbook/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/task-gw-req11-04-t05-k3-card-count-follows-clustering/README.md
```
