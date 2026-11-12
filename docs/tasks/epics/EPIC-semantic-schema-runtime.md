# EPIC-semantic-schema-runtime: Schema Runtime T-wave (gateway)

## Epic Meta
- Status: 🟡 In Progress (SSR-01…05 🔵 Done; T-wave 5/5. SSR-08…15 + SSR-16…18 🔵 Done; SSR-19–21 🔵 Done; SSR-22–25 🔵 Done; SSR-26 🔵 Done pkg-000083; SSR-12 Draft experimental; SSR-06/07 Draft)
- Priority: Medium
- Owner: TBD
- Target: T-wave (REQ3-WAVE-001 / 51 §2) + post-T-wave (D-SSR-7) + node-schema (D-SSR-8) + cluster-knobs (D-SSR-9) + geo-detail (D-SSR-10) + taxonomy-pack (SSR-26…)
- **Materialized:** 2026-08-28T13:11:39Z (P1.3 `input_mode=backlog_story` STORY-GW-SSR-01)
- **Git:** `semantic-schema-runtime` only — [T-wave](../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) (01–05 Done) · [пост-T-wave](../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) (08–15 Done) · [node-schema](../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) (16–18 Done) · [cluster-knobs](../backlog-stories/semantic-schema-runtime/orchestrator-cluster-knobs-runbook.md) (19–21) · [geo-detail](../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md) (с 22)
- **Not:** `EPIC-M2-*` (INDEX: эпик-дом не invent M2)

## Business Goal
Добавление node-specific semantic model = публикация **schema pack** + in-process `SchemaRuntime`, а не правка `StoryRecord` / intake parser / колонок `stories` / `ClusterLens` на каждое поле. T-wave (REQ3-WAVE-001 / 51 §2) закрывается без generic filter HTTP и без processor delivery.

