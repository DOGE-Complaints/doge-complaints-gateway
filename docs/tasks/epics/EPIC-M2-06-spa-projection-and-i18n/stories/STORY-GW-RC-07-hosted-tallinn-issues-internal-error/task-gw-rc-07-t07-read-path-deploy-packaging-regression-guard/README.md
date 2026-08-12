# task-gw-rc-07-t07

## Meta
- **Story:** [STORY-GW-RC-07](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000047)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_rc_07_audit_followup`)
- **Depends on:** T06
- **Audit ref:** [`audit-gw-rc-07-hosted-tallinn-issues-internal-error-2026-07-10`](../../../../../../analysis/audit-gw-rc-07-hosted-tallinn-issues-internal-error-2026-07-10.md) **G2**

## Purpose
Закрыть audit **G2**: regression-guard под deploy/packaging drift — ленивый import read-path модуля отсутствует в deploy artifact, `/ready` зелёный, первый `GET /tallinn/issues` → `INTERNAL_ERROR`. Существующие req24/gw_rc_03 тесты (local sqlite/memory) этот класс отказа не ловят.

## Code Facts
- Lazy imports — [`db_supabase.py:335,697,737,782`](../../../../../../../src/core/infrastructure/db_supabase.py) `from core.projection.columnar_storage import …`
- `/ready` checks DB columns only — [`dependencies.py:77-79`](../../../../../../../src/core/api/dependencies.py); no Python module import completeness
- Handler catch-all — [`handlers.py:410`](../../../../../../../src/core/api/handlers.py) → `INTERNAL_ERROR` ([`envelope.py:174`](../../../../../../../src/core/api/envelope.py))
- Existing tests insufficient — [`test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py), [`test_gw_rc_03_contract_guarantee.py`](../../../../../../../tests/test_gw_rc_03_contract_guarantee.py) (local, module always present)

## Acceptance / DoD
- Traces audit G2: deploy/packaging drift guard added (test and/or `/ready` extension)
- Guard fails when lazy-imported read-path module missing from artifact (or equivalent contract)
- `pytest` new/extended test green locally
- BULLRUN phases complete
- [`acceptance-verification-gw-rc-07-t07.md`](./acceptance-verification-gw-rc-07-t07.md) signed (Date post P6 verify only)

## Where to change (P6 — pick one approach in README execution)
- **(A)** New `tests/test_gw_rc_07_read_path_import_smoke.py` — assert import of modules used by `list_projections` read path
- **(B)** Extend `/ready` in [`dependencies.py`](../../../../../../../src/core/api/dependencies.py) with `read_path_modules` check

## Out of scope
- Changing clustering thresholds
- SEED-03 E2E runbook
- Re-diagnosing CF-B 2026-06-22 (T06 scope)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_gw_rc_07_read_path_import_smoke.py
python3 -m pytest -q tests/test_req24_tallinn_issues_read_api.py
```
