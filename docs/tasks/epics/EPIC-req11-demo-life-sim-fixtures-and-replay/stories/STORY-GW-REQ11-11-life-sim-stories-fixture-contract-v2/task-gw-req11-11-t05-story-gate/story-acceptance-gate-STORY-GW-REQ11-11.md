# Story acceptance gate — STORY-GW-REQ11-11

- **Story:** Life-sim `stories.json` fixture contract v2 (Narrative-aligned)
- **Package:** `pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml`
- **Result:** PASS
- **Date:** 2026-10-02T08:53:45Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1111-01: Written fixture contract v2: required join keys + Narrative-aligned flat content keys; layout = **flat** (locked) | PASS | [`note-gw-req11-11-…`](../../../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md) §1–3; T01 |
| AC-GW-REQ1111-02: Explicit **out of fixture** list: no `story_id` / lifecycle / submitter / invent taxonomy axis IDs / invent `gpt_signals` in v2 AC | PASS | note §5; T02 |
| AC-GW-REQ1111-03: Mapping table fixture → intake Narrative documented in named analysis note | PASS | note §4; filename lock; T03 |
| AC-GW-REQ1111-04: Compatibility: 6-key = Partial / thin; v2 = Pass richness once 12 | PASS | note §7; pack 6-key disk len 1661; T04 |
| AC-GW-REQ1111-05: Scale locks from REQ11-01 unchanged; pack ≠ `StoryRecord` dump | PASS | note §6; T02 |

## Commands (live verification 2026-10-02T08:53:45Z)

```text
--verify ok 5 (pkg-000109)
--verify --check-dates → ok date-check
test -f docs/analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md
pack stories.json keys = 6 (fixture_story_id, fixture_user_id, language, created_at, title, body) len 1661
utc_now: 2026-10-02T08:53:45Z
branch: dev
docs-only; no generator/adapter; no invent AC/axis/gpt_signals; 07 not reused; §Актуальная точка untouched
```
