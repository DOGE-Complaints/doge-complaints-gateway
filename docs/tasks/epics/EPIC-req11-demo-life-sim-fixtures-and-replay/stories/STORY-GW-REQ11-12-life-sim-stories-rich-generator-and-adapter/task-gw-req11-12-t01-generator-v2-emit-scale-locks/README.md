# task-gw-req11-12-t01-generator-v2-emit-scale-locks

## Task: implement/tooling — generator v2 emit + scale locks (T01)

## Meta
- **Story:** [STORY-GW-REQ11-12](../STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- **Type:** implement/tooling
- **Status:** 🟢 Done
- **Package:** pkg-000110
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-02T09:02:38Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md`

## Purpose
Extend/replace `generate_dogestonia_life_sim_fixtures_v0_1.py` (or successor) to emit fixture **v2** flat fields per REQ11-11; preserve REQ11-01 scale/lang/2026 locks. Scope #1 · **AC-GW-REQ1112-01**.

## Code Facts
1. Contract v2 Present — [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md).
2. **As-of-Done:** v2 generator Present — `life_sim_stories_v2_lib.py` + `generate_life_sim_pack_stories_v2.py`; scale/lang lock = v0_1 seed.
3. **Historical (pre-P3):** Generator = 6-key + BLURBS — `generate_dogestonia_life_sim_fixtures_v0_1.py`.
4. Scale locks: 200 / Gauss 8.5·σ2.0·[1,20] / langs 60/30/10 / 2026 curve (REQ11-01).

## Gap
**CLOSED (P3):** v2 emit path Present under pack dir SSOT.

## Acceptance / DoD
- [x] Generator/successor emits flat v2 fields per REQ11-11
- [x] Scale/lang/2026 locks preserved
- [x] No LLM; no invent StoryRecord dump / gpt_signals / taxonomy axis IDs
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-12-t01.md` signed (P3)

## Where to change
- `tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py` (extend/replace) and/or successor under sandbox writing into pack dir

## Out of scope
Diversity cardinality (T02); params.json (T03); adapter (T04); tests (T05); ops docs (T06); gate (T07); live Auth/threads; reuse 07.

## Verification commands
```bash
rg -n "fixture_story_id|title_i18n|description_i18n" doge-complaints-gateway/tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py | head -30
```
