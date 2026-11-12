# task-gw-req11-06-t07-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G1)

## Meta
- **Story:** [STORY-GW-REQ11-06](../STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-09-30T08:02:52Z
- **Package:** pkg-000105 (parent product AC Done); wave `run_mode=gw_req11_06_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ11-06
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-06-wipe-node-content-stories-derivatives-2026-09-30.md`](../../../../../../analysis/audit-gw-req11-06-wipe-node-content-stories-derivatives-2026-09-30.md) **G1**
- **Scaffolded:** 2026-09-30T08:01:10Z
- **Completed:** 2026-09-30T08:02:52Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_06_gap_20260930T080005Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog §Verified / Code touchpoints still present-tense «Absent» while Status=Done; T01 Code Facts «Target Absent» / «Make Absent». Docs-only As-of-Done vs Historical. G3 WAIVED operator.

## Code Facts
1. Audit G1 — backlog Verified + T01 Code Facts present-tense Absent (pre-P6).
2. Product Present — `life_sim_wipe_node_content.py` + `life_sim_wipe_lib.py`; `make life-sim-wipe-node-content`.
3. Gate PASS 2026-09-30T07:56:35Z; live DELETE 204.
4. **As-of-Done (P6 2026-09-30T08:02:52Z):** G1 CLOSED — backlog §Verified + Code touchpoints As-of-Done vs Historical; T01 Code Facts Present.
5. Pointer stays pkg-000105; product Story Done.

## Gap
**G1 CLOSED:** present-tense pre-P3 «Absent» only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (wipe Present)
- [x] Backlog Code touchpoints: As-of-Done Present + Historical Absent
- [x] T01 Code Facts: Present (not Absent); Gap As-of-Done closed cleanly
- [x] T06 product gate **не** reopen
- [x] Product wipe tooling/tests not reopened; no invent wipe HTTP
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] `current.yaml` stays pkg-000105
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-06-t07.md` signed (P6)

## Where to change
- Backlog `STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md` §Verified / Code touchpoints (done)
- T01 README Code Facts / Gap (done)
- Bullrun T07 row + P6 registry (on close)

## Out of scope
Product/wipe execute; invent wipe HTTP; Identity DELETE; §Актуальная точка rewrite (G3 WAIVED); mutate pkg-000105; G2 manual §8 (T08).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000105 / current.yaml.

## Verification commands
```bash
rg -n 'Absent|As-of-Done|Historical|life_sim_wipe' \
  doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives/task-gw-req11-06-t01-wipe-script-confirm-gate/README.md \
  | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
