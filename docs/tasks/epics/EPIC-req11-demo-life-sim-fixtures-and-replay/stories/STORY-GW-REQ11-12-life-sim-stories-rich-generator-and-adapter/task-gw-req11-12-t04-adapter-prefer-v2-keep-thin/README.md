# task-gw-req11-12-t04-adapter-prefer-v2-keep-thin

## Task: implement — adapter prefer v2 keep thin (T04)

## Meta
- **Story:** [STORY-GW-REQ11-12](../STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000110
- **Skill declared:** python-pro
- **Depends on:** soft T01; soft REQ11-11 contract
- **Scaffolded:** 2026-10-02T09:02:38Z
- **Decision Ref:** backlog STORY-GW-REQ11-12 · note-gw-req11-11 consumer handoff

## Purpose
Update `life_sim_story_to_intake_payload` to **prefer** v2 `title_i18n` / `description_i18n` / `summary_i18n` / `location_query` / `canonical_*` / `session_language` / `institution_i18n` when Present; keep thin path for 6-key rows. **No invent** public HTTP. Scope #4 · **AC-GW-REQ1112-04**.

## Code Facts
1. Thin adapter today — `tests/sandbox/life_sim_replay_lib.py` → `life_sim_story_to_intake_payload` (synthesize all-lang from title/body).
2. Contract mapping table — note-gw-req11-11 §4 / §7.

## Gap
Adapter does not prefer on-disk v2 i18n/location/canonical when Present (scaffold).

## Acceptance / DoD
- [x] Prefer v2 fields when Present
- [x] 6-key thin path remains (Partial)
- [x] No invent HTTP APIs
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-12-t04.md` signed (P3)

## Where to change
- `tests/sandbox/life_sim_replay_lib.py` → `life_sim_story_to_intake_payload`

## Out of scope
Generator emit (T01); tests ownership (T05); live fill; invent gpt_signals/taxonomy axis IDs.

## Verification commands
```bash
rg -n "def life_sim_story_to_intake_payload|title_i18n|description_i18n" doge-complaints-gateway/tests/sandbox/life_sim_replay_lib.py | head -40
```
