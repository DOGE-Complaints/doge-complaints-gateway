# task-gw-public-01-t01

## Meta
- **Story:** [STORY-GW-PUBLIC-01](../STORY-GW-PUBLIC-01-public-issues-regression.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000048
- **Skill declared:** python-pro
- **Depends on:** —

## Purpose
Regression guard: `GET /tallinn/issues` без auth headers → HTTP 200 (не 401/403). Закрывает backlog T01 и AC «T01–T02: read routes публичны».

## Code Facts
- Route без auth deps — [`asgi_app.py:429`](../../../../../../../../src/core/api/asgi_app.py) `GET /tallinn/issues`
- Gap: [`test_http_transport_smoke.py`](../../../../../../../../tests/test_http_transport_smoke.py) — `/health`, `/ready` only, not `/tallinn/issues`
- Functional GET exists in [`test_req24_tallinn_issues_read_api.py`](../../../../../../../../tests/test_req24_tallinn_issues_read_api.py) but без explicit «must not 401/403» regression semantics
- Target module — [`tests/test_gw_public_01_public_issues_regression.py`](../../../../../../../../tests/test_gw_public_01_public_issues_regression.py) (create in P3)

## Acceptance / DoD
- [ ] Traces parent AC: T01–T02 read routes публичны (T01 slice)
- [ ] Test: bare `client.get("/tallinn/issues")` → `status_code == 200`
- [ ] Test asserts `status_code not in (401, 403)`
- [ ] Offline TestClient only (no network)
- [ ] [`acceptance-verification-gw-public-01-t01.md`](./acceptance-verification-gw-public-01-t01.md) signed after pytest PASS

## Where to change
- `doge-complaints-gateway/tests/test_gw_public_01_public_issues_regression.py` (add T01 test)

## Out of scope
- `GET /tallinn/issues/{id}` (T02)
- Write-route contrast (T03–T04)
- `src/core/` changes

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py -k t01
```
