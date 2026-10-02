# task-gw-req11-11-t04-compat-partial-vs-v2-pass

## Task: docs — 6-key Partial vs v2 Pass compat (T04)

## Meta
- **Story:** [STORY-GW-REQ11-11](../STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-02T08:52:55Z
- **Package:** pkg-000109
- **Skill declared:** python-pro
- **Depends on:** T01, T03
- **Scaffolded:** 2026-10-02T08:51:14Z
- **Completed:** 2026-10-02T08:52:55Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md`

## Purpose
State compatibility: old **6-key** rows = load **Partial** / thin adapter path; **v2** rows = **Pass** richness once REQ11-12 implements. Scope #5 · **AC-GW-REQ1111-04**.

## Code Facts
**As-of-Done (P3 2026-10-02T08:52:55Z):**
1. Note §7 Compatibility — Partial vs Pass.
2. Thin adapter Present; pack still 6-key (disk-verified).
3. Join keys preserved for REQ11-10.

## Gap
**As-of-Done:** closed (AC-04).

## Acceptance / DoD
- [x] 6-key = Partial / thin path stated
- [x] v2 = Pass richness once 12 implements stated
- [x] Join keys preserved for 01/10
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-11-t04.md` signed

## Where to change
- [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md) §7

## Out of scope
Implement thin/rich adapter (→12); pack regen; gate (T05).

## Verification commands
```bash
rg -n "Partial|Pass|6-key|thin" doge-complaints-gateway/docs/analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md | head -20
```
