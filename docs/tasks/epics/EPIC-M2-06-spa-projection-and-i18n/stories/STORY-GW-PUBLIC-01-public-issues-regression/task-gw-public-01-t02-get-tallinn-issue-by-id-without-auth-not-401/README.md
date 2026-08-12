# task-gw-public-01-t02

## Meta
- **Story:** [STORY-GW-PUBLIC-01](../STORY-GW-PUBLIC-01-public-issues-regression.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000048
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Regression guard: `GET /tallinn/issues/{id}` без auth → 200 or 404, **never** 401/403. Закрывает backlog T02 и AC «T01–T02: read routes публичны».

## Code Facts
- Route без auth deps — [`asgi_app.py:471`](../../../../../../../../src/core/api/asgi_app.py) `GET /tallinn/issues/{issue_id}`
- Existing GET-by-id in [`test_req24_tallinn_issues_read_api.py`](../../../../../../../../tests/test_req24_tallinn_issues_read_api.py) (`test_req24_ac6_get_by_id`, `test_req24_ac7_not_found`) — functional, not M-5 regression guard
- Target module — [`tests/test_gw_public_01_public_issues_regression.py`](../../../../../../../../tests/test_gw_public_01_public_issues_regression.py)

## Acceptance / DoD
- [ ] Traces parent AC: T01–T02 read routes публичны (T02 slice)
- [ ] Test: bare `GET /tallinn/issues/{known_id}` → 200 (when seeded) or 404 for unknown id
- [ ] Test: status never 401 or 403 for both cases
- [ ] Offline TestClient only
- [ ] [`acceptance-verification-gw-public-01-t02.md`](./acceptance-verification-gw-public-01-t02.md) signed after pytest PASS

## Where to change
- `doge-complaints-gateway/tests/test_gw_public_01_public_issues_regression.py` (add T02 tests)

## Out of scope
- List route (T01 — done)
- Write routes (T03–T04)
- `GET /story-drafts/{id}` (out of M-5 scope per backlog)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py -k t02
```
