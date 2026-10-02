# task-gw-req11-12-t06-pack-dir-ssot-ops-docs-partial-to-pass

## Task: docs/tooling — pack dir SSOT + ops Partial→Pass (T06)

## Meta
- **Story:** [STORY-GW-REQ11-12](../STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- **Type:** docs/tooling
- **Status:** 🟢 Done
- **Package:** pkg-000110
- **Skill declared:** python-pro
- **Depends on:** soft T01–T02
- **Scaffolded:** 2026-10-02T09:02:38Z
- **Decision Ref:** backlog STORY-GW-REQ11-12

## Purpose
Write/reference new pack under `tests/sandbox/life_sim_packs/<pack_id>/` (not flat `*_v0_1` SSOT); load-manual / note — Partial (6-key blurbs) → **Pass** when v2 pack used. Scope #5+#7 · **AC-GW-REQ1112-06**.

## Code Facts
1. Pack dir layout Present — `life_sim_packs/<pack_id>/`.
2. Manual — `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md`.

## Gap
No v2 reference pack + Partial→Pass ops note yet (scaffold).

## Acceptance / DoD
- [x] New/reference pack under `life_sim_packs/<pack_id>/`
- [x] Flat `*_v0_1` sandbox JSON **not** SSOT for new packs
- [x] Load-manual note Partial→Pass when v2 pack used
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-12-t06.md` signed (P3)

## Where to change
- `tests/sandbox/life_sim_packs/<pack_id>/`
- `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md` (and/or analysis note)

## Out of scope
Live Auth/threads; invent HTTP; change 08/09 UX beyond cross-link if needed.

## Verification commands
```bash
ls doge-complaints-gateway/tests/sandbox/life_sim_packs/*/stories.json | head -10
rg -n "Partial|Pass|v2|stories.json" doge-complaints-gateway/docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md | head -30
```
