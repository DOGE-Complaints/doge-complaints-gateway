# task-gw-req11-06-t04-dry-run-operator-docs

## Task: docs / tooling — dry-run + operator docs (T04)

## Meta
- **Story:** [STORY-GW-REQ11-06](../STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Type:** docs / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-30T07:56:35Z
- **Package:** pkg-000105
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-09-30T07:51:07Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`

## Purpose
`--dry-run` lists planned deletes without mutating DB; link Present script/Make from `life-sim-demo-node-load-manual-ru.md` wipe §. Scope #5 · AC-GW-REQ1106-03. Name ≠ create until P3.

## Code Facts
1. Manual already names wipe path as acceptance target: `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md`.
2. Life_sim_load plan similarly names wipe story — Present link pending script.
3. Dry-run must not DELETE.

## Gap
**As-of-Done (P3):** closed.

No `--dry-run` behavior; manual wipe § not linked to Present script.

## Acceptance / DoD
- [x] `--dry-run` documents/lists planned tables/order without delete (AC-03)
- [x] Manual wipe § links to Present script + Make
- [x] Confirm flag documented for operators
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_wipe_node_content.py` (`--dry-run`; P3)
- `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md` wipe § (P3)

## Out of scope
Implement other tasks' product logic beyond docs/dry-run; invent wipe HTTP; Identity DELETE; rewrite §Актуальная точка.
- Overlay bans:
  - Stay `dev`.
  - Confirm: `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1`.
  - Tables lock unchanged.
  - Pointer pkg-000105; do not mutate pkg-000100…104.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
# after P3:
# rg -n 'dry-run|life_sim_wipe_node_content|life-sim-wipe' doge-complaints-gateway/docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md | head -40
```