## Problem Statement
**As-of-Done (SSR-15 pkg-000072):** pytest public URLs `/node/…`; rename `test_req24_issues_read_api.py`; scenarios civic / pack / Pulse≠issues / 404 `/tallinn/issues` + T-dual include (`tests/test_gw_ssr_15_scenarios.py`); `@app.get("/tallinn"` empty in tests; sole leftover `client.get("/tallinn/issues")` = T05 404. G15: T07 isolation **exit 0** 2026-08-29T19:57:04Z — **745 passed**, 12 skipped, 10 deselected; identity-service not rewritten (D-SSR-3). G15 PASS (P3 claim 19:47:15Z; suite green T07). **As-of-Done (SSR-11 pkg-000070):** pack `card_fields` allowlist → named `schema_card` sidecar on `GET /node/issues` (`dto.py` `to_public_dict`; `card_fields.py`; `issue_create.py` `_to_public_payload`); absent key = civic form; `forbidden`/`node_private` filtered; `rg structured_payload` in `dto.py` empty; `SchemaRuntime.project` stub stays. G11 PASS 2026-08-29T19:13:51Z. **As-of-Done (SSR-13 pkg-000069):** hard cut `/node/*` — `PUBLIC_ROUTES` `/node/issues`, `/node/network-pulse`, `/node/emerging-signals` (`asgi_app.py:65–67`); GET/POST `:462`/`:518`; handlers `handle_issues_list` / `handle_issue_get` / `handle_issue_create` (`handlers.py:385,433,462`); spa three repos + spa-16/51 `GET /node/issues`; no alias; `/tallinn/` empty in `src/core/api`. G13 PASS 2026-08-29T18:55:15Z. **As-of-Done (SSR-10 pkg-000068):** Path B dual opt-in — pack key `dual_civic_lenses` (`SchemaContext` default False); bound story always pack exact; civic memberships only if flag True (`_process_bound_story` / `_process_dual_civic_membership`); default exact-only (`legal_process` / `tallinn_civic` без ключа); `ClusterLens` still 10; no new HTTP. G10 PASS 2026-08-29T18:31:19Z. **As-of-Done (SSR-09 pkg-000067):** G9 artifacts on disk — migration `20260828_1400_*` six nullable binding cols = `_STORIES_BINDING_COLUMNS`; omit-probe / `required_columns_ready` without binding names; `schema-packs/` + resolver default; no new HTTP; Dockerfile not invented. Live hosted apply / restart / image = operator/deploy, not overnight proof. Gate PASS 2026-08-29T18:14:04Z. **As-of-Done (SSR-08 pkg-000066):** civic-as-pack `tallinn_civic/v1` (pack data; 10 `exact_lenses` as civic lens *values*, not new `ClusterLens` members); pack readiness knobs 35/3/`false`; civic `require_actionable_canonical_type=True` default/factory unchanged; `ClusterLens` still 10; G8 PASS 2026-08-29T17:52:54Z. **As-of-Done (SSR-05 pkg-000065):** pack exact-lens promote under pack `ReadinessPolicy` (legal_process 40/3/False on that call); `CLUSTERED` after successful pack promote; civic factory unchanged; no QRY HTTP; `to_public_dict` without `structured_payload`. T-wave 5/5. **As-of-Done (SSR-14 pkg-000071):** docs inventory `/tallinn/issues|network-pulse|emerging-signals` → `/node/…` as current contract (runtime-docs + REQ 49/50 + spa-15; openapi/51/spa-16 N/A already `/node`); G14 rg empty; T-wave G3 `:271` historical kept; `settlement:tallinn` live. G14 PASS 2026-08-29T19:30:07Z. **SSR-12** Draft experimental (pair matching). SSR-06/07 remain Draft after 16–18. **As-of-Done (SSR-18 pkg-000075):** pack/dual iff persist == `NODE_SCHEMA_*`; bound mismatch skip+log `cluster.skipped_schema_mismatch` (not civic); unbound READY_FOR_PROFILE civic as-is; dual from active pack.json (`dual_civic_lenses_for_ref`); `ClusterLens` still 10; no `GET /schema-active`. G18 PASS 2026-08-30T15:06:33Z — **767 passed**, 18 skipped, 10 deselected. **As-of-Done (SSR-17 pkg-000074):** stash+submit require `schema_binding` == `NODE_SCHEMA_*`; absent/`{}`/null/mismatch → `IntakeValidationError` 4xx; match → `resolve`/`validate` active pack (`services.py:249–271`); G17 22 passed; civic HTTP adapted; gate PASS 2026-08-30T14:45:34Z. **As-of-Done (SSR-16 pkg-000073):** `NODE_SCHEMA_ID`/`NODE_SCHEMA_VERSION` required in AppConfig (`schema.py:63–64`); boot `resolve_pack`; lifespan logs pair (`asgi_app.py:121–128`); G16 8 passed; gate PASS 2026-08-30T14:24:58Z. **As-of-Done (SSR-19 pkg-000076):** `node_clustering.civic` required parse → `SchemaContext.node_clustering` (`resolver.py` `_parse_civic_clustering`); three packs from EnvSpec defaults (tallinn `geo_scope=settlement:tallinn`); factory still AppConfig `CLUSTER_*`; `ClusterLens` still 10; no `GET /schema-active`. G19 PASS 2026-08-30T19:21:58Z — **5 passed**. **As-of-Done (SSR-20 pkg-000077):** civic engine/gate/min_size/geo_scope from active pack `node_clustering.civic`; semantic `CLUSTER_*` removed from AppConfig; `CLUSTER_CRON_*` stay; missing civic → ConfigError; ClusterLens=10. G20 PASS 2026-08-30T19:40:38Z — **776 passed**, 18 skipped, 10 deselected. **As-of-Done (SSR-21 pkg-000078):** мануал два контура (`exact_lenses` vs `node_clustering.civic`); 05-env semantic CLUSTER_* = **Не текущий SSOT** / pack; `CLUSTER_CRON_*` stay; server-env не требует semantic CLUSTER_*. G21 PASS 2026-08-30T19:53:57Z. **As-of-Done (SSR-23 pkg-000080):** envelope `geo_detail` + pack `geo_intake` (three packs `optional`); merge with `location_query`; ClusterLens=10; no SQL (→24). G23 PASS 2026-08-30T20:40:50Z — **12 passed**. **As-of-Done (SSR-22 pkg-000079):** scope + `geo_service is None` → `IntakeValidationError("geo unavailable")` (`handlers.py:258–260`); no silent skip; ClusterLens=10. G22 PASS 2026-08-30T20:07:21Z. **Next (D-SSR-9):** closed (19–21 Done). cron остаётся env. **As-of-Done (SSR-24 pkg-000081):** `StoryGeoSnapshot` street/house/house_range/houses/address_line persist sqlite+supabase; omit-probe; not in `required_columns_ready`; `mirror_to_payload` dual-write; migration `20260830_2100_gw_ssr_24_stories_geo_detail.sql` + `000_full_init`; ClusterLens=10. G24 PASS 2026-08-30T21:00:56Z — **801 passed**, 18 skipped, 10 deselected. **Next (D-SSR-10):** SSR-22–24 Done; SSR-25 Todo — clustering/docs. **Next (D-SSR-8):** node-schema 16–18 closed. **As-of-Done (SSR-04 pkg-000064):** pack exact membership via `SchemaPackClusterEngine`; civic `ClusterLens` still 10. **As-of-Done (SSR-03 pkg-000063):** optional `schema_binding` sidecar on v2 intake/stash; `LocalSchemaRuntime.validate` before `save_story`; persist map + server `payload_hash`. Civic absent/empty stays LegacyM2.

