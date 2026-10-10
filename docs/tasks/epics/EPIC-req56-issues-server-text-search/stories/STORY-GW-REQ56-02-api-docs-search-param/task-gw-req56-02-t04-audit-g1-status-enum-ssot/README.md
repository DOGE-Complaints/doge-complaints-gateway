# task-gw-req56-02-t04-audit-g1-status-enum-ssot

## Task: docs — align list `status` enum with DOGEIssueStatus (G1)

## Meta
- **Story:** [STORY-GW-REQ56-02](../STORY-GW-REQ56-02-api-docs-search-param.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Done at:** 2026-10-10T16:50:05Z
- **Package:** pkg-000112 (parent product AC Done); wave `run_mode=gw_req56_02_audit_followup`
- **Skill declared:** python-pro
- **Soft skill:** code-documenter
- **Wave:** audit follow-up GW-REQ56-02
- **Depends on:** T01–T03 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req56-02-api-docs-search-param-2026-10-10.md`](../../../../../../analysis/audit-gw-req56-02-api-docs-search-param-2026-10-10.md) **G1**
- **Scaffolded:** 2026-10-10T16:45:04Z
- **Completed:** 2026-10-10T16:50:05Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req56_02_gap_20261010T164014Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): co-located `GET /node/issues` query table still documents `status` as `DRAFT`, `PUBLISHED` while governed `DOGEIssueStatus` is `NEW` / `IN_REVIEW` / `PUBLISHED` (`enums.py`). Soft: align openapi issue schema enum if same docs pass. Product search AC (T01–T03) **не** reopen. G2 WAIVED operator (§Актуальная точка).

## Code Facts
### As-of-Done (P6 2026-10-10T16:50:05Z)
1. API_REFERENCE list `status` → `NEW`, `IN_REVIEW`, `PUBLISHED` (governed DOGEIssueStatus).
2. Soft openapi `IssueProjection.status` enum aligned; planned PATCH line no longer invents DRAFT.
3. G1 **CLOSED**. Pointer stays pkg-000112. G2 WAIVED kept.

### Historical (pre-P6 / audit)
1. List table claimed `DRAFT`/`PUBLISHED`; openapi schema `enum: [DRAFT, PUBLISHED]`.

## Gap
**G1 CLOSED:** status SSOT aligned with `DOGEIssueStatus`.

## Acceptance / DoD
- [x] API_REFERENCE list `status` aligns with `DOGEIssueStatus` (no invent `DRAFT`)
- [x] Soft: openapi issue schema enum aligned in same pass
- [x] T03 product gate **не** reopen
- [x] No runtime filter rewrite; no invent AC; no comments/separate route/index claims
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000112
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-02-t04.md` signed (P6)

## Where to change
- `docs/runtime-docs/api-reference/API_REFERENCE.md`
- Soft: `docs/runtime-docs/api-reference/openapi.yaml`

## Out of scope
Rewrite §Актуальная точка (G2 WAIVED); mutate pkg-000112 / current.yaml; reopen T01–T03 AC; runtime filter code.

## Verification commands
```bash
rg -n "status|DRAFT|NEW|IN_REVIEW|PUBLISHED" doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml | head -40
rg -n "NEW|IN_REVIEW|PUBLISHED" doge-complaints-gateway/src/core/projection/enums.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
