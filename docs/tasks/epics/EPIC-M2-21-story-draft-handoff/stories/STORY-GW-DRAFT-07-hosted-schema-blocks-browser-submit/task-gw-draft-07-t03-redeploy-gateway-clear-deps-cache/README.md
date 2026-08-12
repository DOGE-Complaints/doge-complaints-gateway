# task-gw-draft-07-t03-redeploy-gateway-clear-deps-cache

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** ops
- **Status:** 🟢 Done
- **Package:** pkg-000056
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Backlog T03: redeploy/restart Railway `doge-complaints-gateway` so `_cached_dependencies` (`@lru_cache`) rebuilds and picks up new schema readiness.

## Code Facts
- Cache — [`asgi_app.py:228-238`](../../../../../../../../src/core/api/asgi_app.py) `@lru_cache(maxsize=1)` on `_cached_dependencies`; `get_api_dependencies()` returns cached `ApiDependencies` including `db_ready`
- Clear helper exists — `_clear_api_dependencies_cache()` at [`asgi_app.py:233-234`](../../../../../../../../src/core/api/asgi_app.py) but hosted process restart/redeploy is the operational path
- Readiness baked at build — [`dependencies.py:51-95`](../../../../../../../../src/core/api/dependencies.py)

## Acceptance / DoD
- [x] Traces story target #3: gateway process restarted/redeployed after DDL
- [x] New process started (deployment id / restart evidence recorded)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t03.md`](./acceptance-verification-gw-draft-07-t03.md) signed (Date post P3 verify only)

## Where to change
- Railway service `doge-complaints-gateway` (redeploy/restart) — no `src/` required

## Out of scope
- `/ready` assertion (T04); browser submit (T05); SPA changes

## Verification commands
```bash
# Operator: Railway redeploy or restart doge-complaints-gateway
# Record deployment id / timestamp in acceptance-verification-gw-draft-07-t03.md
```
