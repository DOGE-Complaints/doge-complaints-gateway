# task-gw-public-01-t04

## Meta
- **Story:** [STORY-GW-PUBLIC-01](../STORY-GW-PUBLIC-01-public-issues-regression.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000048
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Contrast test: `POST /tallinn/issues` без service token → 401; confirm full offline pytest suite green. Закрывает backlog T04 и AC «T03–T04: write routes закрыты» + «Тесты в offline-сюите, зелёные».

## Code Facts
- Write auth — [`asgi_app.py:485`](../../../../../../../../src/core/api/asgi_app.py) `POST /tallinn/issues` with `require_public_content_service_auth`
- Partial overlap: [`test_gw_gauth_01_two_layer_auth_contract.py`](../../../../../../../../tests/test_gw_gauth_01_two_layer_auth_contract.py) `test_tallinn_issues_post_requires_service_auth`
- Target module — [`tests/test_gw_public_01_public_issues_regression.py`](../../../../../../../../tests/test_gw_public_01_public_issues_regression.py)

## Acceptance / DoD
- [ ] Traces parent AC: T03–T04 write routes закрыты (T04 slice)
- [ ] Test: bare `POST /tallinn/issues` → 401
- [ ] `python3 -m pytest -q` offline suite green (no network)
- [ ] [`acceptance-verification-gw-public-01-t04.md`](./acceptance-verification-gw-public-01-t04.md) signed after pytest PASS

## Where to change
- `doge-complaints-gateway/tests/test_gw_public_01_public_issues_regression.py` (add T04 contrast test)

## Out of scope
- Hosted E2E
- `src/core/` changes

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py
cd doge-complaints-gateway && python3 -m pytest -q
```
