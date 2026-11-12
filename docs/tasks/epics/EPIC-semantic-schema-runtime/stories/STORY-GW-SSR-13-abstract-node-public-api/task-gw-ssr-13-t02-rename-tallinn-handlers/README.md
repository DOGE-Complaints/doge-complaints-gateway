# task-gw-ssr-13-t02-rename-tallinn-handlers

## Task: refactor — rename `handle_tallinn_*` + asgi imports (T02)

## Meta
- **Story:** [STORY-GW-SSR-13](../STORY-GW-SSR-13-abstract-node-public-api.md)
- **Type:** refactor
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000069
- **Skill declared:** python-pro
- **Depends on:** T01 routes registered on `/node/*`
- **Scaffolded:** 2026-08-29T18:50:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md` T02

## Purpose
Rename `handle_tallinn_issues_list` / `_get` / `_create` → `handle_issues_list` / `handle_issue_get` / `handle_issue_create`; update asgi imports/calls. Pulse/Emerging handlers already `handle_network_pulse` / `handle_emerging_signals` — **no** rename unless a `tallinn` token remains in `src/core/api` (asgi wrapper fn names `tallinn_*` must go so `rg /tallinn/` is empty).

## Code Facts
- Imports `handle_tallinn_*` — [`asgi_app.py:35–37`](../../../../../../../src/core/api/asgi_app.py)
- Issue handlers city names — [`handlers.py:385`](../../../../../../../src/core/api/handlers.py) `handle_tallinn_issues_list`; [`:433`](../../../../../../../src/core/api/handlers.py) `_get`; [`:462`](../../../../../../../src/core/api/handlers.py) `_create`
- Pulse/Emerging handlers — [`handlers.py:40`](../../../../../../../src/core/api/handlers.py) `handle_network_pulse`; [`:51`](../../../../../../../src/core/api/handlers.py) `handle_emerging_signals` — **no** `tallinn` in name
- Call sites — [`asgi_app.py:482`](../../../../../../../src/core/api/asgi_app.py), [`:510`](../../../../../../../src/core/api/asgi_app.py), [`:526`](../../../../../../../src/core/api/asgi_app.py)
- G13 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.4

## Acceptance / DoD
- [x] `/tallinn/` отсутствует в `src/core/api` (handler names + imports + wrapper fn names)
- [x] asgi imports/calls use `handle_issues_list` / `handle_issue_get` / `handle_issue_create`
- [x] Pulse/Emerging semantics unchanged (`handle_network_pulse` / `handle_emerging_signals`)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/api/handlers.py` (`:385+`)
- `doge-complaints-gateway/src/core/api/asgi_app.py` (`:35–37`, call sites `:482`, `:510`, `:526`; wrapper names `tallinn_*`)

## Out of scope
- Новая семантика Pulse/Emerging; rewrite closed T-wave G3 audits; API_REFERENCE full pass (SSR-14)
- INDEX/runbook §8 + fence hard bans:
  - **Hard cut `/tallinn/*` — NO alias.** Do not keep both prefixes.
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`.
  - Не расширять `ClusterLens` (`types.py` :10–22).
  - `CLUSTER_GEO_SCOPE=settlement:tallinn` и pack id `tallinn_civic` **stay**.
  - Overlay UI spa-app — **not this story** (SSR-11).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/11/12/14/15. Не reopen 01–05/08–10.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Полный pytest URL / rename `test_req24_*` — **SSR-15 / G15**, не G13 HALT.
  - Не коммитить spa-app nested git без явной команды (P8 skip spa git).
  - Полный API_REFERENCE / manuals — SSR-14.
  - REQ-45 GPT — out.

## Verification commands
```bash
rg -n "handle_tallinn_|/tallinn/|def tallinn_" doge-complaints-gateway/src/core/api
rg -n "handle_issues_list|handle_issue_get|handle_issue_create|handle_network_pulse|handle_emerging_signals" \
  doge-complaints-gateway/src/core/api/handlers.py \
  doge-complaints-gateway/src/core/api/asgi_app.py
```
