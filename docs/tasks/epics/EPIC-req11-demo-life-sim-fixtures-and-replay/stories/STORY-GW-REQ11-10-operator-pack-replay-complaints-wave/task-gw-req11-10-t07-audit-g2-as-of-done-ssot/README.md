# task-gw-req11-10-t07-audit-g2-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G2)

## Meta
- **Story:** [STORY-GW-REQ11-10](../STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-01T11:41:52Z
- **Package:** pkg-000108 (parent product AC Done); wave `run_mode=gw_req11_10_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ11-10
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-10-operator-pack-replay-complaints-wave-2026-10-01.md`](../../../../../../analysis/audit-gw-req11-10-operator-pack-replay-complaints-wave-2026-10-01.md) **G2**
- **Scaffolded:** 2026-10-01T11:40:22Z
- **Completed:** 2026-10-01T11:41:52Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_10_gap_20261001T113937Z.plan.md` G2 TASKED follow_up=none

## Purpose
Закрыть G2 (LOW): backlog (+ pipeline) §Verified still present-tense «Absent» (wave-state / RU pack-wave / Make fail-closed narrative) while Meta Status=Done and artifacts Present. Docs-only As-of-Done vs Historical (mirror REQ11-08 T08 / REQ11-09 T07). G1/G3 WAIVED operator.

## Code Facts
1. Audit G2 — backlog §Verified (as-of 11:24) claims wave-state / RU pack-wave **Absent**; Make simulate not fail-closed as sole narrative (pre-P6).
2. Product Present — `life_sim_replay_pack_wave.py` + Make + RU manual + `ReplayWaveStore`; offline 8 (disk-verified P4/P6).
3. Gate PASS 2026-10-01T11:35:43Z; dry-run LIMIT=2 ok.
4. **As-of-Done (P6 2026-10-01T11:41:52Z):** G2 CLOSED — backlog + pipeline §Verified / Code touchpoints As-of-Done vs Historical.
5. Pointer stays pkg-000108; product Story Done; G1 WAIVED (live Tunnel 403 leftover); G3 WAIVED (§Актуальная точка).

## Gap
**G2 CLOSED:** present-tense pre-P3 «Absent» only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (CLI/Make/RU/wave Present)
- [x] Pipeline §Verified / Code touchpoints Present-tense matches disk (optional soft sync)
- [x] T06 product gate **не** reopen
- [x] Product replay CLI/tests not reopened; no invent intake/force-cluster; no live full pack this task
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] G1 remains WAIVED operator (no task reopen)
- [x] `current.yaml` stays pkg-000108
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-10-t07.md` signed (P6)

## Where to change
- Backlog `STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md` §Verified / Code touchpoints (done)
- Pipeline story §Verified soft sync (done)
- Bullrun T07 row status on close (done)

## Out of scope
Live full/LIMIT pack submit (G1 WAIVED); invent intake/force-cluster; mutate pack JSON; rewrite §Актуальная точка (G3 WAIVED); mutate pkg-000108; product code execute.
- Overlay bans:
  - Stay `dev`.
  - Safe-override only; do not change `gateway-active-package.current.yaml`.

## Verification commands
```bash
rg -n "As-of-Done|Historical|Absent|life_sim_replay_pack_wave|LIFE_SIM_PACK_DIR" doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```
