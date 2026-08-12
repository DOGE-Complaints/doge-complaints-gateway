# EPIC-M2-23: Taxonomy fidelity (gateway)

## Epic Meta
- Status: Done active (TAX-01/02/03 Done awaiting commits; TAX-04 Deferred; TAX-03 P6 audit T06–T08)
- Priority: Medium-High
- Owner: TBD
- Target: Sprint 8
- **Materialized:** 2026-07-14 (P1 backlog_story STORY-GW-TAX-01); TAX-03 P1 2026-08-07

## Business Goal
Persist GPT taxonomy **без потерь** с **точно замапленной** осью (Цель 1), затем использовать per-axis данные в кластеризации (Цель 2 → GW-TAX-02). Hygiene: repo migration `story_labels` text FK SSOT (TAX-03). Синтез gap-анализа GPT §12-24/§33 + интервью 2026-07-13 ([`interview-taxonomy-persistence-clustering-2026-07-13.md`](../analysis/interview-taxonomy-persistence-clustering-2026-07-13.md)).

## Problem Statement
GPT шлёт таксономию **плоским списком**; gateway пере-угадывает ось словарями (`infer_signals_from_canonical`). ~8 осей → `unknown`; disposition не хранится. Civic-смысл историй частично теряется. Post DRAFT-07: hosted `story_labels` is text FK. **Pre-TAX-03** repo migration `20260714_…` was UUID (fresh-host drift); **post-TAX-03** (pkg-000058) repo file is text FK + RLS — dual-path closed.

## Scope
### In Scope
- STORY-GW-TAX-01: per-axis intake + `story_labels` storage + public read-filter (pipeline pkg-000054; D-TAX-1/2/3)
- STORY-GW-TAX-02: clustering axis expansion (pipeline pkg-000055 T01–T06; D-CLUST-1..4)
- STORY-GW-TAX-03: align `story_labels` migration to text FK (pipeline pkg-000058 Done; migration SSOT hygiene)
- STORY-GW-TAX-04: ALTER residual UUID hosts (Deferred backlog; TAX-03 audit G2)

### Out of Scope
- Identity
- GPT-контракт producer-side → GPT-TAX-01 (GPT UI)
- Reopen GW-DRAFT-07 / change `REQUIRED_READINESS_TABLES` for TAX-03

## Stakeholders
- Product Owner
- Backend (gateway)
- GPT UI (producer contract)
- Clustering / analytics consumers

## Dependencies
- [`interview-taxonomy-persistence-clustering-2026-07-13.md`](../analysis/interview-taxonomy-persistence-clustering-2026-07-13.md) — D-TAX-1..4
- **GPT-TAX-01** (GPT UI, cross-repo) — per-axis taxonomy in OpenAPI/instructions; предпосылка GW-TAX-01 (D-TAX-1)
- Existing intake: [`intake/contracts.py`](../../src/core/intake/contracts.py), submit bridge [`handlers.py`](../../src/core/api/handlers.py)
- TAX-03 deps: GW-TAX-01 Done; GW-DRAFT-07 Done (hosted text DDL)

## Success Metrics
- GW-TAX-01 gate PASS: per-axis intake, full `story_labels` persist, public read-filter excludes `internal`
- Legacy flat-label stories remain readable via fallback
- GW-TAX-02 unblocked for clustering axis expansion
- GW-TAX-03 gate PASS: repo migration text FK + indexes + guard; INDEX dual-path closed; DRAFT-07 not reopened

## Epic Acceptance Criteria
- GW-TAX-01 story gate PASS (pkg-000054)
- GW-TAX-02 story gate PASS (pkg-000055) after GW-TAX-01 Done
- GW-TAX-03 story gate PASS (pkg-000058) — migration SSOT text FK

## Risks and Mitigation
- **Producer lag (GPT-TAX-01):** gateway accepts legacy flat `canonical_labels` + new per-axis path in parallel (D-TAX-1)
- **Public leak of internal labels:** disposition read-filter on all public surfaces (D-TAX-3, §24)
- **Migration of existing stories:** legacy fallback via `infer_signals_from_canonical`, no breaking change
- **TAX-03 edit-in-place:** Public Node never applied UUID migration (DRAFT-07 path); fresh hosts need corrected file

## Definition of Done
- GW-TAX-01 decomposed and executed (pkg-000054 T01–T08)
- GW-TAX-02 decomposed and executed (pkg-000055 T01–T06)
- GW-TAX-03 decomposed (pkg-000058 T01–T05); execute after P2/P3

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-GW-TAX-01 | [Taxonomy persistence fidelity](./EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-01-taxonomy-persistence-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md) | Done (Awaiting Commits) pkg-000054 gate PASS 2026-07-14 |
| STORY-GW-TAX-02 | [Clustering axis expansion](./EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-02-clustering-axis-expansion/STORY-GW-TAX-02-clustering-axis-expansion.md) → [backlog](../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-02-clustering-axis-expansion.md) | Done (Awaiting Commits) pkg-000055 gate PASS 2026-07-15 |
| STORY-GW-TAX-03 | [Align story_labels migration text FK](./EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-03-align-story-labels-migration-text-fk/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md) → [backlog](../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md) | Done (Awaiting Commits) pkg-000058 gate PASS 2026-08-07 |

## Decision Ref
- [`backlog-stories/taxonomy-fidelity/INDEX.md`](../backlog-stories/taxonomy-fidelity/INDEX.md)
- [`interview-taxonomy-persistence-clustering-2026-07-13.md`](../analysis/interview-taxonomy-persistence-clustering-2026-07-13.md)
- TAX-03: [`STORY-GW-TAX-03-align-story-labels-migration-text-fk.md`](../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md); elegance + execution G1 audits
