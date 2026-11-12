# acceptance-verification — GW-SSR-14 t01

- **Result:** PASS
- **Date:** 2026-08-29T19:30:07Z
- **Package:** pkg-000071

## Inventory (story tables)

| File | Disposition | Reason |
|------|-------------|--------|
| `docs/runtime-docs/api-reference/API_REFERENCE.md` | patched | Issues / Pulse / Emerging / TOC; handlers → `handle_issues_*` |
| `docs/runtime-docs/api-reference/openapi.yaml` | N/A | SSR-13 already `/node/issues\|network-pulse\|emerging-signals`; no `/tallinn/` public paths |
| `docs/runtime-docs/bootstrap-infrastructure/01-fastapi-transport.md` | patched | OPTIONS / `PUBLIC_ROUTES` / route table + handler names |
| `docs/runtime-docs/bootstrap-infrastructure/06-testing-architecture.md` | patched | `client.get("/node/issues…")` |
| `docs/runtime-docs/security-env-api-access.md` | patched | `POST /node/issues` |
| `docs/runtime-docs/story-persistence-model.md` | patched | query example list issues |
| `docs/runtime-docs/clustering-story-to-issue.md` | patched | §результат GET only; `settlement:tallinn` kept |
| `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md` | patched | карточка GET; pack id `tallinn_civic` kept |
| `docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md` | patched | curl / e2e / troubleshooting current path |
| `docs/runtime-docs/manuals/server-env-quickstart.md` | patched | POST public-content |
| `docs/runtime-docs/appendix/taxonomy-update-process-ru.md` | patched | `?labels=` filter |
| `docs/requirements/51-semantic-schema-runtime.md` | N/A | already `GET /node/issues` (SSR-13) |
| `docs/requirements/49-early-signal-network-pulse-l1-api.md` | patched | path canon only; L1 semantics unchanged |
| `docs/requirements/50-early-signal-emerging-l2-api.md` | patched | path canon only; L2 semantics unchanged |
| `spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md` | N/A | already `GET /node/issues` (SSR-13) |
| `spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md` | patched | sibling 49/50 + Issue read URLs |
| `spa-app/docs/requirements/README-index.md` | patched | строка 15 paths |

**Story-table counts:** patched **14** / N/A **3**.

## Leftover `docs/requirements` `/tallinn/`

| File | Disposition | Reason |
|------|-------------|--------|
| `docs/requirements/README-index.md` 49/50 lines | patched | taught current Pulse/Emerging paths |
| `docs/requirements/README-index.md` REQ-24 line | N/A | historical Accepted REQ-24 |
| `24` / `27` / `30` / `39` / `40` / `41` / `48` | N/A | historical Accepted; not current-contract teach |
| INDEX / dashboard / SSR-08/11 | N/A | already `/node` |
| `spa-app/docs/tasks/spa-mvp-dashboard.md` | N/A | MVP snapshot (fence) |
| T-wave G3 | N/A | historical; not rewritten |

## Commands

```bash
rg -n "/tallinn/(issues|network-pulse|emerging-signals)" \
  doge-complaints-gateway/docs/runtime-docs \
  doge-complaints-gateway/docs/requirements/51-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/requirements/49-early-signal-network-pulse-l1-api.md \
  doge-complaints-gateway/docs/requirements/50-early-signal-emerging-l2-api.md \
  spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md \
  spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md
# → empty
rg -n "settlement:tallinn" doge-complaints-gateway/docs/runtime-docs/clustering-story-to-issue.md
```