**Historical (pre-P3):** не было `src/core/schema/`, `schema-packs/`, `jsonschema` в deps.

## Scope
### In Scope
- STORY-GW-SSR-01: SchemaRuntime + SCHEMA-005 pack load — **Done** pkg-000061 T00–T07 gate PASS 2026-08-28T13:18:56Z
- STORY-GW-SSR-02: structured_payload persist — **Done** pkg-000062 T00–T08 gate PASS 2026-08-28T13:47:57Z
- STORY-GW-SSR-03: optional `schema_binding` v2 wire — **Done** pkg-000063 T01–T08 gate PASS 2026-08-28T14:13:05Z
- STORY-GW-SSR-04: schema-pack exact lens — **Done** pkg-000064 T01–T06 gate PASS 2026-08-28T14:36:12Z
- Soft (backlog): SSR-05 promotion + T-wave close — **Done** pkg-000065 T01–T07 gate PASS 2026-08-28T15:00:08Z
- Soft (backlog): SSR-08 Tallinn civic as schema pack — **Done** pkg-000066 T00–T06 gate PASS 2026-08-29T17:52:54Z
- Soft (backlog): SSR-09 hosted apply + packs — **Done** pkg-000067 T01–T04 gate PASS 2026-08-29T18:14:04Z (G9 artifacts; live apply = operator)
- Soft (backlog): SSR-10 taxonomy + exact dual — **Done** pkg-000068 T00–T04 gate PASS 2026-08-29T18:31:19Z
- Soft (backlog): SSR-13 abstract `/node/*` public API — **Done** pkg-000069 T01–T06 gate PASS 2026-08-29T18:55:15Z
- Soft (backlog): SSR-11 pack-declared Issue projection — **Done** pkg-000070 T00–T04 gate PASS 2026-08-29T19:13:51Z
- Soft (backlog): SSR-14 docs abstract node paradigm — **Done** pkg-000071 T01–T02 gate PASS 2026-08-29T19:30:07Z
- Soft (backlog): SSR-15 tests `/node` + scenarios — **Done** pkg-000072 T01–T06 + T-dual gate PASS 2026-08-29T19:47:15Z
- Soft (backlog): SSR-16 node active schema config — **Done** pkg-000073 T01–T06 G16 PASS 2026-08-30T14:24:58Z (D-SSR-8; env + boot)
- Soft (backlog): SSR-17 intake active schema gate — **Done** pkg-000074 T01–T05 G17 PASS 2026-08-30T14:45:34Z (нет/mismatch binding → 4xx)
- Soft (backlog): SSR-18 cluster active schema — **Done** pkg-000075 T01–T05 G18 PASS 2026-08-30T15:06:33Z (pack только активный; мануал)
- Soft (backlog): SSR-19 node clustering pack contract — **Done** pkg-000076 T00–T05 G19 PASS 2026-08-30T19:21:58Z (D-SSR-9; `node_clustering.civic` loader)
- Soft (backlog): SSR-20 node clustering runtime wire — **Done** pkg-000077 T01–T06 G20 PASS 2026-08-30T19:40:38Z (factory/handlers из pack; семантические CLUSTER_* убраны)
- Soft (backlog): SSR-21 node clustering docs — **Done** pkg-000078 T01–T04 G21 PASS 2026-08-30T19:53:57Z (два контура; 05-env)
- Soft (backlog): SSR-22 civic geo-gate hardening — **Done** pkg-000079 T00–T04 G22 PASS 2026-08-30T20:07:21Z (D-SSR-10; T00=intake 4xx)
- Soft (backlog): SSR-23 geo_detail wire + geo_intake — **Done** pkg-000080 T00–T05 G23 PASS 2026-08-30T20:40:50Z
- Soft (backlog): SSR-24 geo detail persist — **Done** pkg-000081 T01–T07 G24 PASS 2026-08-30T21:00:56Z (snapshot depth + SQL + mirror)
- Soft (backlog): SSR-25 geo clustering + docs — **Done** pkg-000082 T01–T05 G25 PASS 2026-08-30T21:27:05Z (civic/pack + мануал; 811 passed)
- Soft (backlog): SSR-26 taxonomy.json pack contract + loader — **Done** pkg-000083 T00–T05 G26 PASS 2026-09-01T13:00:37Z (no tallinn seed; ClusterLens=10)
- Soft (backlog): SSR-28 tallinn taxonomy.json seed — **Done** pkg-000085 T01–T06 G28 PASS 2026-09-01T13:35:45Z (182 keys from GPT SSOT; ClusterLens=10)
- Soft (backlog): SSR-29 taxonomy docs + operator copy-paste seam — **Done** pkg-000086 T01–T06 G29 PASS 2026-09-01T13:49:03Z (docs-only)
- Soft (backlog): SSR-30 tallinn card_fields / SPA overlay readiness — **Done** pkg-000087 T00–T05 G30 PASS 2026-09-02T14:00:46Z (Declare MVP 3 paths; SSR-11 unchanged)
- Soft (backlog): SSR-31 Contour2 node-specific taxonomy axes — **Done** pkg-000088 T01–T05 G31 PASS 2026-09-04T12:55:28Z (D-SSR-11 drop lockstep; keep structural)
- Soft (backlog): SSR-32 Contour1 wire taxonomy axes — **Done** pkg-000089 T01–T04 G32 PASS 2026-09-04T13:13:31Z (D-SSR-11 open `normalize_axis`; civic skip)
- Soft (backlog): SSR-33 node-specific taxonomy docs setup tests hygiene — **Done** pkg-000090 T01–T05 G33 PASS 2026-09-04T13:28:42Z · P6 T06 G1 CLOSED 2026-09-04T13:34:49Z (D-SSR-11 docs-only; GPT-SSR-15 handoff note)
- Soft (backlog): SSR-34 uus active schema-packs volume ops — **Done** pkg-000091 T01–T06 G34 PASS 2026-09-07T08:32:02Z · P6 T07 G1 CLOSED 2026-09-07T08:38:47Z (D-SSR-12 docs/env/gitignore; SCHEMA_ROOT_URL → SSR-35)
- Soft (backlog): SSR-35 SCHEMA_ROOT_URL + SCHEMA_PACK_REFRESH — **Done** pkg-000092 T01–T07 G35 PASS 2026-09-07T08:54:22Z · P6 T08 G1 CLOSED 2026-09-07T08:58:54Z (federation consume; URL ≠ Volume mount)

