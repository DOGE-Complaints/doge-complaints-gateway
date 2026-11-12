# acceptance-verification — GW-SSR-15 t02

- **Result:** PASS
- **Date:** 2026-08-29T19:47:15Z
- **Package:** pkg-000072

## Evidence

`test_ssr15_civic_unbound_lists_on_node_issues` — unbound civic projection appears on `GET /node/issues` (200). Also `test_gw_public_01_*` / `test_req24_issues_read_api.py` after T01.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_15_scenarios.py::test_ssr15_civic_unbound_lists_on_node_issues
```
