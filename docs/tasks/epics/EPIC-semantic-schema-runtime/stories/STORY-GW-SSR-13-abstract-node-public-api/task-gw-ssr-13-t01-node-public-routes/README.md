# task-gw-ssr-13-t01-node-public-routes

## Task: implement — `/node/*` public routes + PUBLIC_ROUTES (T01)

## Meta
- **Story:** [STORY-GW-SSR-13](../STORY-GW-SSR-13-abstract-node-public-api.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000069
- **Skill declared:** python-pro
- **Depends on:** SSR-05 Done
- **Scaffolded:** 2026-08-29T18:50:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md` T01

## Purpose
Replace city prefixes in `PUBLIC_ROUTES` + OPTIONS + GET/POST wrappers with `/node/…`. Remove `/tallinn/` route registrations. Do not keep a second prefix. G13: five families on `/node/…` + `PUBLIC_ROUTES`; no alias.

## Code Facts
- `PUBLIC_ROUTES` city paths — [`asgi_app.py:59–67`](../../../../../../../src/core/api/asgi_app.py) `/tallinn/issues`, `network-pulse`, `emerging-signals`
- OPTIONS + GET/POST city — [`asgi_app.py:421–526`](../../../../../../../src/core/api/asgi_app.py) (story cite `:421–518`; POST create continues `:518–526`)
- GET list / get / POST — [`:462`](../../../../../../../src/core/api/asgi_app.py) / [`:504`](../../../../../../../src/core/api/asgi_app.py) / [`:518`](../../../../../../../src/core/api/asgi_app.py)
- Config write-route string — [`config/schema.py:127`](../../../../../../../src/core/config/schema.py) `POST /tallinn/issues`
- Geo example stay — [`config/schema.py:225`](../../../../../../../src/core/config/schema.py) `settlement:tallinn`
- G13 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.4

## Acceptance / DoD
- [x] Канон: `GET/POST /node/issues`, `GET /node/issues/{issue_id}`, `GET /node/network-pulse`, `GET /node/emerging-signals`
- [x] Нет alias (нет второго префикса `/tallinn/` в asgi)
- [x] `PUBLIC_ROUTES` lists `/node/issues`, `/node/network-pulse`, `/node/emerging-signals` (not city)
- [x] `config/schema.py:127` names `POST /node/issues`; `:225` geo example unchanged
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/api/asgi_app.py` (`:59–67`, `:421–526`)
- `doge-complaints-gateway/src/core/config/schema.py:127` (POST path string only)

## Out of scope
- Alias `/tallinn`; новая семантика Pulse/Emerging; invent filter HTTP
- INDEX/runbook §8 + fence hard bans:
  - **Hard cut `/tallinn/*` — NO alias.** Do not keep both prefixes.
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`.
  - Не расширять `ClusterLens` (`types.py` :10–22).
  - `CLUSTER_GEO_SCOPE=settlement:tallinn` и pack id `tallinn_civic` **stay** (`schema.py:225`).
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
rg -n "/tallinn/|/node/" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "POST /tallinn/issues|POST /node/issues|settlement:tallinn" \
  doge-complaints-gateway/src/core/config/schema.py
```
