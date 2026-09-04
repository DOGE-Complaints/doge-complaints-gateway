# Dual gap analysis: Pack Builder onboarding meta → uus_veerenni_civic v1 (gateway Schema Runtime)

| Field | Value |
|-------|--------|
| **Date** | 2026-09-04 (refresh: **D-SSR-11** node-specific taxonomy; **As-of-Done** Contour2/Contour1 after SSR-31/32; docs SSR-33) |
| **Project** | `doge-complaints-gateway` |
| **Method** | [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — only verified claims |
| **Parent context (workspace)** | [`docs/analysis/uus-veerenni-civic-v1-pack-validation-gateway-handoff-2026-09-03.md`](../../../docs/analysis/uus-veerenni-civic-v1-pack-validation-gateway-handoff-2026-09-03.md) |
| **Architecture SSOT** | [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](./architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md) (**D-SSR-11**) |
| **Stories** | [GW-SSR-31](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md) · [GW-SSR-32](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md) · [GW-SSR-33](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md) |
| **Purpose** | Two gap analyses with gateway load as SSOT; taxonomy Contour2 lockstep = **obsolete** post-SSR-31 (not «uus must remap to 13») |

**Out of this document (do not execute here):** repair uus `pack.json` civic/exact; GPT-SSR-15 rewrite; Railway Volume.

---

## Operator summary (two verdicts)

**A — Onboarding meta:** Pack Builder meta + overlays checklist are **authoring checks only**, still **weaker** than runtime on `readiness_policy`, civic ClusterLens + `_CIVIC_REQUIRED_KEYS`, `geo_intake.mode`, `field_policy`. Taxonomy: meta already allows free axes (uus VALID). **As-of-Done:** gateway Contour2 is pack-defined (SSR-31) and Contour1 wire is open (SSR-32). Meta should **stay free / structural** and **not** be tightened to 13 — sibling [GPT-SSR-15](../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-15-taxonomy-meta-axis-lockstep.md) (lock-to-13) must be **superseded/inverted** (SSR-33 records handoff). Meta still wrongly **requires** `geo_model` / `gpt_instance_territory` / `taxonomy_schema` (gateway optional).

**B — uus_veerenni_civic/v1:** GPT six-file set complete for checklist. Gateway load **NOT ready** until pack.json civic/exact repair. **Historical** `/tmp` chain (2026-09-03): `readiness_policy` → `min_size_by_lens` → unknown civic lenses → taxonomy 24≠13. **As-of-Done:** taxonomy step **obsolete as load-blocker** after SSR-31 — **keep uus 24 axes**; do **not** remap Contour2 to 13. Contour1 wire with uus axes = SSR-32 Done. Remaining hard blockers: readiness_policy, `min_size_by_lens`, civic `ClusterLens` ids.

---

## SSOT references (gateway)

| Artifact | Path |
|----------|------|
| Load / parse | [`src/core/schema/resolver.py`](../../src/core/schema/resolver.py) |
| Field / geo enums | [`src/core/schema/contracts.py`](../../src/core/schema/contracts.py) |
| Civic lens enum | [`src/core/cluster/types.py`](../../src/core/cluster/types.py) `ClusterLens` |
| Taxonomy axes reference (tallinn exemplar; **not** reject SSOT after D-SSR-11) | [`src/core/taxonomy/axes.py`](../../src/core/taxonomy/axes.py) `TAXONOMY_AXIS_VALUES` |
| Label dispositions | [`src/core/taxonomy/disposition.py`](../../src/core/taxonomy/disposition.py) |
| Control pack | [`schema-packs/tallinn_civic/v1/`](../../schema-packs/tallinn_civic/v1/) |
| Node-taxonomy arch | [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](./architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md) |

**As-of-Done (post SSR-31/32):** Contour2 pack-defined axes; Contour1 wire open; `TAXONOMY_AXIS_VALUES` = tallinn/reference only. **Historical (pre-SSR-31):** Contour2 lockstep to 13 (`resolver.py` membership/set-eq).

**ClusterLens (civic only — unchanged by D-SSR-11):**  
`composite_primary_micro`, `civic_domain_micro`, `failure_pattern_micro`, `civic_weight_systemic`, `desired_outcome_local`, `affected_group_local`, `geographic_district_micro`, `service_object_micro`, `deep_need_local`, `ecosystem_signal_systemic`.

**`_CIVIC_REQUIRED_KEYS`:**  
`active_lenses`, `primary_lens`, `min_size`, `min_size_by_lens`, `readiness_threshold`, `signal_source`, `id_algorithm`, `geo_filter`, `geo_scope`, `tie_breaker`, `type_resolution`.

**`GEO_INTAKE_MODES`:** `optional` \| `require_location_or_detail` \| `require_detail` (+ `merge`, `mirror_to_payload`).

**`FIELD_POLICY_STATES`:** `required` \| `optional` \| `disabled` \| `forbidden` \| `node_private` \| `derived` \| `computed_aggregate_only`.

---

## Part A — Gap: Pack Builder onboarding meta vs gateway load

**Meta sources (verified on disk):**

- [`pack-builder-pack.schema.json`](../../../GPT%20UI/instructions/node-onboarding/pack-builder-pack.schema.json)
- [`pack-builder-payload-schema.schema.json`](../../../GPT%20UI/instructions/node-onboarding/pack-builder-payload-schema.schema.json)
- [`pack-builder-taxonomy.schema.json`](../../../GPT%20UI/instructions/node-onboarding/pack-builder-taxonomy.schema.json)
- [`pack-builder-overlays.checklist.md`](../../../GPT%20UI/instructions/node-onboarding/pack-builder-overlays.checklist.md)

| Topic | Meta allows / requires | Gateway **historical (pre-31)** | Gateway **As-of-Done (D-SSR-11)** | Severity **today** |
|-------|------------------------|----------------------------------|-----------------------------------|--------------------|
| `exact_lenses` | MAY `[]`; weak item required | non-empty + readiness_policy + … | unchanged | **blocker** (stays) |
| `node_clustering` | MAY `{}` | civic + ClusterLens + keys | unchanged | **blocker** (stays) |
| taxonomy `axes` | Free strings, minItems 1 | lockstep exactly 13 | **pack-defined** (SSR-31); wire open (SSR-32) | **aligned** (meta free = shipped); GPT-SSR-15 lock-to-13 = **wrong direction** |
| `dispositions` / `internal_axes` | loose | disposition enum; internal ⊆ axes | same structural | **blocker when wrong** (stays) |
| `geo_intake.mode` | bad examples `required`/`disabled` | three modes + merge/mirror | unchanged | **blocker** (stays) |
| `field_policy` | any string | 7 states | unchanged | **blocker** (stays) |
| `geo_model` / territory / `taxonomy_schema` | meta **required** | gateway **optional** (+ typed if present) | unchanged asymmetry | **drift** |
| overlays / payload skeleton | prose / signals skeleton | MD unused; payload blob at load | unchanged | cosmetic / drift |

### Part A — notes (refreshed)

1. Taxonomy gap flipped by product: **uus Contour2 richness is correct**; historical gateway lockstep was the defect (arch-doc + SSR-31…33 **As-of-Done**). Do **not** recommend locking Pack Builder meta to 13.
2. Meta remains weaker on readiness_policy / civic ClusterLens — uus still fails those first.
3. Checklist still lacks gateway load-gate ticks (readiness, civic keys, ClusterLens, geo modes) — keep; «axis lockstep» tick → «Contour2 structural + node axes OK» (**SSR-33 Done**).

### Part A — repair recommendations (docs only; not executed)

1. Pack meta: harden exact lenses + civic ClusterLens + geo_intake + field_policy (unchanged from prior deepen).
2. **`pack-builder-taxonomy.schema.json`:** keep/allow **free axes** + dispositions enum + `internal_axes ⊆ axes`; **do not** const-lock to 13. Invert/cancel GPT-SSR-15.
3. Overlays checklist: gateway load gates without «must be 13 axes».
4. Optional symmetry: meta `geo_model` / territory / `taxonomy_schema` optional like gateway.

---

## Part B — Gap: uus_veerenni_civic/v1 vs gateway

### B.1 Artifact inventory

| Flat GPT path (`GPT UI/instructions/`) | Class | Gateway load? |
|----------------------------------------|-------|----------------|
| `schema-packs.uus_veerenni_civic.v1.pack.json` | JSON model | **Yes** → `pack.json` |
| `…payload.schema.json` | JSON model | **Yes** |
| `…taxonomy.json` | JSON model | **Yes** (`taxonomy_schema` set) — **24 axes = target Contour2 under D-SSR-11** |
| `…inbound-validation.md` / interview / locale | GPT prose | **No** |

`schema-packs/uus_veerenni_civic/` **not** in gateway tree yet.

### B.2 Verdict split

| Gate | Result |
|------|--------|
| Pack Builder meta | **VALID** |
| Overlays checklist | **PASS** |
| Gateway `resolve_pack` (as-built 2026-09-03) | **FAIL** |
| Control `tallinn_civic`/`v1` | **SUCCESS** |

### B.3 Failure chain (as-built) vs target

| Step | As-built failure (2026-09-03) | After D-SSR-11 / SSR-31…33 |
|------|-------------------------------|----------------------------|
| 0 | `KeyError: 'readiness_policy'` | **Still blocker** — pack.json repair |
| 1 | missing `min_size_by_lens` | **Still blocker** — pack.json repair |
| 2 | civic lens `primary_story_shape` / `service_object_local` ∉ ClusterLens | **Still blocker** — map to ClusterLens ids |
| 3+ | taxonomy 24 ≠ 13 | **Obsolete** — Contour2 unlock **SSR-31 Done**; **keep 24 axes** |

Exact `lens_id`s may stay custom; civic list cannot invent enum members.

### B.4 Geo / district intent

Unchanged: uus `geo_intake` compatible; `geo_scope=settlement:tallinn`; district community in prose/signals — not a new gateway zone level.

### B.5 Soft-ignored

`semantic_merge_policy`, `preserve_distinct_variants`, `community_focus` — ignored by civic parser.

### B.6 Non-blockers

Payload / field_policy / card_fields extras / MD GPT-only — as before.

### B.7 Repair direction (docs only; refreshed)

1. **pack.json:** `readiness_policy` on all exact lenses; `min_size_by_lens`; civic `active_lenses` / `primary_lens` ∈ ClusterLens (e.g. → `composite_primary_micro`, `service_object_micro`).
2. **taxonomy.json:** **keep** uus axes / keys (node-specific). Contour2 load accepts them (**SSR-31 Done**). Do **not** remap to 13. Contour1 wire with those axes = **SSR-32 Done**.
3. Copy three JSON → `schema-packs/uus_veerenni_civic/v1/`; `NODE_SCHEMA_*`; `resolve_pack` after pack.json repair (runtime axes unlock already shipped).
4. Docs/setup: **SSR-33 Done**.

### B.8 Local layout reminder

```text
doge-complaints-gateway/schema-packs/uus_veerenni_civic/v1/
  pack.json
  payload.schema.json
  taxonomy.json
```

```bash
NODE_SCHEMA_ID=uus_veerenni_civic
NODE_SCHEMA_VERSION=v1
```

---

## What to deepen next

| Layer | Action |
|-------|--------|
| SSR-31 → 32 → 33 | **Shipped** Contour2 unlock / Contour1 open / docs (D-SSR-11) |
| uus pack.json | Civic/exact repair only |
| Post-load | validate samples; card_fields; geo behaviour |

---

## Links

| Doc | Role |
|-----|------|
| [Architecture D-SSR-11](./architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md) | Flexible taxonomy vs hardcoded 13 |
| [GW-SSR-31](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md) | Contour2 pack axes |
| [GW-SSR-32](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md) | Contour1 wire |
| [GW-SSR-33](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md) | Docs / setup / hygiene |
| [Workspace handoff](../../../docs/analysis/uus-veerenni-civic-v1-pack-validation-gateway-handoff-2026-09-03.md) | Parent GPT + Pack Builder summary |
| [`schema-packs/tallinn_civic/v1/`](../../schema-packs/tallinn_civic/v1/) | Control pack (13 as **data**) |
| Onboarding meta | [`GPT UI/instructions/node-onboarding/`](../../../GPT%20UI/instructions/node-onboarding/) |

---

## Claims hygiene

| Claim | Evidence |
|-------|----------|
| D-SSR-11 + story map | arch-doc + INDEX node-taxonomy section |
| Historical Contour2 lockstep | `resolver.py` pre-SSR-31 membership/set-eq |
| As-of-Done Contour2/Contour1 | SSR-31/32 product + commits; docs SSR-33 |
| Failure chain 0→taxonomy | `/tmp` resolve_pack 2026-09-03 + parent analysis |
| Taxonomy step obsolete | SSR-31 Done — not a current uus load blocker |
| Remaining uus blockers | readiness_policy, min_size_by_lens, ClusterLens ids |
| GPT-SSR-15 conflict | GPT story locks meta to 13 vs D-SSR-11 — invert in GPT wave |

No uus pack repair, no GPT meta edit in this SSR-33 align pass.
