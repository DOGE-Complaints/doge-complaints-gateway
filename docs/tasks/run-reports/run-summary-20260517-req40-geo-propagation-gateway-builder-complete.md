# Run summary — REQ-40 Geo Propagation to Issue Projection (Gateway Builder)

- **Story:** STORY-M2-06-05
- **Package:** pkg-000018 (6 tasks T01–T06)
- **Build window:** `gateway-cursor-build-window--STORY-M2-06-05.md`
- **Decision ref:** REQ-40, SA-18 Phase 1
- **Status:** Story gate PASS — Done (Awaiting Commits)
- **Date:** 2026-05-17

## Tasks closed

| Task | Gap | Outcome |
|------|-----|---------|
| T01 | GAP-40-01 | `ProjectionInput` + 7 geo_* fields |
| T02 | GAP-40-02 | `DOGEIssue.geo` + conditional `to_public_dict()` |
| T03 | GAP-40-03 | `project_distinct_issue()` geo dict mapping |
| T04 | GAP-40-04 | `build_projection_input_from_draft(geo_snapshot=…)` |
| T05 | GAP-40-05 | bridge passes `dominant_story.geo` |
| T06 | REQ-40 §7 | `tests/test_req40_geo_propagation.py` + story gate |

## Test evidence

- `python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify` → **ok 6 paths**
- `python3 -m pytest -q` → **294 passed**, 10 skipped

## Out of scope (unchanged)

- REQ-24 geo filters on read API
- Phase 3 postal_code
- Centroid geo v2
- Immutable `pkg-000017`

## Next operator steps

- Commits per `docs/methodology/git-commit.md` (runtime + tests; task docs optional)
