# task-gw-req56-01-t07-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G1)

## Meta
- **Story:** [STORY-GW-REQ56-01](../STORY-GW-REQ56-01-issues-list-search-filter.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Done at:** 2026-10-10T16:15:39Z
- **Package:** pkg-000111 (parent product AC Done); wave `run_mode=gw_req56_01_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ56-01
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req56-01-issues-list-search-filter-2026-10-10.md`](../../../../../../analysis/audit-gw-req56-01-issues-list-search-filter-2026-10-10.md) **G1**
- **Scaffolded:** 2026-10-10T16:12:13Z
- **Completed:** 2026-10-10T16:15:39Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req56_01_gap_20261010T160937Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T01–T06 READMEs (+ soft pipeline §Code touchpoints) still scaffold Absent/Gap present-tense while Status=Done and product Present (`issue_search_match.py`, `search` wire). Docs-only As-of-Done vs Historical (mirror REQ11-08…12). G2 WAIVED operator (§Актуальная точка).

## Code Facts
1. Audit G1 — task README Code Facts/Gap were scaffold Absent while Status=Done.
2. Product Present — `issue_search_match.py`; `filter_projection_rows(search=)`; ASGI/handler `search`; suite green; gate PASS.
3. Pointer stays pkg-000111; product Story Done; G2 WAIVED (§Актуальная точка).
4. **As-of-Done (P6 2026-10-10T16:15:39Z):** G1 CLOSED — T01–T06 As-of-Done vs Historical; pipeline §Code touchpoints flipped.

## Gap
**G1 CLOSED:** T01–T06 README + pipeline Code touchpoints As-of-Done vs Historical.

## Acceptance / DoD
- [x] T01–T06 README: As-of-Done vs Historical (Present paths vs pre-P3 Absent)
- [x] Soft pipeline §Code touchpoints header (no «implement in P3» as present-tense obligation)
- [x] T06 product gate **не** reopen
- [x] No product filter rewrite beyond docs; no invent AC
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000111
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-01-t07.md` signed (P6)

## Where to change
- Task READMEs T01–T06 under this story
- Soft: pipeline `STORY-GW-REQ56-01-….md` §Code touchpoints
- Bullrun T07 row status on close

## Out of scope
Rewrite §Актуальная точка (G2 WAIVED); mutate pkg-000111 / current.yaml; reopen T01–T06 AC; OpenAPI (REQ56-02).

## Verification commands
```bash
rg -n "As-of-Done|Historical|issue_search_match" doge-complaints-gateway/docs/tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t0*/README.md | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
