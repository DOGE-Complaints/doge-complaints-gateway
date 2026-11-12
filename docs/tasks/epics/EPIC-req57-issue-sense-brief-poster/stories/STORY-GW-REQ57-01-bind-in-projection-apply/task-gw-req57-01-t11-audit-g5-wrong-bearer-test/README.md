# task-gw-req57-01-t11-audit-g5-wrong-bearer-test

## Task: tests — wrong Bearer / non-service token → 401 (G5)

## Meta
- **Story:** [STORY-GW-REQ57-01](../STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Type:** tests
- **Status:** ✅ Done
- **Package:** pkg-000113 (parent product AC Done); wave `run_mode=gw_req57_01_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ57-01
- **Depends on:** T01–T08 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req57-01-bind-in-projection-apply-2026-10-15.md`](../../../../../../analysis/audit-gw-req57-01-bind-in-projection-apply-2026-10-15.md) **G5**
- **Scaffolded:** 2026-10-15T11:21:05Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req57_01_gap_20261015T111932Z.plan.md` G5 TASKED follow_up=none

## Purpose
Close G5 (LOW): Scope #5 rejects channel/wrong Bearer as bind auth. Only missing-Authorization case tested today; compare_digest Present in security.py. Add ASGI case Authorization Bearer ≠ SERVICE_API_TOKEN → 401 on POST /v1/issue-sense-brief/bind.

## Code Facts
### Live (post-P6 close) — 2026-10-15T11:26:56Z
1. `test_req57_01_bind_rejects_wrong_bearer` Present — wrong Bearer → 401 on bind.
2. Suite `tests/test_gw_req57_01_bind_in_projection_apply.py` **10 passed**.

## Gap
Closed in P6 (G5 wrong-Bearer ASGI case).

## Acceptance / DoD
- [x] ASGI test: wrong/channel-like Bearer ≠ SERVICE_API_TOKEN → 401 on bind
- [x] No live LLM; no invent AC
- [x] current.yaml stays pkg-000113
- [x] acceptance-verification-gw-req57-01-t11.md signed (P6)

## Where to change
- `doge-complaints-gateway/tests/test_gw_req57_01_bind_in_projection_apply.py`

## Out of scope
Docs T09; extend_issue test T10; mutate auth implementation beyond test

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req57_01_bind_in_projection_apply.py -k wrong
```

## Done
- **Closed:** 2026-10-15T11:26:56Z (P6 `gw_req57_01_audit_followup`)
