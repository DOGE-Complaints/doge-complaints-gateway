# Story acceptance gate — STORY-GW-REQ57-01

- **Story:** Bind-in receiver + sense-brief projection apply
- **Package:** `pkg-000113-20261015-gw-req57-01-bind-in-projection-apply.yaml`
- **Result:** PASS
- **Date:** 2026-10-15T11:13:59Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ5701-01: success bind → public title/summary ≠ sole dominant-story baseline (AC-57-01) | PASS | `test_req57_01_success_bind_applies_title_summary_ready` |
| AC-GW-REQ5701-02: brief-sourced title ≤80 / plainness per REQ13 (AC-57-02) | PASS | `test_req57_01_title_max_80` + success apply |
| AC-GW-REQ5701-03: public read includes `poster_url` when ready (AC-57-04) | PASS | GET `/node/issues/{id}` + list tests |
| AC-GW-REQ5701-04: `generation_status` pending/ready/failed distinguishable (AC-57-05) | PASS | success ready / fail failed / seed pending |
| AC-GW-REQ5701-05: fail bind → failed + no pretend AI sense (AC-57-07) | PASS | `test_req57_01_fail_bind_sets_failed_no_pretend` |
| AC-GW-REQ5701-06: ready brief not overwritten by dominant Story without regenerate | PASS | `test_req57_01_brief_wins_guard_unit` + extend save |
| AC-GW-REQ5701-07: unit/ASGI tests with stub bind payloads (no live LLM) | PASS | suite **8 passed** 2026-10-15T11:13:59Z |

## Commands (live verification 2026-10-15T11:13:59Z)

```text
--verify ok 8 (pkg-000113)
doge-complaints-gateway/.venv/bin/python -m pytest -q tests/test_gw_req57_01_bind_in_projection_apply.py → 8 passed
utc_now: 2026-10-15T11:13:59Z
stay_on_branch: dev · no push · no P8
no live LLM · stub bind payloads only
```
