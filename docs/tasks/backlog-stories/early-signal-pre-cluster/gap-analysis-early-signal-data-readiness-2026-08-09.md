# Gap analysis — Early Signal / Pre-Cluster data readiness (gateway)

**Дата:** 2026-08-09 (inventory); **post-Done sync:** 2026-08-10 — L1 Public via ES-02 / REQ-49; **2026-08-11** — L2 Public via ES-03 / REQ-50 `GET /tallinn/emerging-signals` (audit T09)  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)  
**Task-deliverable:** [`TASK-GW-ES-01-early-signal-data-readiness-inventory.md`](./TASK-GW-ES-01-early-signal-data-readiness-inventory.md)  
**Parent REQ:** [`docs/requirements/48-early-signal-pre-cluster-data-readiness.md`](../../../requirements/48-early-signal-pre-cluster-data-readiness.md)  
**Pulse API REQ:** [`49-early-signal-network-pulse-l1-api.md`](../../../requirements/49-early-signal-network-pulse-l1-api.md)  
**Emerging API REQ:** [`50-early-signal-emerging-l2-api.md`](../../../requirements/50-early-signal-emerging-l2-api.md)  
**Parent product:** [`DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md`](../../../../../docs/requirements%20backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md) §§5–6, §10, §12, §22–23, §29, §33  
**Sibling:** [`spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md`](../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md)

> **Назначение.** Inventory: какие **уже существующие** gateway stores/read paths могут честно поддержать Early Signal (Network Pulse / Emerging) и какие пробелы требуют follow-on REQ/стори. Исходный Draft-48 / TASK-ES-01 **не** назначали HTTP path; path+payload закрыты **REQ-49** / ES-02 (`GET /tallinn/network-pulse`) и **REQ-50** / ES-03 (`GET /tallinn/emerging-signals`). Follow-ups: `TASK-GW-ES-04` (docs seam), hygiene ES-05–ES-08.

---

## 1. Normative constraints (AC-GW-ES-02..05)

1. **No new public route** was mandated by Draft-48 / TASK-GW-ES-01 alone (inventory era). Shipping Pulse path is **REQ-49** / ES-02: `GET /tallinn/network-pulse`.
2. **Privacy:** Story author keys are opaque — [`contracts.py:48–49`](../../../../src/core/domain/contracts.py) `submitter_external_user_id`, `submitter_identity_issuer`. Any *future* aggregate payload MUST NOT include PII (contacts, raw identity joins). **Voices** (unique persons) = out of gateway MVP; do not count via identity contacts.
3. **Topic ≠ Issue.** Taxonomy / topic counts MUST NEVER be labeled as Issue counts. **No** deterministic «N Stories until Issue» counter unless promotion logic is publicly defensible (parent §22.2, §23); anti-threshold-gaming copy remains product-level.
4. **Emerging Signal** is a UI/product concept: derived/ephemeral unless a later REQ introduces a persistent entity (parent §6.2). Must not equal published Issue projection (Level 3).
5. **Sibling spa-15:** L1 Pulse + L2 Emerging paths known (REQ-49 / REQ-50); remaining board seam = **TASK-GW-ES-04**.

---

## 2. Verified inventory (code)

