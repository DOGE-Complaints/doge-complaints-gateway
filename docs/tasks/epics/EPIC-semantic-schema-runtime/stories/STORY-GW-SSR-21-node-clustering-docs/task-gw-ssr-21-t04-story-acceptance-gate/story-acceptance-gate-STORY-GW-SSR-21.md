# Story acceptance gate — STORY-GW-SSR-21

- **Story:** Node clustering docs (кастомизация ноды)
- **Package:** `pkg-000078-20260830-gw-ssr-21-node-clustering-docs.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T19:53:57Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Мануал явно разделяет exact_lenses vs `node_clustering.civic`. | PASS | `schema-packs-node-data-model-ru.md` §«Два контура» |
| Операторский путь смены порогов/линз/geo = правка активного pack + рестарт. | PASS | same § how-to steps 1–3 |
| `05-env-config-and-launch.md` не учит строки 111–120 как текущий SSOT; cron documented. | PASS | table row **Не текущий SSOT**; `CLUSTER_CRON_*` `:112–113` |
| `server-env-quickstart.md` не требует семантические CLUSTER_* для кастомизации. | PASS | cluster knobs → pack; no `export CLUSTER_ACTIVE_LENSES=` |
| T-wave G3 / closed audits не в diff. | PASS | `orchestrator-t-wave-runbook.md:271` untouched; `docs/analysis/audit-*` not in this story diff |

## G21 (runbook §6.3)

| G21 check | Result | Evidence |
|-----------|--------|----------|
| мануал оба контура + pack + рестарт | PASS | `rg node_clustering\|exact_lenses` on manual |
| 05-env не текущий SSOT; cron documented | PASS | semantic names only as moved/pack; `rg CLUSTER_CRON` hits |
| T-wave G3 строка на месте | PASS | `:271` `` `GET /tallinn/issues` на месте `` (rg `stays` = 0; не invent) |
| closed audits не в diff | PASS | no `docs/analysis/audit-*` this story |

## Commands (live verification 2026-08-30T19:53:57Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
rg -n "node_clustering|exact_lenses" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "CLUSTER_MIN_SIZE|CLUSTER_ACTIVE_LENSES|CLUSTER_PRIMARY_LENS|CLUSTER_GEO_SCOPE" \
  doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md
rg -n "CLUSTER_CRON" doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md
rg -n "GET /tallinn/issues stays" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
rg -n "GET /tallinn/issues" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
