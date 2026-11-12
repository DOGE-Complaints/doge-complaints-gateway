# Story acceptance gate — STORY-GW-REQ57-03

- **Story:** Sweep / retry sense-brief jobs
- **Package:** `pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml`
- **Result:** PASS
- **Date:** 2026-10-15T12:03:07Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ5703-01: previously failed/missing job can complete via sweep (AC-57-06) | PASS | `test_req57_03_sweep_renudges_pending_and_failed` + cron `run_once` |
| AC-GW-REQ5703-02: ready brief not silently replaced by alpha on sweep | PASS | `test_req57_03_ready_not_overwritten_by_sweep` |
| AC-GW-REQ5703-03: unit/integration with stubs | PASS | suite **5 passed** · HTTP double only |

## Commands (live verification 2026-10-15T12:03:07Z)

```text
--verify ok 6 (pkg-000115)
doge-complaints-gateway/.venv/bin/python -m pytest -q tests/test_gw_req57_03_sweep_retry_sense_brief.py → 5 passed
utc_now: 2026-10-15T12:03:07Z
stay_on_branch: dev · no push · no P4/P8
HTTP double only · no live aibridge/LLM
```
