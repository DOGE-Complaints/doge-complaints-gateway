# EPIC-req11-demo-life-sim-fixtures-and-replay: REQ11 demo life sim fixtures & replay (gateway)

## Epic Meta
- Status: 🟡 In Progress (REQ11-01…06,08–11 Done; REQ11-12 In Progress pkg-000110; REQ11-07 removed)
- Priority: High (REQ11 / REQ55)
- Type: backlog package epic (not EPIC-M2-*)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../requirements/55-req11-demo-life-sim-fixtures-and-replay.md)
- **Parent product:** REQ11 §3.1–3.2, §6.1 GW-11-01/02, §7.1 D2/D5/D6
- **Justification:** [`brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md`](../../../docs/analysis/brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md); [`status-simulation-story-data-assembly-2026-09-29.md`](../analysis/status-simulation-story-data-assembly-2026-09-29.md); scarcity [`analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md`](../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md)
- **Dashboard:** [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md) — operator lock MVP board
- **Git:** `dev` (no separate package branch)
- **Scaffolded:** 2026-09-29T13:22:23Z
- **Updated:** 2026-10-02T09:02:38Z (REQ11-12 P1 scaffold pkg-000110)

## Problem Statement

Gateway: JSON users+stories at locked scale/langs/2026 curve; named profiles; profiled API replay; service-auth backdate + clustering handoff; **provision 200 real verified API accounts** (secrets file) for 1:1 Bearer — without SPA resident login as Pass requirement (K1). Operator wipe of node content (stories+derivatives+threads) before life-sim load — no Identity DELETE. Operator pack-wave provision CLI (REQ11-08) with wave-state + RU manual — **Done**. Operator threads seed after cluster (REQ11-09) — **Done** pkg-000107 (live full seed leftover if issues empty). Operator pack-wave replay жалоб (REQ11-10) — **Done** pkg-000108 (live full leftover if Supabase Auth unreachable).

## Soft (backlog)

- Soft (backlog): REQ11-01 fixtures users+stories scale — **Done** pkg-000100
- Soft (backlog): REQ11-02 named profiles local/Uus Veerenni — **Done** pkg-000101
- Soft (backlog): REQ11-03 profiled API replay multi-submitter — **Done** pkg-000102 (P3 + audit T07); live pool superseded by 05
- Soft (backlog): REQ11-04 backdate + clustering handoff — **Done** pkg-000103
- Soft (backlog): REQ11-05 provision fixture users Identity + secrets — **Done** pkg-000104 (live signup 429 ops leftover)
- Soft (backlog): REQ11-06 wipe node content stories+derivatives+threads — **Done** pkg-000105
- Soft (backlog): REQ11-08 operator provision pack wave — **Done** pkg-000106
- Soft (backlog): REQ11-09 operator threads seed after cluster — **Done** pkg-000107
- Soft (backlog): REQ11-10 operator pack-wave replay жалоб — **Done** pkg-000108
- Soft (backlog): REQ11-11 life-sim stories fixture contract v2 — **Done** pkg-000109 (docs + mapping note)
- Soft (backlog): REQ11-12 rich stories generator + adapter — **In Progress** pkg-000110 (P1 scaffold; P3 implement)

## Stories

| Story | Pipeline / backlog | Status |
|-------|--------------------|--------|
| STORY-GW-REQ11-01 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/STORY-GW-REQ11-01-fixtures-users-stories-scale.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md) · [pkg-000100](../gateway-active-packages/pkg-000100-20260929-gw-req11-01-fixtures-users-stories-scale.yaml) | 🔵 Done pkg-000100 |
| STORY-GW-REQ11-02 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md) · [pkg-000101](../gateway-active-packages/pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml) | 🔵 Done pkg-000101 |
| STORY-GW-REQ11-03 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md) · [pkg-000102](../gateway-active-packages/pkg-000102-20260929-gw-req11-03-profiled-api-replay-multi-submitter.yaml) | 🔵 Done pkg-000102 |
| STORY-GW-REQ11-04 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md) · [pkg-000103](../gateway-active-packages/pkg-000103-20260929-gw-req11-04-backdate-and-clustering-handoff.yaml) | 🔵 Done pkg-000103 |
| STORY-GW-REQ11-05 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-05-provision-fixture-users-identity/STORY-GW-REQ11-05-provision-fixture-users-identity.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md) · [pkg-000104](../gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml) | 🔵 Done pkg-000104 |
| STORY-GW-REQ11-06 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md) · [pkg-000105](../gateway-active-packages/pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml) | 🔵 Done pkg-000105 |
| STORY-GW-REQ11-08 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-08-operator-provision-pack-wave/STORY-GW-REQ11-08-operator-provision-pack-wave.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md) · [pkg-000106](../gateway-active-packages/pkg-000106-20261001-gw-req11-08-operator-provision-pack-wave.yaml) | 🔵 Done pkg-000106 |
| STORY-GW-REQ11-09 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md) · [pkg-000107](../gateway-active-packages/pkg-000107-20261001-gw-req11-09-operator-threads-seed-after-cluster.yaml) | 🔵 Done pkg-000107 |
| STORY-GW-REQ11-10 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md) · [pkg-000108](../gateway-active-packages/pkg-000108-20261001-gw-req11-10-operator-pack-replay-complaints-wave.yaml) | 🔵 Done pkg-000108 |
| STORY-GW-REQ11-11 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md) · [pkg-000109](../gateway-active-packages/pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml) | 🔵 Done pkg-000109 |
| STORY-GW-REQ11-12 | [pipeline](./EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md) → [backlog](../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md) · [pkg-000110](../gateway-active-packages/pkg-000110-20261002-gw-req11-12-life-sim-stories-rich-generator-and-adapter.yaml) | 🟡 In Progress pkg-000110 |

## Decision Ref
- Backlog INDEX + `$storyFile` REQ11-12 · pkg-000110
- REQ 55 · REQ11 · brief + status-simulation justifications
- Operator locks: 200 users; Gaussian 8.5/σ2.0/[1,20]; langs 60/30/10; breakpoint 2026-09-30; ~25%/75%; backdate **B**; auth **200 provisioned + secrets** (supersedes pool M=20); wipe confirm `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1`; pack-wave `SMS_PROVIDER=file` + `@dogestonia.me`; threads seed fail-closed after cluster + reuse `closed_http_seed`; pack-wave replay fail-closed `LIFE_SIM_PACK_DIR` + wave per `fixture_story_id`; dashboard sync
