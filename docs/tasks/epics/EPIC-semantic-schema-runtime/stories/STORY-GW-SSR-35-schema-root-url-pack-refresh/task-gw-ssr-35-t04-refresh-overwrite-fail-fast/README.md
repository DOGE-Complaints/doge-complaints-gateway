# task-gw-ssr-35-t04-refresh-overwrite-fail-fast

## Task: implement — Refresh overwrite + fail-fast (T04)

## Meta
- **Story:** [STORY-GW-SSR-35](../STORY-GW-SSR-35-schema-root-url-pack-refresh.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000092
- **Skill declared:** python-pro
- **Depends on:** soft SSR-34 Done; prior T* in pkg order
- **Scaffolded:** 2026-09-07T08:45:20Z
- **Completed:** 2026-09-07T08:54:22Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-35-schema-root-url-pack-refresh.md`

## Purpose
SCHEMA_PACK_REFRESH overwrite; corrupt/missing after attempt → ConfigError-class; no silent foreign default / tallinn fallback.

## Code Facts
1. D-SSR-8: no invent DEFAULT_SCHEMA_PACK / first-in-list.
2. Fail-fast aligned with NODE_SCHEMA_* required.

## Gap
**Closed (P3 2026-09-07T08:54:22Z):** implemented.

## Acceptance / DoD
- [x] Refresh overwrites nested cache files
- [x] Corrupt/missing → ConfigError-class; not tallinn default
- [x] No silent foreign pack fallback
- [x] BULLRUN phases complete when closed

## Where to change
- `fetch/refresh path + config errors`

## Out of scope
Volume/gitignore/uus (SSR-34); invent registry; URL as mount; pack repair; §Актуальная точка rewrite.
- Overlay bans (every task):
  - `SCHEMA_ROOT_URL` = remote federation registry URL only — never Volume mount / disk path.
  - Persist target = `SCHEMA_PACKS_ROOT` or default local root — not URL.
  - **No** Volume/gitignore/uus-activate reopen (SSR-34 Done).
  - **No** invent registry product / live CI registry.
  - Fresh cache: no unnecessary re-fetch (or document policy in T03/T04).
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000061…091; pointer is pkg-000092.

## Verification commands
```bash
rg -n 'SCHEMA_PACK_REFRESH|ConfigError' doge-complaints-gateway/src/core
```
