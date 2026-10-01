# task-gw-req11-09-t07-audit-g2-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G2)

## Meta
- **Story:** [STORY-GW-REQ11-09](../STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-01T11:00:11Z
- **Package:** pkg-000107 (parent product AC Done); wave `run_mode=gw_req11_09_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ11-09
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-09-operator-threads-seed-after-cluster-2026-10-01.md`](../../../../../../analysis/audit-gw-req11-09-operator-threads-seed-after-cluster-2026-10-01.md) **G2**
- **Scaffolded:** 2026-10-01T10:58:33Z
- **Completed:** 2026-10-01T11:00:11Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_09_gap_20261001T105733Z.plan.md` G2 TASKED follow_up=none

## Purpose
Закрыть G2 (LOW): backlog §Verified still present-tense «Absent» (CLI/Make/B-THR-CLI) while Meta Status=Done and artifacts Present. Docs-only As-of-Done vs Historical (mirror REQ11-08 T08). Pipeline already splits As-of-Done vs Historical. G1/G3 WAIVED operator.

## Code Facts
1. Audit G2 — backlog §Verified (as-of 10:18) claims Operator CLI/Make **Absent**, B-THR-CLI open (pre-P6).
2. Product Present — `life_sim_seed_threads.py` + Make + RU manual; B-THR-CLI Closed (disk-verified P4/P6).
3. Gate PASS 2026-10-01T10:52:44Z; offline tests 9 passed.
4. **As-of-Done (P6 2026-10-01T11:00:11Z):** G2 CLOSED — backlog §Verified + Code touchpoints As-of-Done vs Historical.
5. Pointer stays pkg-000107; product Story Done; G1 WAIVED (live full seed leftover); G3 WAIVED (§Актуальная точка).

## Gap
**G2 CLOSED:** present-tense pre-P3 «Absent» only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (CLI/Make/RU/B-THR-CLI Present)
- [x] Code touchpoints table Present-tense matches disk
- [x] T06 product gate **не** reopen
- [x] Product seed CLI/tests not reopened; no invent force-cluster; no live full seed this task
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] G1 remains WAIVED operator (no task reopen)
- [x] `current.yaml` stays pkg-000107
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-09-t07.md` signed (P6)

## Where to change
- Backlog `STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md` §Verified / Code touchpoints (done)
- Soft sync INDEX note (done)
- Bullrun T07 row status on close (done)

## Out of scope
Live full seed after cluster (G1 WAIVED); invent force-cluster; mutate pack JSON; rewrite §Актуальная точка (G3 WAIVED); mutate pkg-000107; product code execute.
- Overlay bans:
  - Stay `dev`.
  - Safe-override only; do not change `gateway-active-package.current.yaml`.

## Verification commands
```bash
rg -n "As-of-Done|Historical|Absent|B-THR-CLI|life_sim_seed_threads" doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```
