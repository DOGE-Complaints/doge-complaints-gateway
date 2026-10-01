# task-gw-req11-08-t08-audit-g2-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G2)

## Meta
- **Story:** [STORY-GW-REQ11-08](../STORY-GW-REQ11-08-operator-provision-pack-wave.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:37:50Z
- **Package:** pkg-000106 (parent product AC Done); wave `run_mode=gw_req11_08_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ11-08
- **Depends on:** T01–T07 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-08-operator-provision-pack-wave-2026-10-01.md`](../../../../../../analysis/audit-gw-req11-08-operator-provision-pack-wave-2026-10-01.md) **G2**
- **Scaffolded:** 2026-10-01T10:36:26Z
- **Completed:** 2026-10-01T10:37:50Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_08_gap_20261001T103543Z.plan.md` G2 TASKED follow_up=none

## Purpose
Закрыть G2 (LOW): backlog §Verified still present-tense «Absent» while Meta Status=Done; T01–T04 Code Facts present-tense Absent. Docs-only As-of-Done vs Historical (mirror REQ11-05/06). G1/G3 WAIVED operator.

## Code Facts
1. Audit G2 — backlog Verified + T01–T04 Code Facts present-tense Absent (pre-P6).
2. Product Present — pack-wave CLI/config/wave/RU manual (disk-verified P6).
3. Gate PASS 2026-10-01T10:31:41Z; offline tests 6 passed.
4. **As-of-Done (P6 2026-10-01T10:37:50Z):** G2 CLOSED — backlog §Verified + Code touchpoints As-of-Done vs Historical; T01–T04 Code Facts Present + Historical.
5. Pointer stays pkg-000106; product Story Done; G1 WAIVED operator.

## Gap
**G2 CLOSED:** present-tense pre-P3 «Absent» only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (pack-wave Present)
- [x] T01–T04 Code Facts: Present As-of-Done; pre-P3 Absent only in Historical
- [x] T07 product gate **не** reopen
- [x] Product provision tooling/tests not reopened; no invent OTP HTTP; no live Auth execute this task
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] G1 remains WAIVED operator (no task reopen)
- [x] `current.yaml` stays pkg-000106
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-08-t08.md` signed (P6)

## Where to change
- Backlog `STORY-GW-REQ11-08-operator-provision-pack-wave.md` §Verified / Code touchpoints (done)
- T01–T04 README Code Facts / Gap (done)
- Bullrun T08 row + P6 registry (on close)

## Out of scope
Live Auth provision/wipe (G1 WAIVED); invent OTP HTTP; commit secrets; rewrite §Актуальная точка (G3 WAIVED); mutate pkg-000106; product code execute.
- Overlay bans:
  - Stay `dev`.
  - Safe-override only; do not change `gateway-active-package.current.yaml`.

## Verification commands
```bash
rg -n "As-of-Done|Historical|Absent" doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```
