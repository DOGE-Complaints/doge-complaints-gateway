# Story acceptance gate — STORY-GW-SSR-14

- **Story:** Docs: abstract node public API (inventory)
- **Package:** `pkg-000071-20260829-gw-ssr-14-docs-abstract-node-paradigm.yaml`
- **Result:** PASS
- **Date:** 2026-08-29T19:30:07Z

## G14 (runbook §6.6)

Инвентарь T01: каждый файл patched или N/A. Не аудиты. Не geo `settlement:tallinn`. Не T-wave G3.

| G14 check | Result | Evidence |
|-----------|--------|----------|
| runtime-docs / REQ 49/50/51 / spa-15/16 **не** учат `/tallinn/…` как текущий контракт | PASS | G14 `rg "/tallinn/(issues\|network-pulse\|emerging-signals)"` empty on those paths |
| T-wave runbook G3 строка на месте (исторический) | PASS | `orchestrator-t-wave-runbook.md:271` `` `GET /tallinn/issues` на месте `` — not rewritten; `stays` string not invented |
| `docs/analysis/audit-gw-ssr-0*` не в diff | PASS | audits untouched |
| `CLUSTER_GEO_SCOPE` примеры с городом живы | PASS | `clustering-story-to-issue.md:218,370,399–403` `settlement:tallinn` |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Инвентарь T01 закрыт: каждый файл patched или N/A с причиной. | PASS | `acceptance-verification-gw-ssr-14-t01.md` — story-table patched 14 / N/A 3 |
| Операционные runtime-docs не учат `GET /tallinn/issues` как текущий контракт. | PASS | `rg` empty in `docs/runtime-docs` for `/tallinn/(issues\|network-pulse\|emerging-signals)` |
| Аудиты T-wave / SPA-ES не переписаны. | PASS | `audit-gw-ssr-0*` / `audit-STORY-SPA-ES-*` not in this story diff |
| Geo examples `settlement:tallinn` живы. | PASS | `clustering-story-to-issue.md` geo examples kept |

## Commands (live verification 2026-08-29T19:30:07Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
rg -n "/tallinn/(issues|network-pulse|emerging-signals)" \
  doge-complaints-gateway/docs/runtime-docs \
  doge-complaints-gateway/docs/requirements/51-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/requirements/49-early-signal-network-pulse-l1-api.md \
  doge-complaints-gateway/docs/requirements/50-early-signal-emerging-l2-api.md \
  spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md \
  spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md
rg -n "GET /tallinn/issues stays" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
rg -n "GET /tallinn/issues" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
rg -n "settlement:tallinn" doge-complaints-gateway/docs/runtime-docs/clustering-story-to-issue.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)

## Residual (not story AC)

SSR-06/07/12/15 not started. SSR-01…05 / 08–11 / 13 not reopened. Pie T-wave unchanged. bullrun §«Актуальная точка» unchanged. `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md` unchanged. pkg-000071 immutable. openapi.yaml N/A (already `/node`).
