# task-gw-ssr-21-t05-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for SSR-21 persistent SSOT

## Meta
- **Story:** [STORY-GW-SSR-21](../STORY-GW-SSR-21-node-clustering-docs.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000078 (parent product AC Done); wave `run_mode=gw_ssr_21_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-21
- **Depends on:** T01–T04 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-21-node-clustering-docs-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-21-node-clustering-docs-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T19:56:41Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-21_gap_20260830T195641Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T19:57:31Z

## Purpose
Закрыть G1 (MEDIUM): backlog + pipeline §Verified still present-tense «05-env учит CLUSTER_* из env» vs Не текущий SSOT / pack civic. Confirm epic/dashboard As-of-Done SSR-21. Docs only. No runtime. No T-wave G3 rewrite. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-21-node-clustering-docs-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-21-node-clustering-docs-2026-08-30.md) §3 / §5.
2. 05-env **Не текущий SSOT** — [`05-env-config-and-launch.md:111–113`](../../../../../../../runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md).
3. server-env knobs не env — [`server-env-quickstart.md:118`](../../../../../../../runtime-docs/manuals/server-env-quickstart.md).
4. Мануал §два контура — [`schema-packs-node-data-model-ru.md:59–80`](../../../../../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md).
5. Stale backlog §Verified — [`STORY-GW-SSR-21-node-clustering-docs.md:24–31`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md).
6. Stale pipeline §Verified — [`STORY-GW-SSR-21-node-clustering-docs.md:50–57`](../STORY-GW-SSR-21-node-clustering-docs.md).
7. Dashboard Status already Done — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md).
8. Pointer stays pkg-000078 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
9. Product AC T01–T04 yes; G21 gate PASS 2026-08-30T19:53:57Z.

## Gap / Проблема
Present-tense story §Verified contradicts manuals after P3. Operators still see «05-env учит CLUSTER_* из env».

## Acceptance / DoD
- [x] Backlog SSR-21 §Verified: As-of-Done (05-env moved/pack; cron stay; мануал два контура; server-env не требует semantic CLUSTER_*) vs Historical («учит из env» / CLUSTER_ACTIVE_LENSES обязателен)
- [x] Pipeline §Verified synced (same split)
- [x] Epic/dashboard As-of-Done SSR-21 confirmed (Status Done; cluster-knobs 19–21 closed)
- [x] No `src/` / ClusterLens / `GET /schema-active` / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] T-wave G3 `:271` **не** переписан
- [x] `current.yaml` stays pkg-000078
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-21-t05.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-21-node-clustering-docs/STORY-GW-SSR-21-node-clustering-docs.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (confirm/add As-of-Done SSR-21)
- `doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md` (confirm As-of-Done)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; `GET /schema-active`; GPT UI
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000078
- `gateway-mvp-dashboard.md`; pie T-wave; T-wave G3 rewrite
- Invent SSR-06/07/12; reopen 01–20 product; start 22…25
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-06/07/12.
  - Не переписывать T-wave G3.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n '05-env учит CLUSTER_|CLUSTER_ACTIVE_LENSES' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-21-node-clustering-docs/STORY-GW-SSR-21-node-clustering-docs.md
rg -n 'As-of-Done \(SSR-21' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
sed -n '271p' doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```
