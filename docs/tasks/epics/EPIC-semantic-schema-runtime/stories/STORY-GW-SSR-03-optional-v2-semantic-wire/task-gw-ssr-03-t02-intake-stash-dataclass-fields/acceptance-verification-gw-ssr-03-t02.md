# acceptance-verification — GW-SSR-03 t02

- **Result:** PASS
- **Date:** 2026-08-28T14:13:05Z
- **Package:** pkg-000063

## Evidence

`SchemaBinding` on `StoryIntakeRequest` and `StoryDraftStashRequest`; `intake_request_from_stash_and_submitter` copies `schema_binding`.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_03_optional_v2_semantic_wire.py::test_stash_and_submit_share_binding
```