| Fact | Path / evidence |
|------|-----------------|
| Public Issues list (L3) | [`asgi_app.py:462`](../../../../src/core/api/asgi_app.py) `GET /tallinn/issues`; handler [`handlers.py`](../../../../src/core/api/handlers.py) |
| Public Network Pulse (L1) | [`asgi_app.py:65,434`](../../../../src/core/api/asgi_app.py) `GET /tallinn/network-pulse`; [`NetworkPulseService`](../../../../src/core/application/network_pulse.py); handler [`handlers.py:40`](../../../../src/core/api/handlers.py) |
| Public Emerging L2 | [`asgi_app.py:67,450`](../../../../src/core/api/asgi_app.py) `GET /tallinn/emerging-signals`; [`EmergingSignalsService`](../../../../src/core/application/emerging_signals.py); handler [`handlers.py:51`](../../../../src/core/api/handlers.py) |
| Issues fetch-all then filter | [`db_supabase.py:789–833`](../../../../src/core/infrastructure/db_supabase.py) `list_projections` → `filter_projection_rows` |
| Public content routes | [`asgi_app.py:58–67`](../../../../src/core/api/asgi_app.py) `PUBLIC_ROUTES`: … + `/tallinn/network-pulse` + `/tallinn/emerging-signals` |
| `/metrics` service-auth | [`asgi_app.py`](../../../../src/core/api/asgi_app.py) `PROTECTED_ROUTES`; [`handlers.py`](../../../../src/core/api/handlers.py) |
| `/metrics` payload | [`api/metrics.py:31–38`](../../../../src/core/api/metrics.py) — in-process counters only (`health_requests`, …); **no** Story/Issue domain counts (≠ Pulse / Emerging) |
| Opaque author keys | [`contracts.py:48–49`](../../../../src/core/domain/contracts.py) |
| Story list Protocol | [`contracts.py:79–87`](../../../../src/core/domain/contracts.py) `list_stories`, `list_stories_by_submitter`, `list_stories_ready_for_clustering` |
| Story timestamps / language / geo | [`contracts.py:51–62`](../../../../src/core/domain/contracts.py) `created_at`, `updated_at`, `narrative_language`, `narrative_session_language`, `geo: StoryGeoSnapshot` |
| Supabase `list_stories` | [`db_supabase.py:517–523`](../../../../src/core/infrastructure/db_supabase.py) order `created_at.asc` |
| Required signal axes (6) | [`profile/schema.py:6–13`](../../../../src/core/profile/schema.py) |
| SignalDimension enum | [`contracts.py:172–193`](../../../../src/core/domain/contracts.py) incl. `geographic_district`, civic axes |
| `story_labels` / `story_signals` / `cluster_memberships` ports | [`db_supabase.py:39–42`](../../../../src/core/infrastructure/db_supabase.py) readiness; REST paths `:1137+`, `:1180+`, `:1248+` |
| Cluster lenses | [`cluster/types.py:10–22`](../../../../src/core/cluster/types.py) |
| Cluster cron | [`scheduler/cluster_cron.py:15+`](../../../../src/core/scheduler/cluster_cron.py); gated [`asgi_app.py:156–178`](../../../../src/core/api/asgi_app.py) |

**Unknown (not claimed):** whether any *other* internal admin route (beyond `/metrics`) exposes Story counts suitable for public reuse — none found on public content reads; `/metrics` itself is unfit (service-auth + no Story counts).

---

## 3. AC-GW-ES-01 — Parent metric → source → Public today? → Gap

| Parent metric (Level) | Existing source (file/store) | Public today? | Gap |
|-----------------------|------------------------------|---------------|-----|
| **L1 Stories collected** | Count via `StoryRepository.list_stories` — Protocol [`contracts.py:79–81`](../../../../src/core/domain/contracts.py); Pulse fold [`network_pulse.py`](../../../../src/core/application/network_pulse.py) | **Y** — `GET /tallinn/network-pulse` [`asgi_app.py:65`](../../../../src/core/api/asgi_app.py) (`stories_collected`) | Closed by ES-02 / REQ-49 (Awaiting Commits OK) |
| **L1 Voices / unique contributors** | Opaque `submitter_external_user_id` [`contracts.py:48`](../../../../src/core/domain/contracts.py); distinct count theoretically possible in-process | **N** | Out of gateway MVP / identity+privacy ADR; do not join contacts |
| **L1 Areas represented** | `StoryRecord.geo` / `StoryGeoSnapshot.admin_*` [`contracts.py:28–40,62`](../../../../src/core/domain/contracts.py); Pulse `areas` dim | **Y** — same Pulse route | Closed by ES-02; honesty caveat (small sample ≠ city coverage) remains |
| **L1 Topics touched** | `story_labels` + `is_public_label_disposition` [`network_pulse.py:69`](../../../../src/core/application/network_pulse.py) | **Y** — Pulse `topics` | Closed by ES-02; **Topic ≠ Issue** normative |
| **L1 Languages** | `narrative_language` on `StoryRecord`; Pulse `languages` dim | **Y** — same Pulse route | Closed by ES-02 (canonical field = `narrative_language` in service) |
| **L1 Recent Story activity** | `created_at` window; Pulse `recent_stories_7d` | **Y** — same Pulse route | Closed by ES-02 (7d UTC window) |
| **L2 Emerging Signal** | Label-freq top-N via [`EmergingSignalsService`](../../../../src/core/application/emerging_signals.py) (`story_labels` + published-exclusion); REQ-50 | **Y** — `GET /tallinn/emerging-signals` [`asgi_app.py:67`](../../../../src/core/api/asgi_app.py) | **Closed by ES-03** / REQ-50 (Awaiting Commits OK); ≠ Issues; no EmergingSignal DDL |
| **L3 Confirmed Issues** | `GET /tallinn/issues` [`asgi_app.py`](../../../../src/core/api/asgi_app.py) | **Y** | Covered; keep regression (AC-06) |

