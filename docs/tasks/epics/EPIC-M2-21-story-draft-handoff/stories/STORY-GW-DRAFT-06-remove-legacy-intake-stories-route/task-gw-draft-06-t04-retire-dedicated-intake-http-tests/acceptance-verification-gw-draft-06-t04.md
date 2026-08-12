# Acceptance verification — task-gw-draft-06-t04-retire-dedicated-intake-http-tests

- **Task:** T04 retire dedicated intake HTTP tests
- **Status:** PASS
- **Date:** 2026-07-11T10:15:42Z

## Checklist

- [x] `test_http_intake_endpoint.py` removed
- [x] `test_openapi_runtime_compliance` asserts `/story-drafts`, not `/intake/stories`
- [x] `test_gw_gauth_01` covers story-drafts stash auth
- [x] GW-DRAFT-01/02 contract tests present

## Evidence

```
test ! -f tests/test_http_intake_endpoint.py → ok
python3 -m pytest -q tests/test_openapi_runtime_compliance.py tests/test_gw_draft_01_story_draft_stash_contract.py → pass
python3 -m pytest -q tests/test_gw_gauth_01_two_layer_auth_contract.py → pass
```
