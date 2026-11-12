# task-gw-ssr-11-t05-audit-g1-epic-dod-ssot

## Task: add — epic Definition of Done SSR-11 line

## Meta
- **Story:** [STORY-GW-SSR-11](../STORY-GW-SSR-11-pack-declared-issue-projection.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000070 (parent product Done); wave `run_mode=gw_ssr_11_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-11
- **Depends on:** T00–T04 Done (product AC/DoD, G11)
- **Audit ref:** [`audit-gw-ssr-11-pack-declared-issue-projection-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-11-pack-declared-issue-projection-2026-08-29.md) **G1**
- **Scaffolded:** 2026-08-29T19:19:13Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-11_gap_20260829T191803Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-29T19:21:00Z

## Purpose
Закрыть G1 (MEDIUM): persistent SSOT drift — epic Definition of Done `:67–75` ends at SSR-13 — **нет** SSR-11 line — vs Scope `:31` / Stories `:90` / Problem Statement As-of-Done SSR-11 / INDEX / dashboard Done. Add DoD line SSR-11 product Done pkg-000070 T00–T04; gate PASS 2026-08-29T19:13:51Z (named `schema_card` / no dump / `GET /node/issues`). Keep Meta/Scope/Stories/PS/INDEX already Done-lump. Без runtime. Без rewrite §«Актуальная точка» (G2 WAIVED). **G11:** named sidecar; no payload dump.

## Code Facts
1. Audit G1 — [`audit-gw-ssr-11-pack-declared-issue-projection-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-11-pack-declared-issue-projection-2026-08-29.md) §3 / §5.
2. Product named sidecar — [`dto.py`](../../../../../../../src/core/projection/dto.py) no `structured_payload` token; [`card_fields.py`](../../../../../../../src/core/projection/card_fields.py); [`issue_create.py`](../../../../../../../src/core/application/issue_create.py) `_to_public_payload`; [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py) `GET /node/issues`.
3. INDEX row 11 Done — [`INDEX.md:87`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) 🔵 Done (Awaiting Commits).
4. INDEX header + Progress already Done-lump — [`INDEX.md:14,110`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) «SSR-08 + … + SSR-11 Done»; remaining Todo 14…15.
5. Epic Meta already Done-lump — [`EPIC-semantic-schema-runtime.md:4`](../../../../EPIC-semantic-schema-runtime.md) «SSR-08 + … + SSR-11 🔵 Done»; remaining Todo 14…15.
6. Epic Scope SSR-11 Done — [`EPIC-semantic-schema-runtime.md:31`](../../../../EPIC-semantic-schema-runtime.md) Done pkg-000070 gate PASS 2026-08-29T19:13:51Z.
7. Epic Stories row SSR-11 Done — [`EPIC-semantic-schema-runtime.md:90`](../../../../EPIC-semantic-schema-runtime.md) 🔵 Done pkg-000070.
8. Epic Problem Statement already As-of-Done SSR-11 — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md).
9. **Epic DoD ends at SSR-13 — no SSR-11 line** — [`EPIC-semantic-schema-runtime.md:67–75`](../../../../EPIC-semantic-schema-runtime.md) (last: SSR-13 `:75`).
10. Backlog + pipeline §Verified As-of-Done — Status 🔵 Done; AC `[x]`.
11. Dashboard SSR-11 Done — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md).
12. Bullrun §«Актуальная точка» still MVP ES-03/M2-24 — [`bullrun-launch-index.md:17–20`](../../../../../bullrun-launch-index.md) (G2 WAIVED — **do not rewrite**).
13. Pointer stays pkg-000070 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
14. Product Story Done (AC/DoD, G11) = **yes**. Empty OPEN gap-list = **no** until this task + P7 (G2 WAIVED kept).

## Gap / Проблема
Persistent SSOT (не `docs/analysis/**`): epic Definition of Done lists SSR-13 and omits SSR-11 after pkg-000070 G11 Done.

## Acceptance / DoD
- [x] Epic Definition of Done `:67–75`: add SSR-11 product Done (pkg-000070 T00–T04); gate PASS 2026-08-29T19:13:51Z (named `schema_card` / no dump / `GET /node/issues`)
- [x] Epic Scope `:31` / Stories `:90` / PS `:16` / Meta `:4` Done **не** revert
- [x] INDEX / dashboard / backlog+pipeline §Verified already As-of-Done — **keep**
- [x] Status backlog+pipeline stays 🔵 Done; do not reopen product AC T00–T04
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] Нет invented `EPIC-M2-*` rows
- [x] No `src/` / `ClusterLens` / dump payload / identity / `SchemaRuntime.project` edits
- [x] No pytest this wave (docs-only)
- [x] `gateway-mvp-dashboard.md` **не** править; pie T-wave **не** трогать
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-11-t05.md` signed (Date post P6 live `--verify` + `--print-utc-now` only)

## Where to change
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (Definition of Done `:67–75` only; Meta/Scope/Stories/PS stay Done)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / dump `structured_payload` / `ClusterLens` / invent HTTP / identity
- Implement `SchemaRuntime.project` (`runtime.py:68–72` stub stays)
- `gateway-mvp-dashboard.md`; pie T-wave
- New pkg; `gateway-active-package.current.yaml` stays pkg-000070
- SSR-06/07/12/14/15 execute; reopen 01–05/08–10/13
- T-wave G3 / `audit-gw-ssr-0[1-5]*` rewrite
- Overlay UI spa-app — **not this story**
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens`.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` и civic factory.
  - Не invent HTTP filter / IDX/QRY.
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12/14/15. Не reopen 01–05/08–10/13.
  - Не вызывать / не реализовывать `SchemaRuntime.project`.
  - Не dump `structured_payload` на карточку.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'SSR-11 product Done|SSR-13 product Done' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md
# G2: heading block 17–20 must still be EPIC-M2-24 / ES-03 (do not rewrite)
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
