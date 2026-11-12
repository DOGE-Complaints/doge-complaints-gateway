# task-gw-ssr-09-t05-audit-g1-epic-index-ssot

## Task: add — epic Stories/Problem Statement/DoD + INDEX header As-of-Done

## Meta
- **Story:** [STORY-GW-SSR-09](../STORY-GW-SSR-09-hosted-apply-and-pack-image.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000067 (parent product Done); wave `run_mode=gw_ssr_09_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-09
- **Depends on:** T01–T04 Done (product AC/DoD, G9)
- **Audit ref:** [`audit-gw-ssr-09-hosted-apply-and-pack-image-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-09-hosted-apply-and-pack-image-2026-08-29.md) **G1**
- **Scaffolded:** 2026-08-29T18:19:17Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-09_gap_20260829T181822Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-29T18:20:52Z

## Purpose
Закрыть G1 (MEDIUM): persistent SSOT drift — epic Stories `:84` still ⚪ Todo; Problem Statement `:16` still lumps «Backlog (SSR-09…11 + 13…15 Todo): hosted apply»; DoD `:67–72` lists SSR-08 без SSR-09; INDEX header `:14` still «SSR-09…15 Todo» vs row 84 **Done**. Split Problem Statement As-of-Done (SSR-09 G9 artifacts + omit-probe/`/ready`; live apply = operator) vs remaining backlog (SSR-10…11 + 13…15 Todo). Stories row 🔵 Done. DoD + INDEX Updated. Без runtime. Без rewrite §«Актуальная точка» (G2 WAIVED). **G9:** hosted apply = operator/deploy, not overnight proof.

## Code Facts
1. Audit G1 — [`audit-gw-ssr-09-hosted-apply-and-pack-image-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-09-hosted-apply-and-pack-image-2026-08-29.md) §3 / §5.
2. Package INDEX row 9 SSR-09 Done — [`INDEX.md:84`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) 🔵 Done (Awaiting Commits).
3. INDEX header still Todo-lump — [`INDEX.md:14`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) «SSR-09…15 Todo» vs row 84 Done.
4. Epic Scope SSR-09 Done — [`EPIC-semantic-schema-runtime.md:28`](../../../../EPIC-semantic-schema-runtime.md) Done pkg-000067 gate PASS 2026-08-29T18:14:04Z.
5. Epic Stories row SSR-09 still Todo — [`EPIC-semantic-schema-runtime.md:84`](../../../../EPIC-semantic-schema-runtime.md) ⚪ Todo pkg-000067.
6. Epic Problem Statement still Todo-lump — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md) «**Backlog (SSR-09…11 + 13…15 Todo):** hosted apply» vs Scope Done.
7. Epic DoD lists SSR-08, no SSR-09 — [`EPIC-semantic-schema-runtime.md:67–72`](../../../../EPIC-semantic-schema-runtime.md).
8. Bullrun §«Актуальная точка» still MVP ES-03/M2-24 — [`bullrun-launch-index.md:17–20`](../../../../../bullrun-launch-index.md) (G2 WAIVED — **do not rewrite**).
9. Bullrun SSR-09 rows already Done (below heading) — existing T01–T04.
10. Pointer stays pkg-000067 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
11. Product Story Done (AC/DoD, G9) = **yes**. Empty OPEN gap-list = **no** until this task + P7 (G2 WAIVED kept).

## Gap / Проблема
Persistent SSOT (не `docs/analysis/**`): epic Stories/Problem Statement/DoD и INDEX header still present-tense Todo for hosted apply after pkg-000067 G9 Done.

## Acceptance / DoD
- [x] Epic Stories `:84`: ⚪ Todo → 🔵 Done (Awaiting Commits) pkg-000067 gate PASS 2026-08-29T18:14:04Z; G9 note: hosted apply = operator/deploy, not overnight proof
- [x] Epic Problem Statement `:16`: As-of-Done (SSR-09 G9 artifacts + omit-probe/`/ready`; live apply = operator) vs remaining backlog (SSR-10…11 + 13…15 Todo)
- [x] Epic DoD `:67–72`: add SSR-09 product Done (pkg-000067 T01–T04); gate PASS 2026-08-29T18:14:04Z; do not claim live Railway apply
- [x] INDEX header `:14`: Updated + «SSR-08 + SSR-09 Done»; remaining Todo 10…15 (not «SSR-09…15 Todo»); row 84 stays Done
- [x] Epic Scope `:28` Done **не** revert
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] Нет invented `EPIC-M2-*` rows
- [x] No `src/` / `db_supabase.py` / `asgi_app.py` / Dockerfile / identity edits
- [x] No pytest this wave (docs-only)
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-09-t05.md` signed (Date post P6 live `--verify` + `--print-utc-now` only)

## Where to change
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (Stories `:84`, Problem Statement `:16`, DoD `:67–72`)
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` (header `:14` only; row 84 stays Done)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Live Railway apply / restart / image as overnight proof (G9)
- Runtime / omit-probe / `required_columns_ready` / invent Dockerfile / invent HTTP
- `gateway-mvp-dashboard.md`; pie T-wave
- New pkg; `gateway-active-package.current.yaml` stays pkg-000067
- SSR-06/07/10/12; reopen SSR-08; T-wave G3 / `audit-gw-ssr-0[1-5]*` rewrite
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/10/12. Не reopen SSR-08.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story**.
  - Не invent Dockerfile.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'STORY-GW-SSR-09|Backlog \(SSR-09|As-of-Done \(SSR-09' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md
rg -n 'SSR-09…15 Todo|SSR-08 \+ SSR-09 Done' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
# G2: heading block 17–20 must still be EPIC-M2-24 / ES-03 (do not rewrite)
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
