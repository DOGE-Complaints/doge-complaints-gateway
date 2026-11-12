# task-gw-ssr-35-t03-boot-wire-before-resolve

## Task: implement — Boot wire: fetch before resolve_pack (T03)

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
When URL set and (cache miss or refresh) → fetch before `resolve_pack`; on success continue normal resolve. Document fresh-cache policy (skip unnecessary re-fetch).

## Code Facts
1. Active pair from NODE_SCHEMA_* / AppConfig.
2. LocalSchemaRuntime / resolve_pack post-fetch consumer.
3. SSR-34 path must work with URL unset.

## Gap
**Closed (P3 2026-09-07T08:54:22Z):** implemented.

## Acceptance / DoD
- [x] URL + miss/refresh → fetch then resolve_pack SUCCESS
- [x] URL unset → SSR-34 local/Volume path unchanged
- [x] Fresh cache policy documented or no unnecessary re-fetch
- [x] BULLRUN phases complete when closed

## Where to change
- `boot/init / schema runtime wiring (services or schema package)`

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
rg -n 'resolve_pack|SCHEMA_ROOT_URL' doge-complaints-gateway/src/core
```
