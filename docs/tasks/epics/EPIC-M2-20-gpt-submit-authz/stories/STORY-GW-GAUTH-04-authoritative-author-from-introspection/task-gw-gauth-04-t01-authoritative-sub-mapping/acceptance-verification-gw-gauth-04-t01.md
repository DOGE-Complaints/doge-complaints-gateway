# Acceptance — TASK-GW-GAUTH-04-T01

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Автор = `sub` из introspection (mapping) | PASS | `authoritative_submitter_from_introspection` in `src/core/identity/authoritative_submitter.py` |

**Live run:** `pytest -q tests/test_gw_gauth_04_authoritative_author_contract.py::test_authoritative_submitter_mapping_unit` → PASS (2026-06-25)
