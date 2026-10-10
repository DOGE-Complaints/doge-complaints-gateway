# task-gw-req56-01-t05-asgi-handler-search-tests

## Task: test — ASGI/handler search tests (T05)

## Meta
- **Story:** [STORY-GW-REQ56-01](../STORY-GW-REQ56-01-issues-list-search-filter.md)
- **Type:** test
- **Status:** 🟢 Done
- **Package:** pkg-000111
- **Skill declared:** python-pro
- **Depends on:** soft T03–T04
- **Scaffolded:** 2026-10-10T15:52:08Z
- **Done:** 2026-10-10T16:01:13Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md`

## Purpose
Production-entry тест: `search` влияет на фильтр; S3 non-widening vs same params without search; TECH-ARCH §6.2 · DP3/DP4 · **AC-GW-REQ5601-01/03/06**.

## Code Facts
### As-of-Done (P3 2026-10-10T16:01:13Z)
1. ASGI production-entry tests Present — filter / non-widen / whitespace / `/node/search` 404 in `tests/test_gw_req56_01_issues_list_search_filter.py`.
2. TECH-ARCH §6.2 production-entry verify covered.

### Historical (pre-P3 / scaffold)
1. Production-entry search wiring tests Absent (scaffold).

## Gap
**G1 residual closed by T07:** Code Facts flipped As-of-Done vs Historical (ASGI tests Present).

## Acceptance / DoD
- [x] ASGI/handler test: non-empty `search` + `status=PUBLISHED` filters matches
- [x] S3: with same other params, `search` does not return rows excluded without `search`
- [x] Wiring on production entry (not orphan helper only)
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-01-t05.md` signed (P3)

## Where to change
- `tests/test_gw_req56_01_*.py` and/or existing issues-list ASGI suite (P3)

## Out of scope
OpenAPI docs (REQ56-02); gate ownership (T06); SQL invent.

## Verification commands
```bash
# P3 example
cd doge-complaints-gateway && python -m pytest tests/test_gw_req56_01*.py -q
```
