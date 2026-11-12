# task-gw-ssr-33-t03-index-inventory-gpt-ssr15-handoff

## Task: docs — INDEX + test inventory + GPT-SSR-15 invert handoff (T03)

## Meta
- **Story:** [STORY-GW-SSR-33](../STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000090
- **Skill declared:** code-documenter
- **Depends on:** T01–T02
- **Scaffolded:** 2026-09-04T13:23:06Z
- **Closed:** 2026-09-04T13:28:42Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md`

## Purpose
Ensure INDEX node-taxonomy section lists 31–33 + arch-doc + D-SSR-11; land/keep test inventory (31 Contour2 vs 32 Contour1 vs 33 docs); **record** GPT-SSR-15 must be superseded/inverted (gateway wins) — **do not** edit GPT UI file unless operator expands scope.

## Code Facts
1. INDEX — `docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` D-SSR-11 + rows 31–33.
2. Backlog SSR-33 — test inventory table (Contour2/1/docs ownership).
3. Sibling GPT — `GPT UI/.../STORY-GPT-SSR-15-taxonomy-meta-axis-lockstep.md` (out of edit scope).

## Gap
**Historical (pre-P3):** Need explicit inventory + GPT-SSR-15 invert handoff on gateway side.  
**As-of-Done:** INDEX inventory + sibling handoff landed (no GPT file edit). G1 SSOT labels closed P6 2026-09-04T13:34:49Z.

## Acceptance / DoD
- [x] INDEX node-taxonomy: 31–33 + arch-doc + D-SSR-11 aligned
- [x] Test inventory documents 31/32/33 ownership
- [x] GPT-SSR-15 invert/supersede note recorded (INDEX or manual or Related) — no GPT file edit
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md`
- Optionally backlog SSR-33 Related / manual cross-link

## Out of scope
Edit GPT UI STORY-GPT-SSR-15 body; product code.
- Overlay bans (every task):
  - Docs/README/manual/setup/test inventory **only**.
  - **No** `resolver.py` Contour2 reopen; **no** `axes.py` / `normalize_axis` reopen.
  - **No** GPT UI file edit (GPT-SSR-15) unless operator expands scope — handoff note only.
  - **No** ClusterLens / vocabulary / uus pack.json product repair.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Prefer README+manual+INDEX; avoid rewriting Done story bodies (SSR-26/29) unless necessary.

## Verification commands
```bash
rg -n "GPT-SSR-15|D-SSR-11|test_gw_ssr_31|test_gw_ssr_32" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md
```
