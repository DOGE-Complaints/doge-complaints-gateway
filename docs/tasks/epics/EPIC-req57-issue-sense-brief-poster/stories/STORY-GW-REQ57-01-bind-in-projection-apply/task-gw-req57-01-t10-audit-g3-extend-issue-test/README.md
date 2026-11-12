# task-gw-req57-01-t10-audit-g3-extend-issue-test

## Task: tests — AC-06 evidence via live _extend_issue (G3)

## Meta
- **Story:** [STORY-GW-REQ57-01](../STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Type:** tests
- **Status:** ✅ Done
- **Package:** pkg-000113 (parent product AC Done); wave `run_mode=gw_req57_01_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ57-01
- **Depends on:** T01–T08 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req57-01-bind-in-projection-apply-2026-10-15.md`](../../../../../../analysis/audit-gw-req57-01-bind-in-projection-apply-2026-10-15.md) **G3**
- **Scaffolded:** 2026-10-15T11:21:05Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req57_01_gap_20261015T111932Z.plan.md` G3 TASKED follow_up=none

## Purpose
Close G3 (LOW): AC-06 evidence today = preserve_brief_wins_fields + manual save_projection; does not invoke IssueCreateService._extend_issue. Add one stub test path through _extend_issue (or create-extend) with generation_status=ready so brief title/summary survive. No live LLM. Product wire Present at issue_create.py ~375–387.

## Code Facts
### Live (post-P6 close) — 2026-10-15T11:26:56Z
1. `test_req57_01_brief_wins_via_live_extend_issue` Present — create→bind ready→create_issue extend path (`cluster_growth_extend`).
2. Asserts brief title/summary/generation_status/poster_url survive rebuild (claims: test file).
3. Suite `tests/test_gw_req57_01_bind_in_projection_apply.py` **10 passed**.

## Gap
Closed in P6 (G3 live `_extend_issue` evidence).

## Acceptance / DoD
- [x] At least one test invokes IssueCreateService._extend_issue (or documented create-extend entry) with ready brief
- [x] Assert title/summary remain brief-sourced after extend rebuild attempt
- [x] No live LLM; no invent AC beyond AC-06 evidence
- [x] current.yaml stays pkg-000113
- [x] acceptance-verification-gw-req57-01-t10.md signed (P6)

## Where to change
- `doge-complaints-gateway/tests/test_gw_req57_01_bind_in_projection_apply.py`

## Out of scope
Docs G1/G4 (T09); wrong-Bearer test (T11); reopen product gate

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req57_01_bind_in_projection_apply.py
```

## Done
- **Closed:** 2026-10-15T11:26:56Z (P6 `gw_req57_01_audit_followup`)
