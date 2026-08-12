# Story acceptance gate — STORY-M2-18-02

- **Story:** Cross-layer contract zones A–I (REQ-39)
- **Package:** `pkg-000020-20260518-req39-cross-layer-contract-testing.yaml` (paths 6–13)
- **Result:** PASS
- **Date:** 2026-05-18

## AC checklist (REQ-39 §17)

| AC | Status | Evidence |
|----|--------|----------|
| AC-39-2 Zones A–I | PASS | T06–T13 test modules + hygiene |
| AC-39-8 Closure table | PASS | offline modules listed below |
| AC-39-9 Full offline pytest | PASS | `394 passed` (`--ignore=tests/integration`) |
| AC-39-1 Hygiene | PASS | README-index REQ-39; stale req-cross-layer refs fixed |
| `gateway_resolve_queue.py --verify` paths 6–13 | PASS | pkg-000020 |

## Verification command (story slice)

```bash
cd doge-complaints-gateway && python3 -m pytest -q \
  tests/test_supabase_bootstrap_schema.py \
  tests/test_supabase_deserialization_contracts.py \
  tests/test_story_intake_field_persistence.py \
  tests/test_story_repository_contract.py \
  tests/test_api_service_contract.py \
  tests/test_logging_setup.py \
  tests/test_store_contract_parity.py \
  tests/test_config_loading.py::test_db_backend_defaults_to_in_memory_via_provide_app_config \
  tests/test_config_loading.py::test_db_backend_supabase_from_env \
  tests/test_config_loading.py::test_factory_in_memory_uses_inmemory_repos \
  tests/test_config_loading.py::test_in_memory_default_is_explicit_in_config_schema
```

Result: **55 passed** (2026-05-18).
