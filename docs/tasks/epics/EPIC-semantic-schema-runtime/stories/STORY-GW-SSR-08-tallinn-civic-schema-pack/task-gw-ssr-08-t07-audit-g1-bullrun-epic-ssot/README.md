# task-gw-ssr-08-t07-audit-g1-bullrun-epic-ssot

## Task: add — bullrun SSR-08 rows + epic Problem Statement As-of-Done

## Meta
- **Story:** [STORY-GW-SSR-08](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000066 (parent product Done); wave `run_mode=gw_ssr_08_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-08
- **Depends on:** T00–T06 Done (product AC/DoD)
- **Audit ref:** [`audit-gw-ssr-08-tallinn-civic-schema-pack-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-08-tallinn-civic-schema-pack-2026-08-29.md) **G1**
- **Scaffolded:** 2026-08-29T18:00:42Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-08_gap_20260829T175900Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-29T18:02:52Z

## Purpose
Закрыть G1 (MEDIUM): persistent SSOT drift — `bullrun-launch-index.md` имеет **0 rows** SSR-08 / pkg-000066; epic Problem Statement still lumps «Backlog (SSR-08…11 + 13…15 Todo): civic-as-pack» vs Scope/Stories SSR-08 **Done**. Добавить **существующие** EPIC-semantic-schema-runtime / SSR-08 story+task rows **ниже** §«Актуальная точка»; split Problem Statement As-of-Done (SSR-08 civic-as-pack Done pkg-000066) vs remaining backlog (SSR-09…11 + 13…15 Todo). Без runtime. Без rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-08-tallinn-civic-schema-pack-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-08-tallinn-civic-schema-pack-2026-08-29.md) §3 / §5: Grep `SSR-08` / `pkg-000066` / `tallinn_civic` / `GW-SSR-08` in bullrun = **0 matches**.
2. Package INDEX SSR-08 Done — [`INDEX.md`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) row 8 🔵 Done (Awaiting Commits).
3. Epic Scope SSR-08 Done — [`EPIC-semantic-schema-runtime.md:27`](../../../../EPIC-semantic-schema-runtime.md) Done pkg-000066 gate PASS 2026-08-29T17:52:54Z.
4. Epic Stories row SSR-08 Done — [`EPIC-semantic-schema-runtime.md:83`](../../../../EPIC-semantic-schema-runtime.md).
5. Epic Problem Statement still Todo-lump — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md) «**Backlog (SSR-08…11 + 13…15 Todo):** civic-as-pack» vs Scope Done.
6. Bullrun §«Актуальная точка» still MVP ES-03/M2-24 — [`bullrun-launch-index.md:17–20`](../../../../../bullrun-launch-index.md) (G2 WAIVED — **do not rewrite**).
7. Pack on disk — [`schema-packs/tallinn_civic/v1/pack.json`](../../../../../../../schema-packs/tallinn_civic/v1/pack.json).
8. Product T00–T06 — story folder [`STORY-GW-SSR-08-tallinn-civic-schema-pack/`](../).
9. Pointer stays pkg-000066 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
10. Product Story Done (AC/DoD) = **yes**. Empty OPEN gap-list = **no** until this task + P7.

## Gap / Проблема
Persistent SSOT (не `docs/analysis/**`): launch index не содержит существующих EPIC-semantic-schema-runtime / SSR-08 rows; epic Problem Statement still present-tense Todo for civic-as-pack after pkg-000066 Done.

## Acceptance / DoD
- [x] `bullrun-launch-index.md` содержит rows для **existing** `EPIC-semantic-schema-runtime` + STORY-GW-SSR-08 (pipeline + backlog + pkg-000066 + T00–T06 paths), **ниже** §«Актуальная точка»
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] Нет invented `EPIC-M2-*` rows
- [x] Epic Problem Statement: As-of-Done (SSR-08 civic-as-pack Done pkg-000066) vs Historical / remaining backlog (SSR-09…11 + 13…15 Todo)
- [x] Epic Scope / Stories Done rows **не** revert
- [x] No `src/` / civic enum / pack runtime / identity edits
- [x] No pytest this wave (docs-only)
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-08-t07.md` signed (Date post P6 live `--verify` + `--print-utc-now` only)

## Where to change
- `doge-complaints-gateway/docs/tasks/bullrun-launch-index.md` (new § EPIC-semantic-schema-runtime / SSR-08 rows **below** §«Актуальная точка»; **not** that heading)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (§Problem Statement As-of-Done vs remaining Todo)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime pack/civic / `ClusterLens` / factory / identity
- `gateway-mvp-dashboard.md`; pie T-wave
- New pkg; `gateway-active-package.current.yaml` stays pkg-000066
- SSR-06/07/09/12; T-wave G3 / `audit-gw-ssr-0*` rewrite
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не invent HTTP filter / новый intake path. `GET /tallinn/issues` must stay (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
  - `build_index` / `project` — stub/no-op (`runtime.py` :62–72).
  - Не переименовывать `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0*`.
  - Civic path без binding **must stay**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'SSR-08|pkg-000066|tallinn_civic|GW-SSR-08|EPIC-semantic-schema-runtime' \
  doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
rg -n 'As-of-Done \(SSR-08|Backlog \(SSR-08|civic-as-pack' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md
# G2: heading block 17–20 must still be EPIC-M2-24 / ES-03 (do not rewrite)
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
