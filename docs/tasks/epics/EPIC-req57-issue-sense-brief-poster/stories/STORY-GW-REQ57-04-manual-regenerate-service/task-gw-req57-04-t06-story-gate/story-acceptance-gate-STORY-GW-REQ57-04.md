# Story acceptance gate — STORY-GW-REQ57-04

- **Story:** Manual regenerate (service-auth)
- **Package:** `pkg-000116-20261015-gw-req57-04-manual-regenerate-service.yaml`
- **Result:** PASS
- **Date:** 2026-10-15T12:23:00Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ5704-01: service token → version bump + pending + nudge | PASS | `test_req57_04_asgi_service_token_bumps_pending_and_nudges` + unit regenerate |
| AC-GW-REQ5704-02: without service auth → rejected | PASS | `test_req57_04_asgi_missing_auth_rejected` → 401 |
| AC-GW-REQ5704-03: citizen Bearer cannot regenerate | PASS | `test_req57_04_asgi_citizen_bearer_rejected` → 401 |
| AC-GW-REQ5704-04: new version is distinct idempotency key for peer accept | PASS | bump v1→v2; accept body `generation_version` ≠ prior |

## Commands (live verification 2026-10-15T12:23:00Z)

```text
--verify ok 6 (pkg-000116)
doge-complaints-gateway/.venv/bin/python -m pytest -q tests/test_gw_req57_04_manual_regenerate_service.py → 6 passed
utc_now: 2026-10-15T12:23:00Z
stay_on_branch: dev · no push · no P4/P8
HTTP double only · no live aibridge/LLM · no citizen regenerate
```
