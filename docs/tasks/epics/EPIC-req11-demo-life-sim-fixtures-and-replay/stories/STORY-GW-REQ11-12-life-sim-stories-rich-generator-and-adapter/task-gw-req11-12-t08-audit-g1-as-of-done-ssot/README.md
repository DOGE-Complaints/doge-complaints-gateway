# task-gw-req11-12-t08-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G1)

## Meta
- **Story:** [STORY-GW-REQ11-12](../STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-02T09:16:09Z
- **Package:** pkg-000110 (parent product AC Done); wave `run_mode=gw_req11_12_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ11-12
- **Depends on:** T01–T07 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req11-12-life-sim-stories-rich-generator-and-adapter-2026-10-02.md`](../../../../../../analysis/audit-gw-req11-12-life-sim-stories-rich-generator-and-adapter-2026-10-02.md) **G1**
- **Scaffolded:** 2026-10-02T09:13:54Z
- **Completed:** 2026-10-02T09:16:09Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_12_gap_20261002T091313Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog (+ pipeline) §Verified still scaffold present-tense (generator = 6-key + ~15 BLURBS / unique bodies **15**/1661) while Meta Status=Done and disk shows v2 pack **1661/1661**. Docs-only As-of-Done vs Historical (mirror REQ11-08…11). Soft task README markers if needed. G2 WAIVED operator (§Актуальная точка).

## Code Facts
1. Audit G1 — backlog/pipeline §Verified (scaffold) lacks As-of-Done vs Historical while product Done + pack Present.
2. Product Present — `life_sim_stories_v2_lib.py` / `generate_life_sim_pack_stories_v2.py` / pack `ls-20261002T0906Z-veerenni-v2-rich` / adapter prefer v2; T01–T07 Done.
3. Gate PASS 2026-10-02T09:10:26Z · diversity **1661/1661**.
4. Pointer stays pkg-000110; product Story Done; G2 WAIVED (§Актуальная точка).
5. **As-of-Done (P6 2026-10-02T09:16:09Z):** G1 CLOSED — backlog/pipeline §Verified As-of-Done vs Historical; T01 soft markers.

## Gap
**G1 CLOSED:** backlog/pipeline §Verified now split As-of-Done (v2 · 1661/1661) vs Historical (6-key · 15 BLURBS).

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (v2 pack / 1661 unique As-of-Done; 6-key / 15 BLURBS Historical)
- [x] Pipeline §Verified / Code Facts soft sync if needed
- [x] Optional T01–T06 README As-of-Done markers (docs-only)
- [x] T07 product gate **не** reopen
- [x] No product/generator/adapter/pytest; no invent AC; no pack regen
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000110
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-12-t08.md` signed (P6)

## Where to change
- Backlog `STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md` §Verified
- Pipeline `STORY-GW-REQ11-12-…md` §Verified / Code Facts
- Optional soft task README markers
- Bullrun T08 row status on close

## Out of scope
Rewrite §Актуальная точка (G2 WAIVED); mutate pkg-000110 / current.yaml; product code; reopen T01–T07 AC.

- Overlay bans:
  - Stay `dev`.
  - Safe-override only; do not change `gateway-active-package.current.yaml`.

## Verification commands
```bash
rg -n "As-of-Done|Historical|15|/1661|BLURBS|v2" doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```