---

## 4. Gap register → backlog items (layer-1 + TASK rename 2026-08-09)

| Gap ID | Severity | Summary | Backlog | Status / Blocked on |
|--------|----------|---------|-------|------------|
| **G-ES-PUB-01** | HIGH (product) | Public Stories-collected / Pulse aggregate | [GW-ES-02](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) | **Closed / Satisfied by ES-02** (pkg-000059, REQ-49 `GET /tallinn/network-pulse`; Awaiting Commits OK) |
| **G-ES-PUB-02** | MED | Public Topics/Areas/Languages aggregates | [GW-ES-02](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) (same layer) | **Closed / Satisfied by ES-02** (Pulse dims; Awaiting Commits OK) |
| **G-ES-PUB-03** | MED | No public Emerging (L2) read distinct from Issues | [GW-ES-03](./STORY-GW-ES-03-public-emerging-l2-read.md) | **Closed / Satisfied by ES-03** (pkg-000060, REQ-50 `GET /tallinn/emerging-signals`; Awaiting Commits OK) |
| **G-ES-INV-01** | LOW | `/metrics` unfit for Pulse reuse | Folded into ES-02 note (not a separate story) | Closed as fact in §2 |
| **G-ES-DOC-01** | LOW | REQ-48 still Draft awaiting PA.2 | [TASK-GW-ES-04](./TASK-GW-ES-04-req48-spa15-contract-seam.md) | Operator PA.2 |
| **G-ES-DOC-02** | LOW | spa-15 ↔ gateway contract TBD | [TASK-GW-ES-04](./TASK-GW-ES-04-req48-spa15-contract-seam.md) | spa PA.2; L1/L2 paths known (REQ-49 / REQ-50) |

---

## 5. Open questions (block API design — from REQ-48 §6)

1. Should public Pulse expose Story **count** only, or also recent activity / languages / areas? — **Closed by ES-02 / REQ-49:** count + languages + areas + topics + `recent_stories_7d`.
2. Is Level 2 based on `cluster_memberships` + readiness, `story_signals` / `story_labels` frequency, or spa-only heuristics?
   - **MVP close (GW-ES-03 / REQ-50):** Level 2 Emerging = top-N **public taxonomy label** frequencies excluding stories linked to cabinet-**published** Issues. Path+payload SSOT: [`50-early-signal-emerging-l2-api.md`](../../../requirements/50-early-signal-emerging-l2-api.md). Cluster/memberships/`story_signals` alternatives remain successor ADR / ES-08 territory.
3. k-anonymity / minimum cell size for any aggregate?
4. Service `/metrics` reuse vs dedicated public read — **fact:** `/metrics` has no Story counts ([`api/metrics.py:31–38`](../../../../src/core/api/metrics.py)); dedicated public read = **REQ-49** / ES-02 (**Done**).
5. Hosted performance: Issues path already fetch-all + in-memory filter ([`db_supabase.py:814–833`](../../../../src/core/infrastructure/db_supabase.py)); Pulse MVP same fold — SQL/`count` deferred → [ES-06](./STORY-GW-ES-06-network-pulse-sql-count-perf.md) (evidence-gated).

---

## 6. Regression (AC-GW-ES-06)

TASK-GW-ES-01 / this gap analysis are **docs/decision only**. No change to `GET /tallinn/issues` behavior. Implementation that would alter Issues read requires explicit operator scope expand + separate story.

---

## 7. Traceability

| AC | Satisfied by |
|----|----------------|
| AC-GW-ES-01 | §3 matrix |
| AC-GW-ES-02 | §1.1 |
| AC-GW-ES-03 | §1.2 + §2 opaque keys |
| AC-GW-ES-04 | §1.3 |
| AC-GW-ES-05 | Meta sibling + §1.5 |
| AC-GW-ES-06 | §6 |