### Out of Scope
- SSR-12 complementary matching — **Draft experimental** (не T-wave, не IDX)
- SSR-06 / SSR-07 (Draft post-T-wave refine, **после** 22–25) — not T-wave DoD
- GPT UI / spa-app UI overlay (siblings REQ-45 / 16 overlay later). **Исключение D-SSR-7:** URL трёх Gateway*Repository + spa-16/15 path strings — in scope SSR-13/14.
- Удаление `ClusterLens` / civic engine; публичный `GET /schema-active`; перенос `CLUSTER_CRON_*` в pack; dual-source env+pack; глобальный require-geo без pack `geo_intake`
- `EPIC-M2-*` invent; MVP `gateway-mvp-dashboard.md`; bullrun §«Актуальная точка»
- `doge-identity-service`; invent HTTP filter; WASM / federation

## Stakeholders
- Product Owner
- Backend (gateway)

## Dependencies
- Parent REQ — [`51-semantic-schema-runtime.md`](../../requirements/51-semantic-schema-runtime.md)
- Parent product — [`REQ3-Semantic-Schema-Runtime-and-Node-Specific-Data-Processing.md`](../../../docs/requirements%20backlog/REQ3-Semantic-Schema-Runtime-and-Node-Specific-Data-Processing.md)
- Package INDEX — [`backlog-stories/semantic-schema-runtime/INDEX.md`](../backlog-stories/semantic-schema-runtime/INDEX.md)

