# task-gw-ssr-34-t01-server-env-local-railway-playbook

## Task: docs — server-env Local + Railway Volume playbook (T01)

## Meta
- **Story:** [STORY-GW-SSR-34](../STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000091
- **Skill declared:** code-documenter
- **Depends on:** SSR-16 Done; loadable uus precondition (вне story)
- **Scaffolded:** 2026-09-07T08:28:33Z
- **Closed:** 2026-09-07T08:32:02Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md`

## Purpose
Add Local + Railway sections to `docs/runtime-docs/manuals/server-env-quickstart.md`: local `schema-packs/` + `NODE_SCHEMA_*` (no Volume); Railway Volume mount → **`SCHEMA_PACKS_ROOT`** → copy nested pack → `NODE_SCHEMA_*` → redeploy. Explicit: mount path ≠ `SCHEMA_ROOT_URL`.

## Code Facts
1. Active pair — `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` (SSR-16).
2. Pack root — `SCHEMA_PACKS_ROOT` or default `<gateway>/schema-packs/` (resolver).
3. Volume / URL glossary — D-SSR-12; remote URL → SSR-35 later.
4. **As-of-Done:** Local + Railway playbooks + glossary landed in server-env-quickstart.

## Gap
**As-of-Done:** Gap closed at P3.

## Acceptance / DoD
- [x] Local prose: pack under `schema-packs/<id>/<ver>/`; `NODE_SCHEMA_*`; no Volume; no `SCHEMA_ROOT_URL`
- [x] Railway prose: Volume → mount → `SCHEMA_PACKS_ROOT` → copy → `NODE_SCHEMA_*` → redeploy → fail-fast
- [x] Glossary: mount ≠ remote URL (SSR-35 later)
- [x] No remote-fetch code; no Railway UI clicks; no pack repair
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md`

## Out of scope
SCHEMA_ROOT_URL product code (SSR-35); pack.json repair; GPT file edit.
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
rg -n "SCHEMA_PACKS_ROOT|SCHEMA_ROOT_URL|NODE_SCHEMA_|Volume|D-SSR-12" doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md
```
