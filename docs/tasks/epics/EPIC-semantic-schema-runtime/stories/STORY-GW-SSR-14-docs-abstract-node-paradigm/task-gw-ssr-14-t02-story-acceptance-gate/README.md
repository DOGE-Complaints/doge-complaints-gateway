# task-gw-ssr-14-t02-story-acceptance-gate

## Task: analyze — story acceptance + G14

## Meta
- **Story:** [STORY-GW-SSR-14](../STORY-GW-SSR-14-docs-abstract-node-paradigm.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000071
- **Skill declared:** python-pro
- **Depends on:** T01 Done
- **Scaffolded:** 2026-08-29T19:26:54Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-14-docs-abstract-node-paradigm.md` Target / AC + runbook §6.6
- **Gate Date:** 2026-08-29T19:30:07Z

## Purpose
Story acceptance + G14. Commands from runbook §6.6. After PASS: INDEX/dashboard Status for SSR-14; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** `spa-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-15 in this pkg.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-14-….md`](../STORY-GW-SSR-14-docs-abstract-node-paradigm.md) §Target / AC (verbatim)
- G14 commands — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.6
- T-wave G3 historical — [`orchestrator-t-wave-runbook.md:271`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) `` `GET /tallinn/issues` на месте `` — **do not rewrite**; do **not** invent `stays`
- Gate **Date:** only after `--print-utc-now` post live `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)
- spa-mvp-dashboard — [`spa-app/docs/tasks/spa-mvp-dashboard.md`](../../../../../../../../spa-app/docs/tasks/spa-mvp-dashboard.md) N/A

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-14.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-14-t02.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G14: runtime-docs / REQ 49/50/51 / spa-15/16 **не** учат `/tallinn/…` как текущий контракт (N/A только если нет публичного URL)
- [x] T-wave G3 строка на месте (`:271`); `audit-gw-ssr-0*` не в diff; `CLUSTER_GEO_SCOPE` city examples живы
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/12/15.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-14.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing docs inventory (T01); P3 execution; start SSR-15; rewrite G3 to invent `stays`
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
# P3 only (G14) — from workspace:
rg -n "/tallinn/(issues|network-pulse|emerging-signals)" \
  doge-complaints-gateway/docs/runtime-docs \
  doge-complaints-gateway/docs/requirements/51-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/requirements/49-early-signal-network-pulse-l1-api.md \
  doge-complaints-gateway/docs/requirements/50-early-signal-emerging-l2-api.md \
  spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md \
  spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md
rg -n "GET /tallinn/issues stays" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
# G3 historical line (do not invent stays):
rg -n "GET /tallinn/issues" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
rg -n "settlement:tallinn" doge-complaints-gateway/docs/runtime-docs/clustering-story-to-issue.md
```
