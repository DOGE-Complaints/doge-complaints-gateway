# task-gw-ssr-35-t01-config-schema-root-url-refresh

## Task: implement — Config env contract URL + refresh (T01)

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
Optional `SCHEMA_ROOT_URL` (http/https only; never filesystem mount) + `SCHEMA_PACK_REFRESH` in EnvSpec/load. Reject path-like Volume mounts. One style with env contract; no dual-source.

## Code Facts
1. **As-of-Done (SSR-35 pkg-000092):** `SCHEMA_ROOT_URL` + `SCHEMA_PACK_REFRESH` in `schema.py` EnvSpec/load; path-like Volume rejected.
2. `_validate_http_url` / `_parse_schema_root_url` — http(s) only.
3. `NODE_SCHEMA_*` required in AppConfig; packs root via env/resolver — **unchanged**.
4. **Historical (pre-P3):** no `SCHEMA_ROOT_URL` / `SCHEMA_PACK_REFRESH` in `src/` (grep empty 2026-09-06).

## Gap
**Closed (P3 2026-09-07T08:54:22Z):** implemented. **G1 CLOSED (P6 2026-09-07T08:58:54Z):** Code Facts As-of-Done.

## Acceptance / DoD
- [x] SCHEMA_ROOT_URL optional; http(s) only; path-like rejected
- [x] SCHEMA_PACK_REFRESH env bool/flag one contract
- [x] No mount-as-URL; no NODE_SCHEMA_* semantics change
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/src/core/config/schema.py`
- `example.env / .env.test.example (inventory note; shipped after P3)`

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
rg -n 'SCHEMA_ROOT_URL|SCHEMA_PACK_REFRESH' doge-complaints-gateway/src/core/config
```
