# acceptance-verification — GW-SSR-03 t04

- **Result:** PASS
- **Date:** 2026-08-28T14:13:05Z
- **Package:** pkg-000063

## Evidence

Intake `StoryRecord(` maps envelope → `schema_version`; inner → `schema_id` / `bound_schema_version` / profiles / `structured_payload` + `authoritative_payload_hash`. Client `payload_hash` key rejected at parse.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_03_optional_v2_semantic_wire.py::test_present_schema_binding_persists_and_hashes_server_side \
  tests/test_gw_ssr_03_optional_v2_semantic_wire.py::test_unknown_inner_keys_rejected
```
