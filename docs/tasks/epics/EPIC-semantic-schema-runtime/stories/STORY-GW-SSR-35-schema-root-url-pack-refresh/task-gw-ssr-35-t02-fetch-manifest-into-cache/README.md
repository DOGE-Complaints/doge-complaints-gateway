# task-gw-ssr-35-t02-fetch-manifest-into-cache

## Task: implement — Fetch manifest + files into nested cache (T02)

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
Given URL + `(NODE_SCHEMA_ID, NODE_SCHEMA_VERSION)` fetch fixture-shaped manifest + download files into `SCHEMA_PACKS_ROOT` or default `schema-packs/` as `<id>/<ver>/`. Isolate fetch from resolver parse. No live registry product.

## Code Facts
1. `resolver.py` `default_packs_root()` / SCHEMA_PACKS_ROOT.
2. Manifest shape = fixture stub only until federation SSOT.
3. No F4 Arweave upload / membership registry invent.

## Gap
**Closed (P3 2026-09-07T08:54:22Z):** implemented.

## Acceptance / DoD
- [x] Fetch writes nested `<id>/<ver>/` under packs root
- [x] Fixture-only manifest; no live CI registry required
- [x] Fetch module isolated from resolver parse
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/src/core/schema/ (new fetch module)`
- `packs root via SCHEMA_PACKS_ROOT or default`

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
rg -n 'SCHEMA_ROOT_URL|fetch' doge-complaints-gateway/src/core/schema
```
