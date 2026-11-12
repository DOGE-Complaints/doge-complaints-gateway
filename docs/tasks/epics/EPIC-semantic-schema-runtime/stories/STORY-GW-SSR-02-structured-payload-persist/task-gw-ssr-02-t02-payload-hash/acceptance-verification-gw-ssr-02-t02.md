# acceptance-verification — GW-SSR-02 t02

- **Result:** PASS
- **Date:** 2026-08-28T13:47:57Z
- **Package:** pkg-000062

## Evidence

src/core/schema/payload.py payload_hash_for + authoritative_payload_hash; persist ignores client hash

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_02_structured_payload_persist.py \
  tests/test_stories_schema_cross_layer_invariant.py \
  tests/test_story_intake_contract.py tests/test_story_intake_field_persistence.py
# → 36 passed
```
