# task-gw-req11-06-t08-audit-g2-manual-s8-inventory

## Task: docs — manual §8 Wipe inventory Present (G2)

## Meta
- **Story:** [STORY-GW-REQ11-06](../STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-09-30T08:02:52Z
- **Package:** pkg-000105 (parent product AC Done); wave `run_mode=gw_req11_06_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ11-06
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-06-wipe-node-content-stories-derivatives-2026-09-30.md`](../../../../../../analysis/audit-gw-req11-06-wipe-node-content-stories-derivatives-2026-09-30.md) **G2**
- **Scaffolded:** 2026-09-30T08:01:10Z
- **Completed:** 2026-09-30T08:02:52Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_06_gap_20260930T080005Z.plan.md` G2 TASKED follow_up=none

## Purpose
Закрыть G2 (LOW): `life-sim-demo-node-load-manual-ru.md` §8 inventory Wipe row still future-tense («ожидаем Done») while §5 documents Present script/Make. Docs-only one-line align. G3 WAIVED operator.

## Code Facts
1. Audit G2 — §8 inventory Wipe future-tense (pre-P6).
2. Manual §5 Present — wipe script + Make + confirm/dry-run cmds.
3. Gate PASS 2026-09-30T07:56:35Z.
4. **As-of-Done (P6 2026-09-30T08:02:52Z):** G2 CLOSED — §8 Wipe inventory = Present/Done.
5. Pointer stays pkg-000105.

## Gap
**G2 CLOSED:** §8 inventory aligned with §5 Present.

## Acceptance / DoD
- [x] Manual §8 Wipe inventory row = Present/Done (not «ожидаем Done»)
- [x] §5 Present path unchanged / consistent
- [x] T06 product gate **не** reopen
- [x] Product wipe tooling not reopened
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] `current.yaml` stays pkg-000105
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-06-t08.md` signed (P6)

## Where to change
- `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md` §8 Wipe inventory row (done)
- Bullrun T08 row + P6 registry (on close)

## Out of scope
Product/wipe execute; invent wipe HTTP; Identity DELETE; §Актуальная точка rewrite (G3 WAIVED); mutate pkg-000105; G1 backlog/T01 SSOT (T07).
- Overlay bans:
  - Docs-only inventory align.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000105 / current.yaml.

## Verification commands
```bash
rg -n 'Wipe|ожидаем|life_sim_wipe|Present' \
  doge-complaints-gateway/docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
