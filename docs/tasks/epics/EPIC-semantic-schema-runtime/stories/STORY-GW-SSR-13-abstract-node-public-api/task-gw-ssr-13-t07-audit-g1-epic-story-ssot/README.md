# task-gw-ssr-13-t07-audit-g1-epic-story-ssot

## Task: add — epic Problem Statement + story §Verified + dashboard queue As-of-Done

## Meta
- **Story:** [STORY-GW-SSR-13](../STORY-GW-SSR-13-abstract-node-public-api.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000069 (parent product Done); wave `run_mode=gw_ssr_13_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-13
- **Depends on:** T01–T06 Done (product AC/DoD, G13)
- **Audit ref:** [`audit-gw-ssr-13-abstract-node-public-api-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-13-abstract-node-public-api-2026-08-29.md) **G1**
- **Scaffolded:** 2026-08-29T19:01:01Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-13_gap_20260829T185854Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-29T19:02:58Z

## Purpose
Закрыть G1 (MEDIUM): persistent SSOT drift — epic Problem Statement `:16` still «**Backlog (SSR-11 + 13…15 Todo): abstract `/node/*`**» vs Scope `:30` Done; backlog+pipeline §Verified still present-tense `/tallinn/issues` + `handle_tallinn_*` + OpenAPI `/tallinn/…` + spa-16 «Keep `GET /tallinn/issues`»; wave dashboard queue `:84` still «hard cut — **Todo**» vs Remaining `:43` / Last change `:7` Done. Split PS As-of-Done (hard cut `/node/*`; handlers `handle_issues_list` / `_get` / `_create`; spa three repos + spa-16/51; G13 PASS 2026-08-29T18:55:15Z) vs remaining backlog (**SSR-11 + 14…15 Todo** — drop «13» from the Todo-lump). Story §Verified As-of-Done vs Historical. Dashboard row 84 Done. Без runtime. Без rewrite §«Актуальная точка» (G2 WAIVED). **G13:** hard cut; no alias.

