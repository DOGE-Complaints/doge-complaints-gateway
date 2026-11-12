# task-gw-ssr-28-t05-handoff-indicator

## Task: docs — handoff ready for SSR-29 / GPT byte-copy (T05)

## Meta
- **Story:** [STORY-GW-SSR-28](../STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000085
- **Skill declared:** python-pro
- **Depends on:** T02–T04
- **Scaffolded:** 2026-09-01T13:31:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md`

## Purpose
Document that tallinn taxonomy.json is byte-copy ready for SSR-29 checklist / GPT-SSR-05. Do **not** perform GPT UI copy in gateway P3.

## Code Facts
- Blocks SSR-29 — backlog INDEX
- Sibling GPT-SSR-05 / GPT-SSR-09 — backlog Meta
- README already documents taxonomy_schema (SSR-26)

## Acceptance / DoD
- [x] Pipeline or README note: tallinn seed ready for SSR-29 / GPT copy (paths only)
- [x] Explicit: gateway P3 does not edit GPT UI instructions
- [x] BULLRUN phases complete

## Where to change
- pipeline story and/or `schema-packs/README.md` one-line seed note

## Out of scope
GPT instruction edits. Full SSR-29 manual.
- Overlay bans (every task):
  - **No invent** taxonomy vocabulary — extract only from GPT `story-label-taxonomy.md` §4/§5/§6 + axes/disposition lockstep.
  - **No ClusterLens** add/remove. Enum stays 10.
  - **No** legal/mobility `taxonomy_schema` / taxonomy.json seed.
  - **No** silent renames vs GPT §4.
  - **No** GPT UI materialize / GPT-SSR-05 copy in this pkg.
  - Orphan `taxonomy.json` without manifest = **not** Done.
  - Stay `semantic-schema-runtime`. Не переписывать bullrun §«Актуальная точка».
  - No SSR-06/07/12. Do not start SSR-29 product. Do not reopen 01–27.
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "SSR-28|taxonomy.json|SSR-29|GPT-SSR-05" doge-complaints-gateway/schema-packs/README.md doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md | head
```
