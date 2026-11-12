# task-gw-req57-04-t08-audit-g4-unknown-issue-id-test

## Task: test — empty/unknown issue_id → 400 (G4)

## Meta
- **Story:** [STORY-GW-REQ57-04](../STORY-GW-REQ57-04-manual-regenerate-service.md)
- **Type:** test
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:31:24Z
- **Package:** pkg-000116 (parent product AC Done); wave `run_mode=gw_req57_04_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ57-04
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`../../../../../../analysis/audit-gw-req57-04-manual-regenerate-service-2026-10-15.md`](../../../../../../analysis/audit-gw-req57-04-manual-regenerate-service-2026-10-15.md) **G4**
- **Scaffolded:** 2026-10-15T12:29:46Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req57_04_gap_20261015T122823Z.plan.md` G4 TASKED follow_up=none

## Purpose
Close G4 (LOW soft): assert empty + unknown `issue_id` with service token → **400**. Stub only. G2 WAIVED.

## Code Facts
### Live (post-P6 close) — 2026-10-15T12:31:24Z
1. `test_req57_04_asgi_empty_issue_id_rejected` + `test_req57_04_asgi_unknown_issue_id_rejected` → 400.
2. Suite `tests/test_gw_req57_04_manual_regenerate_service.py` **8 passed**.

## Gap
**Closed P6 2026-10-15T12:31:24Z.**

## Acceptance / DoD
- [x] Test empty `issue_id` + service token → 400
- [x] Test unknown `issue_id` + service token → 400
- [x] Suite still stub-only; AC-01…04 unchanged
- [x] No invent AC; product gate T01–T06 **не** reopen
- [x] current.yaml stays pkg-000116
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-04-t08.md` signed (P6)

## Done
- **Closed:** 2026-10-15T12:31:24Z (P6 `gw_req57_04_audit_followup`)

## Where to change
- `tests/test_gw_req57_04_manual_regenerate_service.py`

## Out of scope
T07 docs SSOT; mutate pkg-000116; rewrite §Актуальная точка; citizen regenerate

## Verification commands
```bash
doge-complaints-gateway/.venv/bin/python -m pytest -q tests/test_gw_req57_04_manual_regenerate_service.py
```
