# task-gw-req11-03-t07-audit-g2-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G2)

## Meta
- **Story:** [STORY-GW-REQ11-03](../STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000102 (parent product AC Done); wave `run_mode=gw_req11_03_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-REQ11-03
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-03-profiled-api-replay-2026-09-29.md`](../../../../../../analysis/audit-gw-req11-03-profiled-api-replay-2026-09-29.md) **G2**
- **Scaffolded:** 2026-09-29T14:26:45Z
- **Completed:** 2026-09-29T14:28:21Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_03_gap_20260929T142541Z.plan.md` G2 TASKED follow_up=none

## Purpose
Закрыть G2 (LOW): T01–T04 README Code Facts still present-tense «Absent» while Gap As-of-Done closed and product tooling shipped. Docs-only As-of-Done vs Historical. No product reopen. G1/G3 WAIVED operator (no invent pool secrets; no §Актуальная точка rewrite).

## Code Facts
1. Audit G2 — T01–T04 Code Facts present-tense Absent (pre-P6).
2. Live product — `life_sim_pool_m20.json`, `life_sim_fixture_to_pool_map_v0_1.json`, `simulation_runner.py --life-sim`, `resolve_pool_slot_bearer_token`.
3. Gate PASS 2026-09-29T14:21:44Z; live pool env 0/20 = G1 WAIVED operator.
4. **As-of-Done (P6 2026-09-29T14:28:21Z):** G2 CLOSED — T01–T04 split As-of-Done vs Historical.
5. Pointer stays pkg-000102; product Story Done (AC-01…04 under gate framing + blocker).

## Gap
**G2 CLOSED:** present-tense pre-P3 «Absent» only in Historical rows of T01–T04.

## Acceptance / DoD
- [x] T01 README Code Facts/Gap: Historical absence vs As-of-Done fixtures+profile wiring
- [x] T02 README Code Facts/Gap: Historical vs As-of-Done `life_sim_pool_m20.json` env refs
- [x] T03 README Code Facts/Gap: Historical vs As-of-Done map + `resolve_pool_slot_bearer_token`
- [x] T04 README Code Facts/Gap: Historical vs As-of-Done `--life-sim` / wipe-confirmed
- [x] T06 product gate **не** reopen
- [x] Product tooling/tests not reopened (no drift); no invent `LIFE_SIM_POOL_*` secrets (G1 WAIVED)
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] `current.yaml` stays pkg-000102
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-req11-03-t07.md` signed (P6)

## Where to change
- T01–T04 Code Facts/Gap (done)
- Bullrun T07 row + P6 registry (on close)

## Out of scope
Product reopen; invent pool secrets / live bootstrap (G1 WAIVED); invent APIs; §Актуальная точка rewrite (G3 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000102 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|Absent|life_sim_pool|resolve_pool_slot|--life-sim' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter/task-gw-req11-03-t01-wire-fixtures-and-profile/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter/task-gw-req11-03-t02-pool-bootstrap-m20/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter/task-gw-req11-03-t03-map-200-to-pool-multi-bearer/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter/task-gw-req11-03-t04-wipe-profiled-replay-runner/README.md
ls doge-complaints-gateway/tests/sandbox/life_sim_pool_m20.json doge-complaints-gateway/tests/sandbox/life_sim_fixture_to_pool_map_v0_1.json
```
