# 48. Early Signal / Pre-Cluster — Data Readiness (no invented API)

Parent: docs/requirements backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md §5–6, §10, §12, §22–23, §29, §33  
Parent-id: early-signal-dashboard-pre-cluster  
Siblings: spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md (contract: TBD-question — which Level 1/2 facts can be exposed publicly without PII; no path in parent)  
Status: Draft — awaiting PA.2  

Дата: 2026-08-09  
Проект: doge-complaints-gateway  
Фокус: inventory существующих источников vs parent Level 1/2; privacy; запрет Topic≠Issue; **без** назначения HTTP path/body в этом Draft

---

## 1) Goal

Зафиксировать, какие **уже существующие** gateway stores/read paths могут честно поддержать Early Signal (Stories activity, taxonomy/geo aggregates, cluster maturity hints) и какие пробелы требуют отдельного API/ADR — **не** проектируя endpoint в этом документе (parent §33; §6.2 Emerging Signal не обязан быть entity).

---

## 2) Scope / Out of scope

### In scope

- Inventory: Stories store, story signals, cluster memberships, Issues projection read.
- Mapping parent Level 1 candidate metrics (§10) → possible existing data vs Unknown.
- Constraints: privacy (no PII in gateway content plane — primer §5); Topic ≠ Issue (§10); honest data (§22); anti-threshold gaming (§23).
- Open questions list for PA.2 / future REQ if public aggregates are approved.
- Explicit non-creation of `EmergingSignal` persistent entity unless later architecture requires (parent §6.2).

### Out of scope

- Inventing `/…` paths, response schemas, or DB tables in this Draft.
- Changing clustering math / promotion gates (parent §33).
- Voices / unique verified persons (identity).
- SPA layout/copy (sibling 15).
- Offers (§32).

---

## 3) Verified current state

| Fact | Path |
|------|------|
| Public Issues list | `asgi_app.py:427` `GET /tallinn/issues`; handler `handlers.py:362` |
| Issues fetch-all then Python filter | `db_supabase.py:814–833` → `filter_projection_rows` |
| StoryRecord author keys (opaque) | `domain/contracts.py:48–49` `submitter_external_user_id`, `submitter_identity_issuer` |
| Required signal axes (6) | `profile/schema.py:6–13` |
| SignalDimension enum (extended) | `domain/contracts.py:172–194` |
| Cluster lenses | `cluster/types.py:10–22` |
| Story list methods on store Protocol | `domain/contracts.py:79–87` `list_stories`, `list_stories_by_submitter`, `list_stories_ready_for_clustering` |
| Cluster cron | `scheduler/cluster_cron.py:15+`; gated `asgi_app.py:156–175` |
| Public HTTP for Story count / pulse / emerging | **Not found** on `asgi_app.py` public content reads (Issues + story-drafts + health/ready) |
| embedding `vector(8)` | `supabase/migrations/20260423_1500_init_db_wave.sql:32,51` |

Unknown: whether any internal admin/metrics route already exposes Story counts suitable for public reuse (`/metrics` is service-auth — `asgi_app.py:393`).

---

## 4) Target behavior

1. This REQ **documents readiness**, not a shipping public pulse API.
2. Any future public aggregate MUST:
   - expose only non-PII aggregates consistent with primer privacy invariant;
   - never label taxonomy topic counts as Issue counts;
   - never expose deterministic «N Stories until Issue» unless promotion logic is publicly defensible (parent §22.2, §23);
   - treat Emerging Signal as derived/ephemeral unless a later REQ introduces an entity (§6.2).
3. Level 3 remains `GET /tallinn/issues` (existing).
4. Level 1 «Stories collected»: theoretically computable from Story store **internally**; public exposure = Open question (no path here).
5. Level 1 Areas / Topics / Languages: depend on geo + signals/taxonomy already on stories; public exposure = Open question.
6. Level 2 Emerging: may use cluster membership / readiness / repeated signal dimensions — rules TBD; must not equal published Issue projection.
7. Voices metric: out of gateway MVP; do not count persons via join to identity contacts.

---

## 5) Acceptance criteria

1. AC-GW-ES-01: This REQ (after PA.2) contains a table Parent metric → Existing source (file/store) → Public today? (Y/N) → Gap.
2. AC-GW-ES-02: Document states explicitly: **no** new public route is mandated by Draft-48 alone.
3. AC-GW-ES-03: Privacy section cites opaque submitter keys (`contracts.py:48–49`) and forbids PII fields in any future aggregate payload.
4. AC-GW-ES-04: Topic≠Issue and no «Stories until Issue» counter are listed as normative constraints for any follow-on API REQ.
5. AC-GW-ES-05: Sibling spa-15 is referenced; contract seam remains TBD-question until a follow-on gateway REQ (new NN) defines a path — if ever.
6. AC-GW-ES-06: Regression: existing `GET /tallinn/issues` behavior not broken by work under this REQ (this REQ is docs/decision unless PA.2 expands scope with explicit operator approval).

---

## 6) Open questions (block PA.2 API design)

1. Should public Pulse expose Story **count** only, or also recent activity / languages / areas?
2. Is Level 2 based on `cluster_memberships` + readiness, `story_signals` frequency, or spa-only heuristics?
3. k-anonymity / minimum cell size for any aggregate (related to matching D3 — not decided here)?
4. Service `/metrics` reuse vs dedicated public read — operator choice?
5. Hosted performance: fetch-all Issues path already in-memory; aggregates must not worsen demo load without SQL plan.

---

## 7) Dependencies

- Parent §§5–6, 10, 12, 22–23, 29, 33.
- Sibling spa `15-early-signal-pre-cluster-public-dashboard.md`.
- Existing Issues read REQ lineage: `24-tallinn-issues-read-api.md` / projection stack.
- Primer privacy: `docs/modules/dashboard/search-matching-interviews/00-architecture-primer.md` §5.
- Not dependent on identity/gpt for this inventory Draft.
