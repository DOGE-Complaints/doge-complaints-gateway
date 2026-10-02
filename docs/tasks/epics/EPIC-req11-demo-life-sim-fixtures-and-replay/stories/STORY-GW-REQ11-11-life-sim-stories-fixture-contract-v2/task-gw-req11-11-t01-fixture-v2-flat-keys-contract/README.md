# task-gw-req11-11-t01-fixture-v2-flat-keys-contract

## Task: docs — fixture v2 flat keys contract (T01)

## Meta
- **Story:** [STORY-GW-REQ11-11](../STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-02T08:52:55Z
- **Package:** pkg-000109
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-02T08:51:14Z
- **Completed:** 2026-10-02T08:52:55Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md`

## Purpose
Write fixture contract v2 SSOT: **flat** layout lock + required join/schedule keys + Narrative-aligned content keys. Scope #1–3 · **AC-GW-REQ1111-01**.

## Code Facts
**As-of-Done (P3 2026-10-02T08:52:55Z):**
1. Contract note §1–3 locks flat layout + join + content keys.
2. Pack disk still 6-key (len 1661) — cite only; no regen.
3. Intake `Narrative` fields cited from `src/core/intake/contracts.py`.

## Gap
**As-of-Done:** closed (AC-01).

## Acceptance / DoD
- [x] Flat layout locked (no nest under `narrative` for v2 Pass)
- [x] Required join: `fixture_story_id`, `fixture_user_id`, `created_at`, `language`
- [x] Content keys: `title`/`body`; i18n maps; `session_language`, `location_query`, `canonical_type`, `canonical_labels`; optional `institution_i18n`
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-11-t01.md` signed

## Where to change
- [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md)

## Out of scope
Out-of-fixture list (T02); mapping note file ownership (T03); compat Partial/Pass (T04); gate (T05); REQ11-12 implement.

## Verification commands
```bash
rg -n "Layout lock|Required join|Narrative-aligned" doge-complaints-gateway/docs/analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md | head -20
```
