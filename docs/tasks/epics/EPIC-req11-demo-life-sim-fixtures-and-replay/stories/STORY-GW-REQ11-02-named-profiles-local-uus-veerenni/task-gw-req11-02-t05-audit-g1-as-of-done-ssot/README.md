# task-gw-req11-02-t05-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G1)

## Meta
- **Story:** [STORY-GW-REQ11-02](../STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000101 (parent product AC Done); wave `run_mode=gw_req11_02_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-REQ11-02
- **Depends on:** T01–T04 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-02-named-profiles-2026-09-29.md`](../../../../../../analysis/audit-gw-req11-02-named-profiles-2026-09-29.md) **G1**
- **Scaffolded:** 2026-09-29T14:06:00Z
- **Completed:** 2026-09-29T14:08:13Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_02_gap_20260929T140514Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T01–T03 README Code Facts/Gap still present-tense pre-P3 («Absent» / Gap open) while profiles + selection note live. Docs-only As-of-Done vs Historical. No product reopen. G2 WAIVED operator (no §Актуальная точка rewrite).

## Code Facts
1. Audit G1 — T01–T03 present-tense absence (pre-P6).
2. Live product — `tests/sandbox/profiles/{local,uus-veerenni,index}.json` + `demo_life_sim_profiles.py`; note on disk.
3. Pipeline / backlog §Verified already **Present**.
4. **As-of-Done (P6 2026-09-29T14:08:13Z):** G1 CLOSED — T01–T03 split As-of-Done vs Historical.
5. Pointer stays pkg-000101; product Story Done (AC-01…03 under gate framing).

## Gap
**G1 CLOSED:** present-tense pre-P3 absence only in Historical rows.

## Acceptance / DoD
- [x] T01 README Code Facts/Gap: Historical absence vs As-of-Done `local.json` + ports
- [x] T02 README Code Facts/Gap: Historical vs As-of-Done `uus-veerenni.json` env refs
- [x] T03 README Gap: Historical vs As-of-Done selection note + `DEMO_LIFE_SIM_PROFILE`
- [x] T04 product gate **не** reopen
- [x] Product profiles/tests not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000101
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-req11-02-t05.md` signed (P6)

## Where to change
- T01–T03 Code Facts/Gap (done)
- Bullrun T05 row + P6 registry (on close)

## Out of scope
Product reopen; replay (REQ11-03); invent APIs; literal secrets; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000101 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|Absent|local.json|uus-veerenni|DEMO_LIFE_SIM_PROFILE' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/task-gw-req11-02-t01-profile-local-five/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/task-gw-req11-02-t02-profile-uus-veerenni-deploy/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/task-gw-req11-02-t03-env-refs-and-selection-doc/README.md
ls doge-complaints-gateway/tests/sandbox/profiles/
```
