# task-gw-ssr-34-t04-env-examples-node-schema-inventory

## Task: env docs — NODE_SCHEMA_* + SCHEMA_PACKS_ROOT inventory (T04)

## Meta
- **Story:** [STORY-GW-SSR-34](../STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md)
- **Type:** docs / env
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000091
- **Skill declared:** code-documenter · soft python-pro
- **Depends on:** T03
- **Scaffolded:** 2026-09-07T08:28:33Z
- **Closed:** 2026-09-07T08:32:02Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md`

## Purpose
Update `example.env` / `.env.test.example`: `NODE_SCHEMA_*` inventory; `SCHEMA_PACKS_ROOT` Railway/disk note; no claim `SCHEMA_ROOT_URL` shipped. (No `.env.example` on disk — used `example.env`.)

## Code Facts
1. **As-of-Done:** `example.env` + `.env.test.example` carry NODE_SCHEMA + SCHEMA_PACKS_ROOT / URL glossary comments.
2. Fail-fast note present; uus commented dual example.

## Gap
**As-of-Done:** Gap closed at P3.

## Acceptance / DoD
- [x] Env examples show `NODE_SCHEMA_*` (tallinn default + uus commented)
- [x] `SCHEMA_PACKS_ROOT` documented as Railway/disk mount
- [x] No claim that `SCHEMA_ROOT_URL` is shipped
- [x] Fail-fast note preserved
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/example.env`
- `doge-complaints-gateway/.env.test.example`

## Out of scope
Implementing SCHEMA_ROOT_URL; inventing AppConfig fields; GPT env files.
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
rg -n "NODE_SCHEMA_|SCHEMA_PACKS_ROOT|SCHEMA_ROOT_URL" doge-complaints-gateway/example.env doge-complaints-gateway/.env.test.example
```
