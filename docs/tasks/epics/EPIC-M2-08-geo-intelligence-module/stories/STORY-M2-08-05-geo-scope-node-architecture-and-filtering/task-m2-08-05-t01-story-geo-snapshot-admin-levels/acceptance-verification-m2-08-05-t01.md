# Acceptance verification — TASK-M2-08-05-T01

- **Task:** StoryGeoSnapshot admin hierarchy fields
- **Result:** PASS
- **Evidence:** `src/core/domain/contracts.py` — four optional `admin_*` fields on `StoryGeoSnapshot`; defaults `None` preserve call-site compatibility
- **Commands:** `python3 -m pytest tests/test_req35_geo_scope_and_filter.py -q --tb=short` (subset); full suite `268 passed`

| AC | Status | Evidence |
|----|--------|----------|
| P0 admin_* fields on snapshot | PASS | `contracts.py` L37–40 |
| P0 backward-compatible optional fields | PASS | frozen dataclass defaults |
| P1 domain re-exports unchanged surface | PASS | `from core.domain import StoryGeoSnapshot` in tests |
