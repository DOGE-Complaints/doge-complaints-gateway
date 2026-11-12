# task-gw-req57-02-t09-audit-g4-manual-issue-nudge-test

## Task: tests — create_manual_issue → pending + nudge evidence (G4)

## Meta
- **Story:** [STORY-GW-REQ57-02](../STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Type:** tests
- **Status:** ✅ Done
- **Package:** pkg-000114 (parent product AC Done); wave `run_mode=gw_req57_02_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ57-02
- **Depends on:** T01–T07 Done (product AC / gate PASS)
- **Audit ref:** [`../../../../../../analysis/audit-gw-req57-02-nudge-on-create-publish-2026-10-15.md`](../../../../../../analysis/audit-gw-req57-02-nudge-on-create-publish-2026-10-15.md) **G4**
- **Scaffolded:** 2026-10-15T11:47:15Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req57_02_gap_20261015T114558Z.plan.md` G4 TASKED follow_up=none

## Purpose
Close G4 (LOW): T04 claims `create_manual_issue` hook Present (`issue_create.py` ~518–523) but suite never calls it. Add one stub test: create_manual_issue → generation_status=pending (+ optional nudge HTTP double). No live aibridge. Product wire Present — test only.

## Code Facts
### Live (post-P6 close) — 2026-10-15T11:51:25Z
1. `test_req57_02_create_manual_issue_sets_pending_and_nudges` invokes `create_manual_issue` with enabled nudge + HTTP double.
2. Asserts pending + `generation_version` + accept URL/Bearer/`issue_id` body (suite 9).
3. Product wire unchanged; current.yaml pkg-000114 unchanged.

## Gap
Closed in P6 (test evidence).

## Acceptance / DoD
- [x] At least one test invokes `create_manual_issue` with nudge service/double
- [x] Assert pending (+ generation_version) after manual create; optional accept call when enabled
- [x] No live aibridge/LLM; no invent AC beyond G4 evidence
- [x] current.yaml stays pkg-000114
- [x] BULLRUN phases complete when closed
- [x] acceptance-verification-gw-req57-02-t09.md signed (P6)

## Done
- **Closed:** 2026-10-15T11:51:25Z (P6 `gw_req57_02_audit_followup`)

## Where to change
- `doge-complaints-gateway/tests/test_gw_req57_02_nudge_on_create_publish.py`

## Out of scope
Docs G3/G5 (T08); ASGI POST create (G1 WAIVED); reopen product AC

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req57_02_nudge_on_create_publish.py -k manual
```
