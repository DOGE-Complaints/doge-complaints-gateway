# Acceptance — TASK-GW-GAUTH-04-T05

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Автор = `sub` | PASS | `test_verified_introspection_persists_sub_not_payload` |
| Mismatch → sub wins | PASS | `test_mismatch_payload_submitter_sub_wins` |
| Нет истории без introspection | PASS | `test_inactive_*`, `test_unverified_*` |

**Live run:** `pytest -q tests/test_gw_gauth_04_authoritative_author_contract.py` → 6 passed (2026-06-25)
