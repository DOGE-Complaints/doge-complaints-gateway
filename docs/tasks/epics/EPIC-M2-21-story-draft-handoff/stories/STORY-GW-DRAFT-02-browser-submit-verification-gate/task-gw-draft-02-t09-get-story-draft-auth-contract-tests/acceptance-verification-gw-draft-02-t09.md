# Acceptance — TASK-GW-DRAFT-02-T09

- **Result:** PASS
- **Date:** 2026-07-03

| AC (audit G1) | Status | Evidence |
|---------------|--------|----------|
| GET auth contract scenarios | PASS | `tests/test_gw_draft_02_get_auth_contract.py` (6 tests); `test_gw_draft_01_*` GET paths updated |

**Live run:** `PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_02_get_auth_contract.py tests/test_gw_draft_01_story_draft_stash_contract.py` → 13 passed (2026-07-03)
