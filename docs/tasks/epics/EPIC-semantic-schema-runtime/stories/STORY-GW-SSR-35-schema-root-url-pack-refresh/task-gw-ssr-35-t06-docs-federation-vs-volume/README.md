# task-gw-ssr-35-t06-docs-federation-vs-volume

## Task: docs — Docs federation remote vs SSR-34 Volume (T06)

## Meta
- **Story:** [STORY-GW-SSR-35](../STORY-GW-SSR-35-schema-root-url-pack-refresh.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000092
- **Skill declared:** python-pro
- **Depends on:** soft SSR-34 Done; prior T* in pkg order
- **Scaffolded:** 2026-09-07T08:45:20Z
- **Completed:** 2026-09-07T08:54:22Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-35-schema-root-url-pack-refresh.md`

## Purpose
Extend SSR-34 manuals: federation remote path; mark SCHEMA_ROOT_URL / SCHEMA_PACK_REFRESH shipped after P3; glossary URL ≠ SCHEMA_PACKS_ROOT. Do not reopen Volume/gitignore product.

## Code Facts
1. server-env-quickstart already has URL ≠ mount glossary (SSR-35 later).
2. example.env notes SSR-35 later / absent.

## Gap
**Closed (P3 2026-09-07T08:54:22Z):** implemented.

## Acceptance / DoD
- [x] Manuals: URL = federation registry; Volume = SCHEMA_PACKS_ROOT only
- [x] Env examples inventory: vars marked shipped
- [x] No Volume/gitignore reopen
- [x] BULLRUN phases complete when closed

## Where to change
- `docs/runtime-docs/manuals/server-env-quickstart.md`
- `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`
- `example.env / .env.test.example`

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
rg -n 'SCHEMA_ROOT_URL|SCHEMA_PACK_REFRESH|SSR-35' doge-complaints-gateway/docs/runtime-docs/manuals doge-complaints-gateway/example.env
```
