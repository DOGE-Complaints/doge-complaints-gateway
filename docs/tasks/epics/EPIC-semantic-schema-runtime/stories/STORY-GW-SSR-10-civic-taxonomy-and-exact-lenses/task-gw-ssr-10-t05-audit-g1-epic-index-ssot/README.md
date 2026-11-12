# task-gw-ssr-10-t05-audit-g1-epic-index-ssot

## Task: add — epic Meta/PS/DoD + INDEX Progress + story Verified As-of-Done

## Meta
- **Story:** [STORY-GW-SSR-10](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000068 (parent product Done); wave `run_mode=gw_ssr_10_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-10
- **Depends on:** T00–T04 Done (product AC/DoD, G10)
- **Audit ref:** [`audit-gw-ssr-10-civic-taxonomy-and-exact-lenses-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-10-civic-taxonomy-and-exact-lenses-2026-08-29.md) **G1**
- **Scaffolded:** 2026-08-29T18:39:40Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-10_gap_20260829T183828Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-29T18:41:29Z

## Purpose
Закрыть G1 (MEDIUM): persistent SSOT drift — epic Meta `:4` still «SSR-10…11 + 13…15 🟡 Todo»; Problem Statement `:16` still lumps «Backlog (SSR-10…11 + 13…15 Todo): dual taxonomy+exact»; DoD `:67–73` lists SSR-09 без SSR-10; INDEX Progress `:110` still «SSR-10…11 + 13…15 Todo (5)» vs header `:14` / row 85 **Done**; backlog+pipeline present-tense «Сейчас код пути B нет» + §Verified stale. Split PS As-of-Done (Path B `dual_civic_lenses` opt-in; default exact-only; `ClusterLens`=10; G10 PASS 2026-08-29T18:31:19Z) vs remaining backlog (SSR-11 + 13…15 Todo). Meta/DoD/INDEX Progress. Story §Verified As-of-Done vs Historical. Без runtime. Без rewrite §«Актуальная точка» (G2 WAIVED). **G10:** dual opt-in; no new `ClusterLens` member.

## Code Facts
1. Audit G1 — [`audit-gw-ssr-10-civic-taxonomy-and-exact-lenses-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-10-civic-taxonomy-and-exact-lenses-2026-08-29.md) §3 / §5.
2. Path B code exists — [`cluster_orchestrator.py:121`](../../../../../../../src/core/application/cluster_orchestrator.py) `_process_bound_story`; [`:93`](../../../../../../../src/core/application/cluster_orchestrator.py) `dual_civic_lenses_for`.
3. Package INDEX row 10 SSR-10 Done — [`INDEX.md:85`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) 🔵 Done (Awaiting Commits).
4. INDEX header already Done-lump — [`INDEX.md:14`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) «SSR-08 + SSR-09 + SSR-10 Done».
5. INDEX Progress still Todo-lump — [`INDEX.md:110`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) «SSR-08 + SSR-09 Done; **SSR-10…11 + 13…15 Todo (5)**».
6. Epic Scope SSR-10 Done — [`EPIC-semantic-schema-runtime.md:29`](../../../../EPIC-semantic-schema-runtime.md) Done pkg-000068 gate PASS 2026-08-29T18:31:19Z.
7. Epic Stories row SSR-10 Done — [`EPIC-semantic-schema-runtime.md:86`](../../../../EPIC-semantic-schema-runtime.md) 🔵 Done pkg-000068.
8. Epic Meta still Todo-lump — [`EPIC-semantic-schema-runtime.md:4`](../../../../EPIC-semantic-schema-runtime.md) «SSR-10…11 + 13…15 🟡 Todo».
9. Epic Problem Statement still Todo-lump — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md) «**Backlog (SSR-10…11 + 13…15 Todo):** dual taxonomy+exact».
10. Epic DoD lists SSR-09, no SSR-10 — [`EPIC-semantic-schema-runtime.md:67–73`](../../../../EPIC-semantic-schema-runtime.md).
11. Backlog present-tense Path B absent — [`STORY-GW-SSR-10:33`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md); pipeline [`:60`](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md); Verified [`:36–43`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md) / pipeline [`:66–75`](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md).
12. Loader key documented — [`schema-packs/README.md:28`](../../../../../../../schema-packs/README.md) `dual_civic_lenses`.
13. Bullrun §«Актуальная точка» still MVP ES-03/M2-24 — [`bullrun-launch-index.md:17–20`](../../../../../bullrun-launch-index.md) (G2 WAIVED — **do not rewrite**).
14. Pointer stays pkg-000068 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
15. Product Story Done (AC/DoD, G10) = **yes**. Empty OPEN gap-list = **no** until this task + P7 (G2 WAIVED kept).

## Gap / Проблема
Persistent SSOT (не `docs/analysis/**`): epic Meta/Problem Statement/DoD, INDEX Progress, и story §Verified still present-tense Todo / «кода пути B нет» after pkg-000068 G10 Done.

## Acceptance / DoD
- [x] Epic Meta `:4`: «SSR-08 + SSR-09 + SSR-10 🔵 Done»; remaining Todo 11 + 13…15 (not «SSR-10…15 Todo»)
- [x] Epic Problem Statement `:16`: As-of-Done SSR-10 (Path B `dual_civic_lenses` opt-in; default exact-only; `ClusterLens`=10; G10 PASS 2026-08-29T18:31:19Z) vs remaining backlog (SSR-11 + 13…15 Todo)
- [x] Epic DoD `:67–73`: add SSR-10 product Done (pkg-000068 T00–T04); gate PASS 2026-08-29T18:31:19Z
- [x] INDEX Progress `:110`: «SSR-08 + SSR-09 + SSR-10 Done»; remaining Todo 11 + 13…15 (4), not «SSR-10…15 Todo (5)»; header `:14` / row 85 stay Done
- [x] Backlog + pipeline SSR-10: As-of-Done vs Historical on «Сейчас код пути B нет» + §Verified (Path B **есть**: `_process_bound_story` / `dual_civic_lenses`)
- [x] Epic Scope `:29` Done **не** revert; Stories `:86` Done **не** revert
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] Нет invented `EPIC-M2-*` rows
- [x] No `src/` / `ClusterLens` / civic factory / identity edits
- [x] No pytest this wave (docs-only)
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-10-t05.md` signed (Date post P6 live `--verify` + `--print-utc-now` only)

## Where to change
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (Meta `:4`, Problem Statement `:16`, DoD `:67–73`)
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` (Progress `:110` only; header `:14` / row 85 stay Done)
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md` (§«Сейчас код пути B нет» + §Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md` (same sections)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / dual flag / orchestrator / `ClusterLens` / civic factory / invent HTTP
- `gateway-mvp-dashboard.md`; pie T-wave
- New pkg; `gateway-active-package.current.yaml` stays pkg-000068
- SSR-06/07/11/12/13; reopen 01–05/08/09; T-wave G3 / `audit-gw-ssr-0[1-5]*` rewrite
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79) как default для всех packs.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/11/12/13. Не reopen 01–05/08/09.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'SSR-10…11 \+ 13…15|As-of-Done \(SSR-10|кода пути B нет|_process_bound_story' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md
# G2: heading block 17–20 must still be EPIC-M2-24 / ES-03 (do not rewrite)
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
