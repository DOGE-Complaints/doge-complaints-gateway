# task-gw-public-01-t06

## Meta
- **Story:** [STORY-GW-PUBLIC-01](../STORY-GW-PUBLIC-01-public-issues-regression.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000048)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_public_01_audit_followup`)
- **Depends on:** T05 (story gate PASS)
- **Audit ref:** [`audit-gw-public-01-public-issues-regression-2026-07-10`](../../../../../../analysis/audit-gw-public-01-public-issues-regression-2026-07-10.md) **G1**

## Purpose
Закрыть audit **G1**: восстановить `TestClient.request` после session-level patch в autouse fixture `_gauth_testclient_auto_headers` — убрать глобальный побочный эффект conftest.

## Code Facts
- Patch site — [`tests/conftest.py:121-132`](../../../../../../../../tests/conftest.py) — `TestClient.request = _patched_request` once per session
- Teardown — [`conftest.py:133-134`](../../../../../../../../tests/conftest.py) — только `_service_skip_auto_headers.reset`, **без** restore метода
- `_ORIGINAL_TESTCLIENT_REQUEST` — module global [`conftest.py:17`](../../../../../../../../tests/conftest.py)
- PUBLIC-01 tests unaffected today — GET no-op for auto-inject; T04 uses `gauth_raw_client` marker [`conftest.py:116-119`](../../../../../../../../tests/conftest.py)
- Auto-inject scope — POST only, suffixes `("/intake/stories", "/tallinn/issues")` [`conftest.py:16`](../../../../../../../../tests/conftest.py)

## Acceptance / DoD
- [x] Traces audit G1: after pytest session (or session finalizer) `TestClient.request` restored to original bound method
- [x] `pytest -q -m "not live_integration"` green (568 passed)
- [x] `tests/test_gw_public_01_public_issues_regression.py` 5/5 unchanged behavior
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-public-01-t06.md`](./acceptance-verification-gw-public-01-t06.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/tests/conftest.py` only

## Out of scope
- R1–R3 doc hygiene (`activation: none` per operator)
- `src/core/` changes
- Re-open T05 gate (operational PASS stands)
- Mutate `pkg-000048` or `gateway-active-package.current.yaml`

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py
python3 -c "from starlette.testclient import TestClient; from tests.conftest import _ORIGINAL_TESTCLIENT_REQUEST; assert TestClient.request is _ORIGINAL_TESTCLIENT_REQUEST or _ORIGINAL_TESTCLIENT_REQUEST is not None"
```
