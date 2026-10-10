# task-gw-req56-02-t05-audit-g3-binding-line-refs

## Task: docs — refresh or drop brittle list binding line refs (G3)

## Meta
- **Story:** [STORY-GW-REQ56-02](../STORY-GW-REQ56-02-api-docs-search-param.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Done at:** 2026-10-10T16:50:05Z
- **Package:** pkg-000112 (parent product AC Done); wave `run_mode=gw_req56_02_audit_followup`
- **Skill declared:** python-pro
- **Soft skill:** code-documenter
- **Wave:** audit follow-up GW-REQ56-02
- **Depends on:** soft T04 (same wave)
- **Audit ref:** [`audit-gw-req56-02-api-docs-search-param-2026-10-10.md`](../../../../../../analysis/audit-gw-req56-02-api-docs-search-param-2026-10-10.md) **G3**
- **Scaffolded:** 2026-10-10T16:45:04Z
- **Completed:** 2026-10-10T16:50:05Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req56_02_gap_20261010T164014Z.plan.md` G3 TASKED follow_up=none

## Purpose
Закрыть G3 (LOW): `### GET /node/issues` HTTP binding still cites brittle `asgi_app.py:462` → `handlers.py:385`. Prefer symbol-level cites. Product search AC **не** reopen. G2 WAIVED.

## Code Facts
### As-of-Done (P6 2026-10-10T16:50:05Z)
1. List binding → `asgi_app.issues_list` → `handlers.handle_issues_list` (no brittle `:NNN`).
2. Live symbols Present — `issues_list` / `handle_issues_list`.
3. G3 **CLOSED**. Pointer stays pkg-000112.

### Historical (pre-P6 / audit)
1. Stale `asgi_app.py:462` / `handlers.py:385` line refs.

## Gap
**G3 CLOSED:** brittle list binding line refs dropped for durable symbols.

## Acceptance / DoD
- [x] List section binding no longer claims false line numbers (refresh or drop)
- [x] Prefer durable symbol cites over brittle `:NNN`
- [x] T03 product gate **не** reopen
- [x] No runtime rewrite; no invent AC
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000112
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-02-t05.md` signed (P6)

## Where to change
- `docs/runtime-docs/api-reference/API_REFERENCE.md` — `### GET /node/issues` HTTP binding line

## Out of scope
Rewrite §Актуальная точка (G2 WAIVED); mutate pkg/current; reopen product AC; mass-fix all endpoints' line refs beyond list.

## Verification commands
```bash
rg -n "HTTP binding state|asgi_app|handle_issues_list" doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md | head -20
rg -n "def issues_list|def handle_issues_list" doge-complaints-gateway/src/core/api/asgi_app.py doge-complaints-gateway/src/core/api/handlers.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
