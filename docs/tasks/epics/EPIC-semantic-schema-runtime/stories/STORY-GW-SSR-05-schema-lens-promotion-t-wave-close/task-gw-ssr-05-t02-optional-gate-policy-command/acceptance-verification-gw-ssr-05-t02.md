# acceptance-verification — GW-SSR-05 t02

- **Result:** PASS
- **Date:** 2026-08-28T15:00:08Z
- **Package:** pkg-000065

## Evidence

`IssueCreateCommand.gate_policy: PromotionGatePolicy | None = None` (`issue_create.py`). `submit_for_review(..., policy=)` uses `self.gate_policy` when `policy is None` (`service.py`). `_create_issue` passes `command.gate_policy`. Civic callers omit the field.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_05_optional_gate_policy.py tests/test_issue_promotion_service.py
```