## Success Metrics
- GW-SSR-01 story gate PASS: packs load; AC-004; SEC-001; `ClusterLens` unchanged — **met** 2026-08-28T13:18:56Z
- GW-SSR-02 story gate PASS: AC-002/003; DATA-001/004; civic envelope persist — **met** 2026-08-28T13:47:57Z
- GW-SSR-03 story gate PASS: AC-015/COMPAT-001; FLOW-003; civic absent — **met** 2026-08-28T14:13:05Z
- GW-SSR-04 story gate PASS: AC-007/008; CL-004; SEC-004; ClusterLens 10 — **met** 2026-08-28T14:36:12Z

## Epic Acceptance Criteria
- GW-SSR-01 story gate PASS (pkg-000061) — **met** 2026-08-28T13:18:56Z
- GW-SSR-02 story gate PASS (pkg-000062) — **met** 2026-08-28T13:47:57Z
- GW-SSR-03 story gate PASS (pkg-000063) — **met** 2026-08-28T14:13:05Z
- GW-SSR-04 story gate PASS (pkg-000064) — **met** 2026-08-28T14:36:12Z

## Risks and Mitigation
- **Invent EPIC-M2 / mix MVP:** named from package `semantic-schema-runtime`; do not rewrite bullrun §«Актуальная точка»
- **Civic lens contamination:** INDEX/runbook §4 bans in every task README

