# task-gw-ssr-19-t06-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for SSR-19 persistent SSOT

## Meta
- **Story:** [STORY-GW-SSR-19](../STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000076 (parent product AC Done); wave `run_mode=gw_ssr_19_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-19
- **Depends on:** T00–T05 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-19-node-clustering-pack-contract-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-19-node-clustering-pack-contract-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T19:26:22Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-19_gap_20260830T192622Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T19:28:00Z

## Purpose
Закрыть G1 (MEDIUM): backlog + pipeline §Verified still present-tense «Нет `node_clustering` в loader» vs code required parse. Confirm epic/dashboard As-of-Done SSR-19. Docs only. No runtime. No factory wire. No ClusterLens. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-19-node-clustering-pack-contract-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-19-node-clustering-pack-contract-2026-08-30.md) §3 / §5.
2. Loader requires `node_clustering.civic` — [`resolver.py:82–85,310`](../../../../../../../src/core/schema/resolver.py).
3. Dataclass on SchemaContext — [`contracts.py:51–85`](../../../../../../../src/core/schema/contracts.py).
4. Factory still AppConfig CLUSTER_* — [`service_factory.py:93–113`](../../../../../../../src/core/infrastructure/service_factory.py).
5. Stale backlog §Verified — [`STORY-GW-SSR-19-node-clustering-pack-contract.md:26–32`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md).
6. Stale pipeline §Verified — [`STORY-GW-SSR-19-node-clustering-pack-contract.md:55–60`](../STORY-GW-SSR-19-node-clustering-pack-contract.md).
7. Dashboard Status already Done — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md).
8. Pointer stays pkg-000076 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
9. Product AC T00–T05 yes; G19 5 passed; gate PASS 2026-08-30T19:21:58Z.

## Gap / Проблема
Present-tense story §Verified contradicts loader Done. Operators reading backlog/pipeline still see «Нет `node_clustering` в loader».

## Acceptance / DoD
- [x] Backlog SSR-19 §Verified: As-of-Done (`node_clustering.civic` required parse → SchemaContext; missing/invalid → `UnsupportedVersionError`; factory still CLUSTER_*) vs Historical («нет в loader»)
- [x] Pipeline §Verified synced (same split)
- [x] Epic/dashboard As-of-Done SSR-19 confirmed (Status Done; cluster-knobs 19 closed, 20–21 Todo)
- [x] No `src/` / ClusterLens / factory wire / `GET /schema-active` / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000076
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-19-t06.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-19-node-clustering-pack-contract/STORY-GW-SSR-19-node-clustering-pack-contract.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (confirm As-of-Done)
- `doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md` (confirm As-of-Done)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; factory wire (→20); `ClusterLens`; `GET /schema-active`; GPT UI
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000076
- `gateway-mvp-dashboard.md`; pie T-wave
- Invent SSR-06/07/12; reopen 01–18 product; start 20/21
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не factory / handler wire.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-06/07/12.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'Нет `node_clustering` в loader' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-19-node-clustering-pack-contract/STORY-GW-SSR-19-node-clustering-pack-contract.md
rg -n 'As-of-Done \(SSR-19' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
