# task-gw-ssr-34-t02-warehouse-model-manual-d-ssr-12

## Task: docs — warehouse model manual D-SSR-12 (T02)

## Meta
- **Story:** [STORY-GW-SSR-34](../STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000091
- **Skill declared:** code-documenter
- **Depends on:** T01
- **Scaffolded:** 2026-09-07T08:28:33Z
- **Closed:** 2026-09-07T08:32:02Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md`

## Purpose
Document warehouse model in `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`: local in-tree `schema-packs/` path; git policy (node packs ignored; demo tracked); Railway Volume precedence via `SCHEMA_PACKS_ROOT`; D-SSR-12 table alignment.

## Code Facts
1. Layout — nested `<id>/<ver>/{pack,payload.schema,taxonomy}.json`.
2. INDEX — D-SSR-12 already recorded (local + Volume; URL → SSR-35).
3. **As-of-Done:** §Warehouse model (D-SSR-12 / SSR-34) landed.

## Gap
**As-of-Done:** Gap closed at P3.

## Acceptance / DoD
- [x] Local path + `NODE_SCHEMA_*` documented
- [x] Git policy: node packs not committed; demo/seed may stay tracked
- [x] Volume = `SCHEMA_PACKS_ROOT` precedence; URL deferred SSR-35
- [x] No pack content invent; no remote-fetch code
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`

## Out of scope
Ignore entire `schema-packs/`; warehouse outside gateway tree; SSR-35 fetch.
- Overlay bans (every task):
  - Docs / env / gitignore ops **only**.
  - **No** `SCHEMA_ROOT_URL` fetch / refresh product code (SSR-35).
  - **No** pack content repair; **no** invent geo/civic enums.
  - **No** Railway UI clicks / remote mount actions in P3 agent.
  - **No** GPT UI file edit — sibling note only (T05).
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - `SCHEMA_PACKS_ROOT` = Volume mount / disk root; **`SCHEMA_ROOT_URL` ≠ mount**.

## Verification commands
```bash
rg -n "D-SSR-12|SCHEMA_PACKS_ROOT|warehouse|gitignore|Volume" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