## Definition of Done
- SSR-01 product Done (pkg-000061 T00–T07); gate PASS 2026-08-28T13:18:56Z
- SSR-02 product Done (pkg-000062 T00–T08); gate PASS 2026-08-28T13:47:57Z
- SSR-03 product Done (pkg-000063 T01–T08); gate PASS 2026-08-28T14:13:05Z
- SSR-05 product Done (pkg-000065 T01–T07); gate PASS 2026-08-28T15:00:08Z
- SSR-08 product Done (pkg-000066 T00–T06); gate PASS 2026-08-29T17:52:54Z
- SSR-09 product Done (pkg-000067 T01–T04); gate PASS 2026-08-29T18:14:04Z (G9 artifacts; live apply = operator)
- SSR-10 product Done (pkg-000068 T00–T04); gate PASS 2026-08-29T18:31:19Z (G10 Path B dual opt-in; ClusterLens=10)
- SSR-13 product Done (pkg-000069 T01–T06); gate PASS 2026-08-29T18:55:15Z (G13 hard cut `/node/*`; no alias)
- SSR-11 product Done (pkg-000070 T00–T04); gate PASS 2026-08-29T19:13:51Z (named `schema_card` / no dump / `GET /node/issues`)
- SSR-14 docs Done (pkg-000071 T01–T02); gate PASS 2026-08-29T19:30:07Z (inventory `/tallinn/`→`/node/` current contract)
- SSR-15 tests Done (pkg-000072 T01–T06 + T-dual + T07 isolation); gate PASS 2026-08-29T19:47:15Z; G15 suite exit 0 2026-08-29T19:57:04Z (745 passed)
- SSR-16 node-schema config — **met** 2026-08-30T14:24:58Z (pkg-000073 G16)
- SSR-17 intake gate — **met** 2026-08-30T14:45:34Z (pkg-000074 G17)
- SSR-18 node-schema cluster — **met** 2026-08-30T15:06:33Z (pkg-000075 G18)
- SSR-19 cluster-knobs pack contract — **met** 2026-08-30T19:21:58Z (pkg-000076 G19)
- SSR-20 cluster-knobs runtime wire — **met** 2026-08-30T19:40:38Z (pkg-000077 G20)
- SSR-21 cluster-knobs docs — **met** 2026-08-30T19:53:57Z (pkg-000078 G21)
- SSR-22 civic geo-gate — **met** 2026-08-30T20:07:21Z (pkg-000079 G22; T00=intake 4xx)
- SSR-23 geo_detail wire — **met** 2026-08-30T20:40:50Z (pkg-000080 G23)
- SSR-24 geo-detail persist — **met** 2026-08-30T21:00:56Z (pkg-000081 G24)
- SSR-26 taxonomy pack contract/loader — **met** 2026-09-01T13:00:37Z (pkg-000083 G26)

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-GW-SSR-01 | [SchemaRuntime + pack load](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-01-schema-runtime-pack-load/STORY-GW-SSR-01-schema-runtime-pack-load.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md) | 🔵 Done (Awaiting Commits) pkg-000061 gate PASS 2026-08-28T13:18:56Z |
| STORY-GW-SSR-02 | [structured_payload persist](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/STORY-GW-SSR-02-structured-payload-persist.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md) | 🔵 Done (Awaiting Commits) pkg-000062 gate PASS 2026-08-28T13:47:57Z |
| STORY-GW-SSR-03 | [optional v2 semantic wire](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-03-optional-v2-semantic-wire/STORY-GW-SSR-03-optional-v2-semantic-wire.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md) | 🔵 Done (Awaiting Commits) pkg-000063 gate PASS 2026-08-28T14:13:05Z |
| STORY-GW-SSR-04 | [schema-pack exact lens](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-04-schema-driven-cluster-lens/STORY-GW-SSR-04-schema-driven-cluster-lens.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md) | 🔵 Done (Awaiting Commits) pkg-000064 gate PASS 2026-08-28T14:36:12Z |
| STORY-GW-SSR-05 | [pack promotion + T-wave close](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md) | 🔵 Done (Awaiting Commits) pkg-000065 gate PASS 2026-08-28T15:00:08Z |
| STORY-GW-SSR-08 | [Tallinn civic schema pack](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-08-tallinn-civic-schema-pack/STORY-GW-SSR-08-tallinn-civic-schema-pack.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md) | 🔵 Done (Awaiting Commits) pkg-000066 gate PASS 2026-08-29T17:52:54Z |
| STORY-GW-SSR-09 | [hosted apply + pack image](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-09-hosted-apply-and-pack-image/STORY-GW-SSR-09-hosted-apply-and-pack-image.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-09-hosted-apply-and-pack-image.md) | 🔵 Done (Awaiting Commits) pkg-000067 gate PASS 2026-08-29T18:14:04Z (G9: hosted apply = operator/deploy, not overnight proof) |
| STORY-GW-SSR-10 | [taxonomy + exact dual](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md) | 🔵 Done (Awaiting Commits) pkg-000068 T00–T04 gate PASS 2026-08-29T18:31:19Z (Path B dual opt-in; G10 ClusterLens=10) |
| STORY-GW-SSR-13 | [pipeline abstract `/node/*` API](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-13-abstract-node-public-api/STORY-GW-SSR-13-abstract-node-public-api.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md) | 🔵 Done (Awaiting Commits) pkg-000069 T01–T06 gate PASS 2026-08-29T18:55:15Z (hard cut `/node/*`; no alias) |
| STORY-GW-SSR-11 | [pipeline pack-declared Issue projection](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-11-pack-declared-issue-projection/STORY-GW-SSR-11-pack-declared-issue-projection.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-11-pack-declared-issue-projection.md) | 🔵 Done (Awaiting Commits) pkg-000070 T00–T04 gate PASS 2026-08-29T19:13:51Z |
| STORY-GW-SSR-14 | [pipeline docs abstract node](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-14-docs-abstract-node-paradigm/STORY-GW-SSR-14-docs-abstract-node-paradigm.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-14-docs-abstract-node-paradigm.md) | 🔵 Done (Awaiting Commits) pkg-000071 T01–T02 gate PASS 2026-08-29T19:30:07Z |
| STORY-GW-SSR-15 | [pipeline tests `/node` + scenarios](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-15-tests-abstract-node-and-scenarios/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md) | 🔵 Done (Awaiting Commits) pkg-000072 T01–T07 + T-dual · G15 exit 0 2026-08-29T19:57:04Z (745 passed) |
| STORY-GW-SSR-16 | [pipeline node active schema config](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-16-node-active-schema-config/STORY-GW-SSR-16-node-active-schema-config.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md) | 🔵 Done (Awaiting Commits) pkg-000073 T01–T06 G16 PASS 2026-08-30T14:24:58Z |
| STORY-GW-SSR-17 | [pipeline intake active schema gate](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-17-intake-active-schema-gate/STORY-GW-SSR-17-intake-active-schema-gate.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md) | 🔵 Done (Awaiting Commits) pkg-000074 T01–T05 G17 PASS 2026-08-30T14:45:34Z |
| STORY-GW-SSR-18 | [pipeline cluster active schema](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-18-cluster-active-schema/STORY-GW-SSR-18-cluster-active-schema.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md) | 🔵 Done (Awaiting Commits) pkg-000075 T01–T05 G18 PASS 2026-08-30T15:06:33Z |
| STORY-GW-SSR-19 | [pipeline node clustering pack contract](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-19-node-clustering-pack-contract/STORY-GW-SSR-19-node-clustering-pack-contract.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md) | 🔵 Done (Awaiting Commits) pkg-000076 T00–T05 G19 PASS 2026-08-30T19:21:58Z |
| STORY-GW-SSR-20 | [pipeline node clustering runtime wire](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-20-node-clustering-runtime-wire/STORY-GW-SSR-20-node-clustering-runtime-wire.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md) | 🔵 Done (Awaiting Commits) pkg-000077 T01–T06 G20 PASS 2026-08-30T19:40:38Z |
| STORY-GW-SSR-21 | [pipeline node clustering docs](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-21-node-clustering-docs/STORY-GW-SSR-21-node-clustering-docs.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md) | 🔵 Done (Awaiting Commits) pkg-000078 T01–T04 G21 PASS 2026-08-30T19:53:57Z |
| STORY-GW-SSR-22 | [pipeline civic geo-gate hardening](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-22-civic-geo-gate-hardening/STORY-GW-SSR-22-civic-geo-gate-hardening.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md) | 🔵 Done (Awaiting Commits) pkg-000079 T00–T04 G22 PASS 2026-08-30T20:07:21Z |
| STORY-GW-SSR-23 | [pipeline geo_detail wire + geo_intake](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-23-geo-detail-intake-contract/STORY-GW-SSR-23-geo-detail-intake-contract.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md) | 🔵 Done (Awaiting Commits) pkg-000080 T00–T05 G23 PASS 2026-08-30T20:40:50Z |
| STORY-GW-SSR-24 | [pipeline geo detail persist](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-24-geo-detail-persist/STORY-GW-SSR-24-geo-detail-persist.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md) | 🔵 Done (Awaiting Commits) pkg-000081 T01–T07 G24 PASS 2026-08-30T21:00:56Z |
| STORY-GW-SSR-25 | [pipeline geo clustering + docs](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-25-geo-detail-clustering-docs/STORY-GW-SSR-25-geo-detail-clustering-docs.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-25-geo-detail-clustering-docs.md) | 🔵 Done (Awaiting Commits) pkg-000082 T01–T05 G25 PASS 2026-08-30T21:27:05Z |
| STORY-GW-SSR-26 | [pipeline taxonomy.json pack contract + loader](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-26-taxonomy-json-pack-contract/STORY-GW-SSR-26-taxonomy-json-pack-contract.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md) | 🔵 Done (Awaiting Commits) pkg-000083 T00–T05 G26 PASS 2026-09-01T13:00:37Z |
| STORY-GW-SSR-27 | [pipeline geo precision + instance territory](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-27-geo-precision-instance-territory/STORY-GW-SSR-27-geo-precision-instance-territory.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md) | 🔵 Done (Awaiting Commits) pkg-000084 T00–T07 G27 PASS 2026-09-01T13:21:04Z |
| STORY-GW-SSR-28 | [pipeline tallinn taxonomy.json seed](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md) | 🔵 Done (Awaiting Commits) pkg-000085 T01–T06 G28 PASS 2026-09-01T13:35:45Z |
| STORY-GW-SSR-29 | [pipeline taxonomy docs + operator copy-paste seam](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md) | 🔵 Done (Awaiting Commits) pkg-000086 T01–T06 G29 PASS 2026-09-01T13:49:03Z |
| STORY-GW-SSR-30 | [pipeline tallinn card_fields / SPA overlay readiness](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md) | 🔵 Done (Awaiting Commits) pkg-000087 T00–T05 G30 PASS 2026-09-02T14:00:46Z |
| STORY-GW-SSR-31 | [pipeline Contour2 node-specific taxonomy axes](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md) | 🔵 Done (Awaiting Commits) pkg-000088 T01–T05 G31 PASS 2026-09-04T12:55:28Z |
| STORY-GW-SSR-32 | [pipeline Contour1 wire taxonomy axes](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-32-node-specific-contour1-wire-axes/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md) | 🔵 Done (Awaiting Commits) pkg-000089 T01–T04 G32 PASS 2026-09-04T13:13:31Z |
| STORY-GW-SSR-33 | [pipeline node-specific taxonomy docs setup tests hygiene](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md) | 🔵 Done (Awaiting Commits) pkg-000090 T01–T05 G33 PASS 2026-09-04T13:28:42Z · P6 T06 G1 CLOSED |
| STORY-GW-SSR-34 | [pipeline uus active schema-packs volume ops](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md) | 🔵 Done (Awaiting Commits) pkg-000091 T01–T06 G34 PASS 2026-09-07T08:32:02Z · P6 T07 G1 CLOSED |
| STORY-GW-SSR-35 | [pipeline SCHEMA_ROOT_URL + SCHEMA_PACK_REFRESH](./EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-35-schema-root-url-pack-refresh/STORY-GW-SSR-35-schema-root-url-pack-refresh.md) → [backlog](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-35-schema-root-url-pack-refresh.md) | 🔵 Done (Awaiting Commits) pkg-000092 T01–T07 G35 PASS 2026-09-07T08:54:22Z · P6 T08 G1 CLOSED |
| STORY-GW-SSR-12 | [backlog complementary pair matching](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-12-complementary-pair-matching.md) | 📝 Draft (experimental) |
| STORY-GW-SSR-06 | [backlog analytical index later](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-06-analytical-index-later.md) | 📝 Draft (post-T-wave refine; after 22–25) |
| STORY-GW-SSR-07 | [backlog processor later](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-07-processor-delivery-later.md) | 📝 Draft (post-T-wave refine) |

## Decision Ref
- [`backlog-stories/semantic-schema-runtime/INDEX.md`](../backlog-stories/semantic-schema-runtime/INDEX.md) D-SSR-1…D-SSR-10
- [`STORY-GW-SSR-01-schema-runtime-pack-load.md`](../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md)
- REQ 51 §2 / §4.1–4.2; parent REQ3 RUNTIME-001…005, SCHEMA-005, SEC-001/002
- **Source (backlog):** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` + `$storyFile`
