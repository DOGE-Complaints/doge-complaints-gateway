# Story acceptance gate — STORY-GW-REQ57-02

- **Story:** Thin nudge on Issue create/publish
- **Package:** `pkg-000114-20261015-gw-req57-02-nudge-on-create-publish.yaml`
- **Result:** PASS
- **Date:** 2026-10-15T11:41:13Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ5702-01: create/publish → pending + nudge observable (AC-57-03) | PASS | `test_req57_02_create_sets_pending_and_nudges` + ASGI pending read |
| AC-GW-REQ5702-02: nudge URL/body/auth match as-built accept + locked env names | PASS | transport double asserts accept URL + Bearer + body |
| AC-GW-REQ5702-03: tests with HTTP test double (no live aibridge required) | PASS | suite **8 passed** |
| AC-GW-REQ5702-04: missing/disabled nudge config → fail-closed (no silent success) | PASS | disabled + missing_config + 503 tests |

## Commands (live verification 2026-10-15T11:41:13Z)

```text
--verify ok 7 (pkg-000114)
doge-complaints-gateway/.venv/bin/python -m pytest -q tests/test_gw_req57_02_nudge_on_create_publish.py → 8 passed
utc_now: 2026-10-15T11:41:13Z
stay_on_branch: dev · no push · no P8
HTTP double only · no live aibridge/LLM
```