## Code Facts
1. Audit G1 — [`audit-gw-ssr-13-abstract-node-public-api-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-13-abstract-node-public-api-2026-08-29.md) §3 / §5.
2. Product hard cut — [`asgi_app.py:65–67`](../../../../../../../src/core/api/asgi_app.py) `/node/*` PUBLIC_ROUTES; GET/POST [`:462`](../../../../../../../src/core/api/asgi_app.py) / [`:518`](../../../../../../../src/core/api/asgi_app.py).
3. Handlers renamed — [`handlers.py:385,433,462`](../../../../../../../src/core/api/handlers.py) `handle_issues_list` / `handle_issue_get` / `handle_issue_create`.
4. INDEX row 13 Done — [`INDEX.md:86`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) 🔵 Done (Awaiting Commits).
5. INDEX header already Done-lump — [`INDEX.md:14`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) «SSR-08 + SSR-09 + SSR-10 + SSR-13 Done».
6. INDEX Progress already Done-lump — [`INDEX.md:110`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) «SSR-08 + SSR-09 + SSR-10 + SSR-13 Done»; Todo 11 + 14…15 (3).
7. Epic Meta already Done-lump — [`EPIC-semantic-schema-runtime.md:4`](../../../../EPIC-semantic-schema-runtime.md) «SSR-08 + SSR-09 + SSR-10 + SSR-13 🔵 Done»; remaining Todo 11 + 14…15.
8. Epic Scope SSR-13 Done — [`EPIC-semantic-schema-runtime.md:30`](../../../../EPIC-semantic-schema-runtime.md) Done pkg-000069 gate PASS 2026-08-29T18:55:15Z.
9. Epic Stories row SSR-13 Done — [`EPIC-semantic-schema-runtime.md:89`](../../../../EPIC-semantic-schema-runtime.md) 🔵 Done pkg-000069.
10. Epic DoD lists SSR-13 — [`EPIC-semantic-schema-runtime.md:75`](../../../../EPIC-semantic-schema-runtime.md).
11. Epic Problem Statement still Todo-lump — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md) «**Backlog (SSR-11 + 13…15 Todo): abstract `/node/*`**» vs Scope `:30` Done.
12. Backlog + pipeline §Verified stale — backlog [`STORY-GW-SSR-13:26–35`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md) present-tense `/tallinn/issues` + `handle_tallinn_*` + OpenAPI `/tallinn/…` + spa-16 Keep; pipeline [`:54–63`](../STORY-GW-SSR-13-abstract-node-public-api.md) same vs code `/node/*`.
13. Dashboard Remaining SSR-13 Done — [`gateway-semantic-schema-runtime-dashboard.md:43`](../../../../../gateway-semantic-schema-runtime-dashboard.md) 🔵 Done; Last change [`:7`](../../../../../gateway-semantic-schema-runtime-dashboard.md) Done.
14. Dashboard queue row still Todo — [`gateway-semantic-schema-runtime-dashboard.md:84`](../../../../../gateway-semantic-schema-runtime-dashboard.md) «`/node/*` hard cut — **Todo**» vs `:7`/`:43`.
15. Bullrun §«Актуальная точка» still MVP ES-03/M2-24 — [`bullrun-launch-index.md:17–20`](../../../../../bullrun-launch-index.md) (G2 WAIVED — **do not rewrite**).
16. SSR-15 already queued — [`STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md) 🟡 Todo (G3 WAIVED — **do not** invent duplicate).
17. Pointer stays pkg-000069 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
18. Product Story Done (AC/DoD, G13) = **yes**. Empty OPEN gap-list = **no** until this task + P7 (G2/G3 WAIVED kept).

## Gap / Проблема
Persistent SSOT (не `docs/analysis/**`): epic Problem Statement still lumps SSR-13 in Todo; backlog+pipeline §Verified still present-tense `/tallinn/` + `handle_tallinn_*`; wave dashboard queue `:84` still Todo after pkg-000069 G13 Done.

## Acceptance / DoD
- [x] Epic Problem Statement `:16`: As-of-Done SSR-13 (hard cut `/node/*`; handlers `handle_issues_list` / `_get` / `_create`; spa three repos + spa-16/51; G13 PASS 2026-08-29T18:55:15Z) vs remaining backlog (**SSR-11 + 14…15 Todo** — drop «13» from the Todo-lump)
- [x] Backlog + pipeline SSR-13 §Verified: As-of-Done vs Historical (`/node/*` + renamed handlers **есть**; Historical = `/tallinn/` + `handle_tallinn_*` + spa-16 Keep)
- [x] Wave dashboard queue (`gateway-semantic-schema-runtime-dashboard.md:84`): «`/node/*` hard cut — **Done**» to match Remaining `:43` / Last change `:7`
- [x] Status backlog+pipeline stays 🔵 Done; do not reopen product AC T01–T06
- [x] Epic Scope `:30` / Stories `:89` / DoD `:75` / Meta `:4` Done **не** revert
- [x] INDEX header `:14` / Progress `:110` / row 86 already Done-lump — **keep**
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] Нет invented `EPIC-M2-*` rows; нет duplicate SSR-15 (G3 `follow_up=none`)
- [x] No `src/` / `ClusterLens` / alias restore / identity edits
- [x] No pytest this wave (docs-only); do not HALT on red `test_req24_*` (G3 WAIVED)
- [x] `gateway-mvp-dashboard.md` **не** править; pie T-wave **не** трогать
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-13-t07.md` signed (Date post P6 live `--verify` + `--print-utc-now` only)

## Where to change
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (Problem Statement `:16` only; Meta/Scope/Stories/DoD stay Done)
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md` (§Verified As-of-Done vs Historical)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-13-abstract-node-public-api/STORY-GW-SSR-13-abstract-node-public-api.md` (same §Verified)
- `doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md` (queue `:84` only; Status OK)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- G3 gateway pytest `/tallinn/` (WAIVED reason=out-of-DoD; SSR-15 already queued)
- Runtime / alias restore / `ClusterLens` / invent HTTP / identity
- `gateway-mvp-dashboard.md`; pie T-wave
- New pkg; `gateway-active-package.current.yaml` stays pkg-000069
- SSR-06/07/11/12/14/15 execute; invent SSR-15 duplicate; reopen 01–05/08–10
- T-wave G3 / `audit-gw-ssr-0[1-5]*` rewrite
- INDEX/runbook §8 + fence hard bans:
  - **Hard cut `/tallinn/*` — NO alias.** Do not restore city prefix.
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / IDX/QRY.
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/11/12/14/15. Не reopen 01–05/08–10.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story** (SSR-11).
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'SSR-11 \+ 13…15 Todo|As-of-Done \(SSR-13|handle_tallinn_|Keep `GET /tallinn/issues`|hard cut — \*\*Done\*\*|hard cut — \*\*Todo\*\*' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-13-abstract-node-public-api/STORY-GW-SSR-13-abstract-node-public-api.md \
  doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md
# G2: heading block 17–20 must still be EPIC-M2-24 / ES-03 (do not rewrite)
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
