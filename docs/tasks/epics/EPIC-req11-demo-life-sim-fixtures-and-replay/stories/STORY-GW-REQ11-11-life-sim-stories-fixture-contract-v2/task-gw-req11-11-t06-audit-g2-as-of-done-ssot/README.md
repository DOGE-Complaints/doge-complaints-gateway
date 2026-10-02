# task-gw-req11-11-t06-audit-g2-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G2)

## Meta
- **Story:** [STORY-GW-REQ11-11](../STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-02T08:58:23Z
- **Package:** pkg-000109 (parent product AC Done); wave `run_mode=gw_req11_11_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ11-11
- **Depends on:** T01–T05 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-11-life-sim-stories-fixture-contract-v2-2026-10-02.md`](../../../../../../analysis/audit-gw-req11-11-life-sim-stories-fixture-contract-v2-2026-10-02.md) **G2**
- **Scaffolded:** 2026-10-02T08:56:49Z
- **Completed:** 2026-10-02T08:58:23Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_11_gap_20261002T085615Z.plan.md` G2 TASKED follow_up=none

## Purpose
Закрыть G2 (LOW): backlog §Verified still present-tense scaffold («as of scaffold» / 6-key Absent contract note) while Meta Status=Done and mapping note Present. Docs-only As-of-Done vs Historical (mirror REQ11-08…10). Pipeline already splits As-of-Done/Historical. G1/G3 WAIVED operator.

## Code Facts
1. Audit G2 — backlog §Verified (scaffold) lacked As-of-Done vs Historical while note Present + gate PASS.
2. Product docs Present — [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md); T01–T05 Done.
3. Gate PASS 2026-10-02T08:53:45Z.
4. **As-of-Done (P6 2026-10-02T08:58:23Z):** G2 CLOSED — backlog §Verified / Code touchpoints As-of-Done vs Historical; pipeline soft Code touchpoints sync.
5. Pointer stays pkg-000109; product Story Done; G1 WAIVED (dirty `life_sim_replay_lib` out-of-DoD); G3 WAIVED (§Актуальная точка).

## Gap
**G2 CLOSED:** present-tense pre-P3 «Absent» / scaffold Verified only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (contract note Present; 6-key pack Historical)
- [x] Soft Code touchpoints if needed
- [x] T05 product gate **не** reopen
- [x] No generator/adapter; no invent AC; no pack regen; no restore lib this task (G1 WAIVED)
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] G1 remains WAIVED (no task reopen)
- [x] `current.yaml` stays pkg-000109
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-11-t06.md` signed (P6)

## Where to change
- Backlog `STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md` §Verified (done)
- Pipeline Code touchpoints soft sync (done)
- Bullrun T06 row status on close (done)

## Out of scope
Restore `life_sim_replay_lib` (G1 WAIVED); invent REQ11-12 implement; rewrite §Актуальная точка (G3 WAIVED); mutate pkg-000109; product code.
- Overlay bans:
  - Stay `dev`.
  - Safe-override only; do not change `gateway-active-package.current.yaml`.

## Verification commands
```bash
rg -n "As-of-Done|Historical|Absent|note-gw-req11-11" doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```
