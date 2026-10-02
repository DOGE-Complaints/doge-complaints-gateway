# task-gw-req11-11-t02-out-of-fixture-and-scale-locks

## Task: docs — out-of-fixture list + scale locks (T02)

## Meta
- **Story:** [STORY-GW-REQ11-11](../STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-02T08:52:55Z
- **Package:** pkg-000109
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-10-02T08:51:14Z
- **Completed:** 2026-10-02T08:52:55Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md`

## Purpose
Explicit **out of fixture v2** list + restate scale locks from REQ11-01 unchanged + pack ≠ `StoryRecord` dump. Scope #4 · **AC-GW-REQ1111-02**, **AC-GW-REQ1111-05**.

## Code Facts
**As-of-Done (P3 2026-10-02T08:52:55Z):**
1. Note §5 out list; §6 scale + ≠ StoryRecord (`story_id`, submitter, lifecycle, `payload_hash` on `StoryRecord`).
2. No invent taxonomy axis IDs / `gpt_signals` in v2 AC.

## Gap
**As-of-Done:** closed (AC-02, AC-05).

## Acceptance / DoD
- [x] Out list: no `story_id` / lifecycle / `submitter_*` / `payload_hash` / invent axis IDs / invent `gpt_signals` in v2 AC
- [x] Scale locks from REQ11-01 unchanged restated
- [x] Pack ≠ `StoryRecord` dump restated
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-11-t02.md` signed

## Where to change
- [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md) §5–6

## Out of scope
Flat keys (T01); mapping table (T03); Partial/Pass (T04); gate (T05); generator/adapter.

## Verification commands
```bash
rg -n "Out of fixture|Scale locks|StoryRecord|gpt_signals" doge-complaints-gateway/docs/analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md | head -20
```
