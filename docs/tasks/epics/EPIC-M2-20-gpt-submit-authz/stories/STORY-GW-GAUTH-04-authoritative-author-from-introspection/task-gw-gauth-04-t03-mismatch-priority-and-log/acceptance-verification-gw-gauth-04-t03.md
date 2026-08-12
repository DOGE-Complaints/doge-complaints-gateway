# Acceptance — TASK-GW-GAUTH-04-T03

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Расхождение payload ↔ sub → приоритет `sub` | PASS | `handlers.py` `story_intake_submitter_mismatch` + `replace(submitter=...)` |

**Live run:** `pytest -q tests/test_gw_gauth_04_authoritative_author_contract.py::test_mismatch_payload_submitter_sub_wins` → PASS (2026-06-25)
