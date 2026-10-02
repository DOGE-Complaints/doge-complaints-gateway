# task-gw-req11-11-t03-mapping-note-fixture-to-narrative

## Task: docs — mapping note fixture v2 → Narrative (T03)

## Meta
- **Story:** [STORY-GW-REQ11-11](../STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-02T08:52:55Z
- **Package:** pkg-000109
- **Skill declared:** python-pro
- **Depends on:** T01, T02
- **Scaffolded:** 2026-10-02T08:51:14Z
- **Completed:** 2026-10-02T08:52:55Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md`

## Purpose
Document mapping table fixture → intake Narrative in a **named analysis note**. Scope #6 · **AC-GW-REQ1111-03**. Soft skill: code-documenter.

## Code Facts
**As-of-Done (P3 2026-10-02T08:52:55Z):**
1. Note Present with filename lock.
2. Mapping table matches backlog §Mapping table + thin adapter cite.
3. Intake `Narrative` / `Origin` from `contracts.py` — cite only.

## Gap
**As-of-Done:** closed (AC-03).

## Acceptance / DoD
- [x] Note Present under `docs/analysis/`
- [x] **Filename lock:** `note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`
- [x] Mapping table includes backlog rows
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-11-t03.md` signed

## Where to change
- [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md)

## Out of scope
Implement adapter (→12); invent Narrative fields; nest layout; gate (T05).

## Verification commands
```bash
test -f doge-complaints-gateway/docs/analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md
rg -n "original_text|title_i18n|fixture_story_id" doge-complaints-gateway/docs/analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md | head -20
```
