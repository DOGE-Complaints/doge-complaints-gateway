# REQ11 demo life sim — fixtures & replay (gateway) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/`  
**Тип:** backlog (постановки; P1.3/P3 — после активации pkg).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md)  
**Parent product:** [`REQ11-DOGEstonia-Uus-Veerenni-Demo-Life-Simulation.md`](../../../../../docs/requirements%20backlog/REQ11-DOGEstonia-Uus-Veerenni-Demo-Life-Simulation.md) §1–§4, §6.1, §7.1 D1–D3/D5–D6, §7.2 K1/K3/K4  
**Justification:** [`brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md`](../../../../../docs/analysis/brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md); [`status-simulation-story-data-assembly-2026-09-29.md`](../../../analysis/status-simulation-story-data-assembly-2026-09-29.md)  
**Dashboard:** [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) (operator lock: MVP board)  
**Naming:** `STORY-GW-REQ11-*`  
**Updated:** 2026-10-02T08:58:23Z · REQ11-11 P6 G2 CLOSED (As-of-Done SSOT); product Done pkg-000109; REQ11-12 backlog Todo; REQ11-07 removed  
**Active pkg:** [`pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml`](../../gateway-active-packages/pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml)  

**Epic:** [`EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay.md)  


---

## Контекст одной фразой

Gateway: JSON users+stories (scale/langs/2026 curve) + profiles (`local` from local-five + Uus Veerenni) + API replay + service-auth backdate + clustering wait — **real verified API accounts** for fixture users (secrets file; no SPA demo-resident login required for Pass).

---

## Operator locks (clarifying 2026-09-29)

| Theme | Decision |
|-------|----------|
| Dashboard | sync `gateway-mvp-dashboard.md` |
| Scale | **200** users; Gaussian mean **8.5**, σ **2.0**, clamp **[1, 20]**; langs **60% et / 30% ru / 10% en**; calendar **2026**; breakpoint **2026-09-30**; mass **~25%** pre / **~75%** post |
| Backdate | **B** — service-auth controlled backdate after stash→submit (not public intake invent; not SQL dump as Pass) |
| Auth multi-submitter | **Superseded 2026-09-29 (REQ11-05):** provision **200** real verified users (Supabase signup + Identity phone with **`SMS_PROVIDER=file`**); CSPRNG passwords; gitignored secrets file per generation; **1:1** fixture→Bearer. ~~pool M=20~~ deprecated for new Pass (file remains until wire). K1: no SPA resident login required for demo Pass. |
| Profile `local` | from [`local-five-serve-and-health.sh`](../../../../../scripts/shell/local-five-serve-and-health.sh): identity **8100**, gateway **8000**, threads **8001**, aibridge **8080**, spa **5173** (env refs; secrets not in git) |
| Package | **new** `req11-demo-life-sim-fixtures-and-replay/` (not reuse closed `demo-data-seeding`) |

---

## Stories

| Key | File | Status | Depends |
|-----|------|--------|---------|
| STORY-GW-REQ11-01 | [STORY-GW-REQ11-01-fixtures-users-stories-scale.md](./STORY-GW-REQ11-01-fixtures-users-stories-scale.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/STORY-GW-REQ11-01-fixtures-users-stories-scale.md) · [pkg-000100](../../gateway-active-packages/pkg-000100-20260929-gw-req11-01-fixtures-users-stories-scale.yaml) | 🔵 Done (Awaiting Commits) P3 2026-09-29T13:43:36Z · gate PASS | — |
| STORY-GW-REQ11-02 | [STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md](./STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md) · [pkg-000101](../../gateway-active-packages/pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml) | 🔵 Done (Awaiting Commits) P3 2026-09-29T14:00:57Z · gate PASS · T05 G1 CLOSED P6 2026-09-29T14:08:13Z | — |
| STORY-GW-REQ11-03 | [STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md](./STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md) · [pkg-000102](../../gateway-active-packages/pkg-000102-20260929-gw-req11-03-profiled-api-replay-multi-submitter.yaml) | 🔵 Done P3 2026-09-29T14:21:44Z · gate PASS · live pool 0/20 blocker (superseded by 05 for new Pass) | REQ11-01, REQ11-02 |
| STORY-GW-REQ11-04 | [STORY-GW-REQ11-04-backdate-and-clustering-handoff.md](./STORY-GW-REQ11-04-backdate-and-clustering-handoff.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md) · [pkg-000103](../../gateway-active-packages/pkg-000103-20260929-gw-req11-04-backdate-and-clustering-handoff.yaml) | 🔵 Done P3 2026-09-29T14:39:37Z · gate PASS · lock B `PATCH /ops/stories/{id}/created-at` | REQ11-03 |
| STORY-GW-REQ11-05 | [STORY-GW-REQ11-05-provision-fixture-users-identity.md](./STORY-GW-REQ11-05-provision-fixture-users-identity.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-05-provision-fixture-users-identity/STORY-GW-REQ11-05-provision-fixture-users-identity.md) · [pkg-000104](../../gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml) | 🔵 Done P3 2026-09-29T18:15:05Z · gate PASS* · live signup 429 · [`pkg-000104`](../../gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml) | REQ11-01; soft REQ11-02 |
| STORY-GW-REQ11-06 | [STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md](./STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md) · [pkg-000105](../../gateway-active-packages/pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml) | 🔵 Done P3 2026-09-30T07:56:35Z · gate PASS · wipe Present | soft REQ11-02/03 |
| STORY-GW-REQ11-08 | [STORY-GW-REQ11-08-operator-provision-pack-wave.md](./STORY-GW-REQ11-08-operator-provision-pack-wave.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-08-operator-provision-pack-wave/STORY-GW-REQ11-08-operator-provision-pack-wave.md) · [pkg-000106](../../gateway-active-packages/pkg-000106-20261001-gw-req11-08-operator-provision-pack-wave.yaml) | 🔵 Done · pack-wave provision · **07 removed — do not reuse** | soft REQ11-05; soft pack/`users.json` |
| STORY-GW-REQ11-09 | [STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md](./STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md) · [pkg-000107](../../gateway-active-packages/pkg-000107-20261001-gw-req11-09-operator-threads-seed-after-cluster.yaml) | 🔵 Done · threads seed after cluster | soft REQ11-06; soft cluster |
| STORY-GW-REQ11-10 | [STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md](./STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md) · [pkg-000108](../../gateway-active-packages/pkg-000108-20261001-gw-req11-10-operator-pack-replay-complaints-wave.yaml) | 🔵 Done · pack-wave replay жалоб | soft REQ11-03; soft 05/08 secrets |
| STORY-GW-REQ11-11 | [STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md](./STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md) · [pkg-000109](../../gateway-active-packages/pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml) | 🔵 Done P3 2026-10-02T08:53:45Z · P6 G2 CLOSED 2026-10-02T08:58:23Z · gate PASS · contract note Present · As-of-Done SSOT · **07 removed** | soft REQ11-01; scarcity analysis |
| STORY-GW-REQ11-12 | [STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md](./STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md) → [pipeline](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md) | ⚪ Todo (backlog) · rich generator + adapter · no LLM · name≠create | soft **REQ11-11**; soft REQ11-10 |

---

## Out of package

- Threads comment/reaction HTTP (sibling `04-…`)  
- Spa chrome / verify (sibling `20-…`)  
- SPA demo-resident login as Pass requirement (K1) — API accounts OK  
- Invent Identity `GET /dev/last-otp` (use `SMS_PROVIDER=file`)  
- REQ8; SQL dump as primary Pass (K4)  
- Inventing undocumented public field names before PA.2 proof  
- Content wipe stories/issues/threads — остаётся **STORY-GW-REQ11-06** (не Auth wipe в 08)  
- Pack-gen (бывший REQ11-07) — removed; successor richness = **REQ11-11/12** (не reuse 07)  
