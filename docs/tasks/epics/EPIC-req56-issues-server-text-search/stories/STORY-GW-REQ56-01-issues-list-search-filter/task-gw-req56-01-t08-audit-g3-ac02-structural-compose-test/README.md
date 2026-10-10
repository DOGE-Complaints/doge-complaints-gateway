# task-gw-req56-01-t08-audit-g3-ac02-structural-compose-test

## Task: test — AC-02 structural compose evidence (G3)

## Meta
- **Story:** [STORY-GW-REQ56-01](../STORY-GW-REQ56-01-issues-list-search-filter.md)
- **Type:** test
- **Status:** 🟢 Done
- **Done at:** 2026-10-10T16:15:39Z
- **Package:** pkg-000111 (parent product AC Done); wave `run_mode=gw_req56_01_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ56-01
- **Depends on:** T01–T06 Done (product AC / gate PASS); soft T07
- **Audit ref:** [`audit-gw-req56-01-issues-list-search-filter-2026-10-10.md`](../../../../../../analysis/audit-gw-req56-01-issues-list-search-filter-2026-10-10.md) **G3**
- **Scaffolded:** 2026-10-10T16:12:13Z
- **Completed:** 2026-10-10T16:15:39Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req56_01_gap_20261010T160937Z.plan.md` G3 TASKED follow_up=none

## Purpose
Закрыть G3 (LOW soft): AC-02 evidence currently uses **status** AND with `search`; add one pointed unit pairing `search` with ≥1 **non-status** structural filter (`issue_type` / `labels` / equivalent). Product AND order already Present (`filter_projection_rows` after `_matches_post_fetch_filters`). No invent AC; no ASGI route invent.

## Code Facts
1. Audit G3 — status AND was sole compose unit; TECH-ARCH/DP4 name «structural».
2. Product AND Present — search after structural/geo in `read_filters.py`.
3. **As-of-Done (P6 2026-10-10T16:15:39Z):** `test_req56_01_filter_compose_and_with_issue_type` Present; suite **11 passed**.

## Gap
**G3 CLOSED:** unit pairs `search` + `issue_type` (non-status structural) AND.

## Acceptance / DoD
- [x] One unit: `search` + ≥1 non-status structural (`issue_type`) composes AND
- [x] Extends existing `tests/test_gw_req56_01_*.py` (no new route invent)
- [x] Pytest green for that case (**11 passed**)
- [x] No SQL/FTS invent; no OpenAPI (REQ56-02)
- [x] `current.yaml` stays pkg-000111
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-01-t08.md` signed (P6)

## Where to change
- `tests/test_gw_req56_01_issues_list_search_filter.py` — `test_req56_01_filter_compose_and_with_issue_type`

## Out of scope
Rewrite §Актуальная точка (G2); mutate pkg/current.yaml; reopen product AC framing; invent DRAFT status.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req56_01_issues_list_search_filter.py
```
