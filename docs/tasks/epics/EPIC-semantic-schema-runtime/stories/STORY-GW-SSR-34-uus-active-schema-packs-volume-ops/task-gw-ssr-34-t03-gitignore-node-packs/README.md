# task-gw-ssr-34-t03-gitignore-node-packs

## Task: git policy — ignore node packs; keep demo tracked (T03)

## Meta
- **Story:** [STORY-GW-SSR-34](../STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md)
- **Type:** docs / git policy
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000091
- **Skill declared:** code-documenter · soft python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-09-07T08:28:33Z
- **Closed:** 2026-09-07T08:32:02Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md`

## Purpose
Apply gateway `.gitignore`: ignore node packs `schema-packs/uus_veerenni_civic/`; **keep** tallinn/legal/mobility tracked. uus was untracked — no `git rm --cached` needed.

## Code Facts
1. **As-of-Done:** `.gitignore` includes `schema-packs/uus_veerenni_civic/`.
2. Demo packs remain tracked (tallinn 3 / legal 2 / mobility 2 files).
3. `git check-ignore` matches uus pack.json.

## Gap
**As-of-Done:** Gap closed at P3.

## Acceptance / DoD
- [x] Ignore rule for node packs (uus…) landed
- [x] Demo packs remain tracked / available for pytest
- [x] No `gitignore` of entire `schema-packs/`
- [x] uus was not tracked — no disk delete / no `--cached` needed
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/.gitignore`

## Out of scope
Deleting operator pack files; ignoring all schema-packs; remote-fetch code.
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
rg -n "uus_|schema-packs/" doge-complaints-gateway/.gitignore
git -C doge-complaints-gateway check-ignore -v schema-packs/uus_veerenni_civic/v2/pack.json
git -C doge-complaints-gateway ls-files 'schema-packs/tallinn_civic/**' | head
```
