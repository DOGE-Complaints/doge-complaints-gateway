# acceptance-verification — GW-SSR-08 t02

- **Result:** PASS
- **Date:** 2026-08-29T17:52:54Z
- **Package:** pkg-000066

## Evidence

`tallinn_civic/v1` `readiness_policy` knobs 35/3/false in pack file. Mapper `pack_policy.py` as-is. Civic default still 70/2/`require_actionable_canonical_type=True` (`gates.py:14`). Factory `service_factory.py:108` unchanged.

## Commands

```bash
rg -n "require_actionable_canonical_type: bool = True" doge-complaints-gateway/src/core/promotion/gates.py
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_08_pack_load_membership.py::test_readiness_knobs_come_from_pack_file_not_civic_defaults
```
