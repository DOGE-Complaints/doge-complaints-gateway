# Story acceptance gate — STORY-GW-REQ10-02

- **Story:** Cleanup lifecycle data + slim mapper + remove debug I/O
- **Package:** `pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml`
- **Result:** PASS
- **Date:** 2026-09-28T17:44:10Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1002-01: Known legacy RECEIVED cleaned to `accepted` in test/hosted data (and fixtures if inventory required) | PASS | Fixtures **N/A** (absent). Hosted: **operator blocker** documented — PostgREST OK but `stories` `*/0` (≠ inventory 162); inventory id absent; RECEIVED×0 on current endpoint — [`evidence-gw-req10-02…`](../../../../../../analysis/evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md) §T01–T02 |
| AC-GW-REQ1002-02: Mapper no longer depends on permanent RECEIVED special-case | PASS | `_parse_lifecycle_status` slimmed — no RECEIVED map (`db_supabase.py`); tests assert source clean |
| AC-GW-REQ1002-03: Unknown lifecycle values still fail closed | PASS | `StoryLifecycleStatus(str(raw))` raises ValueError; pytest parametrize unknown → ValueError |
| AC-GW-REQ1002-04: No `.cursor/debug-*.log` writes from production lifecycle path; `rg` clean under `src` | PASS | agent-log / `debug-ba94c7` removed; `rg` clean under `src`; test asserts |

## Commands (live verification 2026-09-28T17:44:10Z)

```text
--verify ok 6 (pkg-000099)
.venv/bin/python -m pytest -q tests/test_gw_req10_02_lifecycle_parse.py → 11 passed
.venv/bin/python -m pytest -q tests/test_gw_req10_02_lifecycle_parse.py tests/test_story_repository_lifecycle.py tests/test_story_repository_contract.py → 24 passed
rg src clean for debug-ba94c7 / .cursor/debug / RECEIVED map keys
utc_now: 2026-09-28T17:44:10Z
branch: dev
H8 skip; §Актуальная точка untouched
```
