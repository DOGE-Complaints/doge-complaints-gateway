# Run summary — REQ-24 Tallinn Issues Read API (Gateway Builder)

- **Story:** STORY-M2-06-06
- **Package:** pkg-000019 (8 tasks T01–T08)
- **Build window:** `gateway-cursor-build-window--STORY-M2-06-06.md`
- **Decision ref:** REQ-24, REQ-27 (`doge_issues`), SA-18 §7
- **Status:** Story gate PASS — Done (Awaiting Commits)
- **Date:** 2026-05-17

## Tasks closed

| Task | Gap | Outcome |
|------|-----|---------|
| T01 | GAP-24-01 | `IssueProjectionReadStore` Protocol |
| T02 | GAP-24-02 | InMemory `list_projections` / `get_projection` |
| T03 | GAP-24-03 | SQLite + Supabase read on `doge_issues` |
| T04 | GAP-24-04 | Factory + `ApiDependencies` wiring |
| T05 | GAP-24-05 | HTTP handlers + `create_manual_issue` |
| T06 | GAP-24-06 | Routes, OPTIONS CORS, public GET |
| T07 | GAP-24-07 | `read_filters.py` geo/time/institution |
| T08 | GAP-24-08 | `test_req24_tallinn_issues_read_api.py` + OpenAPI |

## Test evidence

- `python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify` → **ok 8 paths**
- `python3 -m pytest tests/test_req24_tallinn_issues_read_api.py -q` → **17 passed**
- `python3 -m pytest -q` → **311 passed**, 10 skipped

## Notable runtime fixes during build

- Status query filter matches SPA `payload.status` (REQ-24 AC-5), not promotion row status.
- Cluster path saves projection row status as SPA status (`PUBLISHED`), aligned with manual create.
- Explicit `OPTIONS` routes for `/tallinn/issues` (AC-9).

## Out of scope (unchanged)

- Pagination, PostGIS, SPA client changes
- Immutable `pkg-000018` (REQ-40)

## Next operator steps

- Commits per `docs/methodology/git-commit.md` (runtime + tests; task docs optional)
- Point `gateway-active-package.current.yaml` at next wave when ready
