# task-gw-draft-06-t04-retire-dedicated-intake-http-tests

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000050
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Backlog T04 (part 1): retire or rewrite route-dedicated tests for public `POST /intake/stories` — primary files before bulk pipeline migration in T05.

## Code Facts
- Dedicated intake HTTP tests — [`test_http_intake_endpoint.py`](../../../../../../../../tests/test_http_intake_endpoint.py)
- OpenAPI compliance intake path — [`test_openapi_runtime_compliance.py:47`](../../../../../../../../tests/test_openapi_runtime_compliance.py)
- Obsolete GAUTH intake cases — [`test_gw_gauth_01_two_layer_auth_contract.py`](../../../../../../../../tests/test_gw_gauth_01_two_layer_auth_contract.py)

## Acceptance / DoD
- [ ] Traces parent AC #5 (partial): dedicated intake route tests removed or rewritten
- [ ] `test_openapi_runtime_compliance` no longer asserts `/intake/stories` path
- [ ] GW-DRAFT-01/02 contract tests still present (not deleted)
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-06-t04.md`](./acceptance-verification-gw-draft-06-t04.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/tests/test_http_intake_endpoint.py`
- `doge-complaints-gateway/tests/test_openapi_runtime_compliance.py`
- `doge-complaints-gateway/tests/test_gw_gauth_01_two_layer_auth_contract.py`

## Out of scope
- Bulk pipeline/e2e migration (~25 files) — T05
- `tests/conftest.py` suffixes — T05

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_openapi_runtime_compliance.py tests/test_gw_draft_01_story_draft_stash_contract.py -k 'not live_integration'
cd doge-complaints-gateway && test ! -f tests/test_http_intake_endpoint.py || rg '"/intake/stories"' tests/test_http_intake_endpoint.py
```
