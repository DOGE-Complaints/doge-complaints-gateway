# task-gw-req11-12-t03-params-json-foci-defaults

## Task: implement/tooling — params.json foci/tags defaults (T03)

## Meta
- **Story:** [STORY-GW-REQ11-12](../STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- **Type:** implement/tooling
- **Status:** 🟢 Done
- **Package:** pkg-000110
- **Skill declared:** python-pro
- **Depends on:** soft T01
- **Scaffolded:** 2026-10-02T09:02:38Z
- **Decision Ref:** backlog STORY-GW-REQ11-12

## Purpose
Consume optional pack `params.json` when Present: `story_foci` / `node_social_direction` / `neighbourhood_tags` (themes blurbs if Present); empty → civic defaults (load manual §4 semantics). Scope #3 · **AC-GW-REQ1112-03**.

## Code Facts
1. Pack layout Present — `tests/sandbox/life_sim_packs/<pack_id>/` + `params.json` per load manual.
2. Manual guiding (not schema SSOT): `life-sim-demo-node-load-manual-ru.md` §4.

## Gap
Generator does not consume pack params for rich v2 emit (scaffold).

## Acceptance / DoD
- [x] params Present → foci/tags/direction consumed
- [x] empty/absent → civic defaults
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-12-t03.md` signed (P3)

## Where to change
- Generator/successor + pack `params.json` read path

## Out of scope
Adapter (T04); invent HTTP; change 08/09 UX.

## Verification commands
```bash
rg -n "story_foci|node_social_direction|neighbourhood_tags" doge-complaints-gateway/docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md | head -20
```
