# task-gw-ssr-34-t05-sibling-gpt-schema-binding-note

## Task: docs — sibling GPT schema_binding == env pair (T05)

## Meta
- **Story:** [STORY-GW-SSR-34](../STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000091
- **Skill declared:** code-documenter
- **Depends on:** T04
- **Scaffolded:** 2026-09-07T08:28:33Z
- **Closed:** 2026-09-07T08:32:02Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md`

## Purpose
Record operator note: GPT `schema_binding` must match gateway active `NODE_SCHEMA_*` pair (SSR-17). **No** GPT Instructions edit.

## Code Facts
1. **As-of-Done:** Notes in `server-env-quickstart.md` Local playbook step 6 + warehouse manual GPT lockstep; `.env.test.example` comment.
2. No GPT UI files touched.

## Gap
**As-of-Done:** Gap closed at P3.

## Acceptance / DoD
- [x] Explicit note: GPT binding == env pair
- [x] No GPT UI file edits
- [x] BULLRUN phases complete when closed

## Where to change
- Manuals / env comments (gateway-side only)

## Out of scope
Edit GPT Instructions; Pack Builder schema; validator scripts.
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
rg -n "schema_binding|NODE_SCHEMA_|SSR-17" doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
