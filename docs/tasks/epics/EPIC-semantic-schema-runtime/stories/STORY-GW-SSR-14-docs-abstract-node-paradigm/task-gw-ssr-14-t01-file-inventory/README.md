# task-gw-ssr-14-t01-file-inventory

## Task: docs — inventory public URL rewrite `/tallinn/` → `/node/`

## Meta
- **Story:** [STORY-GW-SSR-14](../STORY-GW-SSR-14-docs-abstract-node-paradigm.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000071
- **Skill declared:** python-pro
- **Depends on:** SSR-13 Done (G13 PASS; public routes `/node/*`)
- **Scaffolded:** 2026-08-29T19:26:54Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-14-docs-abstract-node-paradigm.md` T01 inventory

## Purpose
Walk `$storyFile` tables verbatim. Each file → patched (`/tallinn/issues|network-pulse|emerging-signals` → `/node/…` as **current** contract) **or** N/A (нет публичного URL / только geo / SSR-13 already closed / historical Accepted). Leftover `docs/requirements` `/tallinn/` grep: same rule; do not invent files. INDEX/dashboard/SSR-08/11: patch only if still old read path. `spa-mvp-dashboard.md` = N/A + gate comment. G14: каждый файл patched или N/A. Не аудиты. Не geo `settlement:tallinn`. Не T-wave G3.

## Code Facts
- Public routes already `/node/*` — [`asgi_app.py:421–518`](../../../../../../../src/core/api/asgi_app.py)
- openapi already `/node` — [`openapi.yaml:1008,1071,1126,1301`](../../../../../../runtime-docs/api-reference/openapi.yaml)
- spa-16 already `GET /node/issues` — [`16-semantic-schema-spa-compatibility.md:5,24,43`](../../../../../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md)
- REQ-51 already `GET /node/issues` — [`51-semantic-schema-runtime.md:5,59`](../../../../../../requirements/51-semantic-schema-runtime.md)
- API_REFERENCE still teaches `/tallinn/…` — [`API_REFERENCE.md:21,570–832`](../../../../../../runtime-docs/api-reference/API_REFERENCE.md)
- 01-fastapi-transport still `/tallinn` — [`01-fastapi-transport.md:58,95,162–166`](../../../../../../runtime-docs/bootstrap-infrastructure/01-fastapi-transport.md)
- 06-testing still `client.get("/tallinn/issues")` — [`06-testing-architecture.md:192,208`](../../../../../../runtime-docs/bootstrap-infrastructure/06-testing-architecture.md)
- REQ-49/50 still `/tallinn/…` — [`49-…:26`](../../../../../../requirements/49-early-signal-network-pulse-l1-api.md); [`50-…:27`](../../../../../../requirements/50-early-signal-emerging-l2-api.md)
- spa-15 still `/tallinn/…` — [`15-…:5,55–61,108`](../../../../../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md); [`README-index.md:42`](../../../../../../../../spa-app/docs/requirements/README-index.md)
- Geo examples live — [`clustering-story-to-issue.md:218,370,399–403`](../../../../../../runtime-docs/clustering-story-to-issue.md) `settlement:tallinn`
- Inventory SSOT — [`STORY-GW-SSR-14-….md`](../STORY-GW-SSR-14-docs-abstract-node-paradigm.md) §Подзадачи
- G14 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.6

## Acceptance / DoD
- [x] Инвентарь T01 закрыт: каждый файл patched или N/A с причиной
- [x] Операционные runtime-docs не учат `GET /tallinn/issues` как текущий контракт
- [x] Аудиты T-wave / SPA-ES не переписаны
- [x] Geo examples `settlement:tallinn` живы
- [x] `spa-mvp-dashboard.md` N/A + comment (не править)
- [x] BULLRUN phases complete

## Where to change
- Only files in `$storyFile` tables + leftover `docs/requirements` hits that still teach current public URL
- Runtime-docs still teaching `/tallinn/issues|network-pulse|emerging-signals` (this scaffold): `API_REFERENCE.md`, `01-fastapi-transport.md`, `06-testing-architecture.md`, `security-env-api-access.md`, `story-persistence-model.md`, `clustering-story-to-issue.md` (§результат GET only), manuals (`schema-packs-node-data-model-ru.md`, `seed-demo-data-runbook-ru.md`, `server-env-quickstart.md`), `taxonomy-update-process-ru.md`
- REQ-49 / REQ-50 path canon (не семантика L1/L2); spa-15 sibling URLs; spa `README-index.md` строка 15
- N/A-likely this scaffold (comment in gate): `openapi.yaml`, REQ-51, spa-16, INDEX/dashboard/SSR-08/11, `spa-mvp-dashboard.md`

## Out of scope
- Invent manuals; patch `audit-gw-ssr-0*` / `audit-STORY-SPA-ES-*`; rewrite G3; touch geo `settlement:tallinn` / pack id `tallinn_civic`; change L1/L2 semantics; overlay UI; `src/**`; SSR-15 pytest
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens`. Не менять civic factory / `PromotionGatePolicy` default True.
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`.
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12/15. Не reopen 01–05/08–11/13 product/code.
  - Не invent manuals beyond `$storyFile` inventory.
  - Не патчить `docs/analysis/audit-gw-ssr-0*` / spa `audit-STORY-SPA-ES-*`.
  - Не переписывать T-wave G3 (`orchestrator-t-wave-runbook.md` :271).
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-app/docs/tasks/spa-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Overlay UI spa-app — **not this story**.
  - Не менять смысл Pulse/Emerging — только путь.

## Verification commands
```bash
rg -n "/tallinn/(issues|network-pulse|emerging-signals)" \
  doge-complaints-gateway/docs/runtime-docs \
  doge-complaints-gateway/docs/requirements/51-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/requirements/49-early-signal-network-pulse-l1-api.md \
  doge-complaints-gateway/docs/requirements/50-early-signal-emerging-l2-api.md \
  spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md \
  spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md
rg -n "settlement:tallinn" doge-complaints-gateway/docs/runtime-docs/clustering-story-to-issue.md
```
