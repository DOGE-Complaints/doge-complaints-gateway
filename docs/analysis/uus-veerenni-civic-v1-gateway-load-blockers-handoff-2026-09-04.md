# Dual gap analysis: Pack Builder onboarding meta → uus_veerenni_civic v1 (gateway Schema Runtime)

| Field | Value |
|-------|--------|
| **Date** | 2026-09-04 (post **D-SSR-11** ship: SSR-31/32/33 Done) |
| **Project** | `doge-complaints-gateway` |
| **Method** | [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — only verified claims |
| **Parent context** | [`docs/analysis/uus-veerenni-civic-v1-pack-validation-gateway-handoff-2026-09-03.md`](../../../docs/analysis/uus-veerenni-civic-v1-pack-validation-gateway-handoff-2026-09-03.md) |
| **Architecture SSOT** | [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](./architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md) (**D-SSR-11**) |
| **Node-taxonomy stories** | [SSR-31](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md) Contour2 · [SSR-32](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md) Contour1 · [SSR-33](../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md) docs — all **Done (Awaiting Commits)** pkg-000088…090 |

**Purpose:** Parts A + B under the **shipped** flexible node taxonomy (not the pre-31 lockstep world).

**Out of this pass:** uus `pack.json` civic/exact repair; GPT-SSR-15 rewrite; Railway Volume; code.

---

## Operator summary

**A — Onboarding meta vs gateway (now):** Contour2/Contour1 axis openness is **aligned**: Pack Builder already allows free `axes`; gateway **As-of-Done** accepts pack-defined Contour2 axes (SSR-31) and any non-empty Contour1 wire axis (SSR-32). Residual meta gaps are **non-taxonomy**: weak `exact_lenses` / civic clustering shape, wrong `geo_intake.mode` examples, free `field_policy` strings, meta-required optional blocks. Sibling [GPT-SSR-15](../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-15-taxonomy-meta-axis-lockstep.md) (lock meta to 13) remains **wrong direction** — invert in GPT wave (SSR-33 recorded).

**B — uus_veerenni:** 24-axis Contour2 is **valid node model** under D-SSR-11 — **not** a load blocker and **must not** be remapped to 13. Gateway load still **FAIL** on pack.json only: missing `readiness_policy` → missing `min_size_by_lens` → civic lenses outside `ClusterLens`. Wire custom axes OK after SSR-32. Next: repair civic/exact in pack.json, copy 3 JSON into nested `schema-packs/`, re-`resolve_pack`.

---

## Flexible taxonomy — as-built (verified)

| Contour | Behaviour **As-of-Done** | Evidence |
|---------|--------------------------|----------|
| Contour2 pack | `axes[]` = non-empty unique strings; **no** membership / set-eq to `TAXONOMY_AXIS_VALUES` | [`resolver.py`](../../src/core/schema/resolver.py) L282–295; README D-SSR-11 row |
| Contour2 structural | `internal_axes ⊆ axes`; map keys ∈ axes; dispositions enum; dupe key reject | same parser after L295 |
| Contour1 wire | `normalize_axis` = strip+lower only | [`axes.py`](../../src/core/taxonomy/axes.py) L24–31 |
| Reference set | `TAXONOMY_AXIS_VALUES` = tallinn exemplar / helpers — **not** reject SSOT | `axes.py` L3–21 |
| Civic | Unmapped axes skipped for `SignalDimension`; `ClusterLens` still 10 | unchanged D-SSR-11 |

**Historical (pre-SSR-31, for audit only):** Contour2 required `set(axes) == TAXONOMY_AXIS_VALUES` (exactly 13). That gate is **gone**.

---

## SSOT references (unchanged load gates outside taxonomy)

| Artifact | Role |
|----------|------|
| [`resolver.py`](../../src/core/schema/resolver.py) | Pack load |
| [`contracts.py`](../../src/core/schema/contracts.py) | `FIELD_POLICY_STATES`, `GEO_INTAKE_MODES` |
| [`cluster/types.py`](../../src/core/cluster/types.py) | `ClusterLens` (10) — civic only |
| [`schema-packs/tallinn_civic/v1/`](../../schema-packs/tallinn_civic/v1/) | Control; 13 axes as **data** |

**`_CIVIC_REQUIRED_KEYS`:** `active_lenses`, `primary_lens`, `min_size`, `min_size_by_lens`, `readiness_threshold`, `signal_source`, `id_algorithm`, `geo_filter`, `geo_scope`, `tie_breaker`, `type_resolution`.

---

## Part A — Gap: Pack Builder onboarding meta vs gateway (post D-SSR-11)

**Meta sources:** [`GPT UI/instructions/node-onboarding/`](../../../GPT%20UI/instructions/node-onboarding/) — `pack-builder-pack.schema.json`, `…payload-schema…`, `…taxonomy…`, `pack-builder-overlays.checklist.md`.

| Topic | Meta today | Gateway **As-of-Done** | Severity **now** |
|-------|------------|------------------------|------------------|
| taxonomy `axes` | Free strings, `minItems: 1` | Pack-defined Contour2; open Contour1 | **Aligned** (uus 24 VALID on both sides for axes). Residual: GPT-SSR-15 would **break** alignment if executed as written |
| `dispositions` / `internal_axes` | Loose / any | Disposition enum; internal ⊆ axes | **blocker when wrong** |
| `exact_lenses` | MAY `[]`; required only lens_id / source_fields / algorithm | Non-empty; + scope/scale/missing_value_policy/min_size/version/**readiness_policy** | **blocker** |
| `node_clustering` | MAY `{}` | `civic` + all `_CIVIC_REQUIRED_KEYS`; lenses ∈ `ClusterLens` | **blocker** |
| `geo_intake.mode` | Examples include invalid `required` / `disabled` | `optional` \| `require_location_or_detail` \| `require_detail` + merge/mirror; no extra keys | **blocker** |
| `field_policy` values | Any string | ∈ `FIELD_POLICY_STATES` (7) | **blocker** |
| `geo_model` / `gpt_instance_territory` / `taxonomy_schema` | Meta **required** | Gateway **optional** (typed if present) | **semantic drift** |
| Overlays checklist | Prose MD presence | MD never read by `load_pack` | **cosmetic** for load |
| Payload meta skeleton | Requires `properties.signals` | Load needs JSON Schema object only | **drift** |

### Part A — notes

1. **Taxonomy is no longer the primary meta↔runtime false-admission story.** uus Contour2 axes were always meta-VALID; gateway now matches that product rule.
2. False admission for uus still comes from **exact lenses + civic clustering** meta weakness (VALID pack.json without readiness_policy / ClusterLens / `min_size_by_lens`).
3. Do **not** tighten Pack Builder taxonomy meta to 13. Prefer: free axes + structural (`dispositions`, `internal_axes ⊆ axes`) + invert GPT-SSR-15.
4. Gateway docs (README / manual) already describe node-defined axes (**SSR-33 Done**).

### Part A — repair recommendations (GPT / meta wave; not this file’s execute)

1. Harden `pack-builder-pack.schema.json`: exact lens readiness + civic ClusterLens + geo_intake enum + field_policy enum.
2. Keep taxonomy meta **free axes**; add structural checks; **cancel/invert GPT-SSR-15**.
3. Checklist: gateway load gates for readiness / civic / geo modes — **without** «must equal 13 axes».
4. Optional: make meta `geo_model` / territory / `taxonomy_schema` optional like gateway.

---

## Part B — Gap: uus_veerenni_civic/v1 vs gateway (post D-SSR-11)

### B.1 Artifacts

| Flat GPT path | Class | Gateway? |
|---------------|-------|----------|
| `schema-packs.uus_veerenni_civic.v1.pack.json` | JSON | **Yes** |
| `…payload.schema.json` | JSON | **Yes** |
| `…taxonomy.json` (24 node axes) | JSON | **Yes** — Contour2 **accepted** under D-SSR-11 |
| three `*.md` overlays | GPT prose | **No** |

Nested `schema-packs/uus_veerenni_civic/` **still absent** in gateway tree.

### B.2 Verdict split

> **Supersession (2026-09-05):** after GPT-PB-06 harden, uus `pack.json` is Pack Builder meta **INVALID** (readiness / `min_size_by_lens` / ClusterLens). Payload + taxonomy remain VALID. Full re-audit: [`docs/analysis/uus-veerenni-civic-v1-pack-validation-audit-2026-09-05.md`](../../../docs/analysis/uus-veerenni-civic-v1-pack-validation-audit-2026-09-05.md).

| Gate | Result |
|------|--------|
| Pack Builder meta (3 JSON) | **Was VALID** at writing (pre PB-06); **as of 2026-09-05:** pack.json **INVALID**, payload+taxonomy **VALID** |
| Overlays checklist | **PASS** |
| Contour2 axes (24) vs gateway | **OK As-of-Done** (SSR-31) — not a fail reason |
| Contour1 custom axes on wire | **OK As-of-Done** (SSR-32) |
| Gateway `resolve_pack` of uus pack.json as authored | **FAIL** (civic/exact only) |
| Control `tallinn_civic`/`v1` | **SUCCESS** |

### B.3 Load failure chain (current)

Only pack.json civic/exact remain. Taxonomy step removed from the live chain.

| Step | Failure | Status |
|------|---------|--------|
| 0 | `KeyError: 'readiness_policy'` on `exact_lenses[]` | **Active blocker** — uus lenses lack object |
| 1 | `node_clustering.civic missing keys: ['min_size_by_lens']` | **Active blocker** |
| 2 | `active_lenses unknown lens: primary_story_shape` (+ `service_object_local` ∉ ClusterLens) | **Active blocker** — map to e.g. `composite_primary_micro` / `service_object_micro` |
| ~~3+~~ | ~~taxonomy 24 ≠ 13~~ | **Obsolete** (SSR-31); keep uus axes |

**Exact vs civic:** custom `exact_lenses[].lens_id` OK once `readiness_policy` present; civic `active_lenses` / `primary_lens` **must** ∈ `ClusterLens`.

### B.4 Geo / district

Unchanged and **not** blocking: `geo_intake` optional/merge/mirror; `geo_scope=settlement:tallinn`; Uus-Veerenni community = prose/signals, not a new `geo_scope` level.

### B.5 Soft-ignored civic keys

`semantic_merge_policy`, `preserve_distinct_variants`, `community_focus` — ignored by parser.

### B.6 Non-blockers

Payload ≈ tallinn shape; `field_policy` values ∈ enum; `card_fields` extras OK; MD GPT-only; 24-axis taxonomy OK.

### B.7 Repair direction (operator; docs only here)

1. **Only `pack.json`:** add `readiness_policy` per exact lens; add `min_size_by_lens`; set civic lenses to `ClusterLens` values.
2. **`taxonomy.json`:** leave node axes/keys as authored — Contour2 + Contour1 already flexible.
3. Copy three JSON → `doge-complaints-gateway/schema-packs/uus_veerenni_civic/v1/`; set `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION`; `resolve_pack` until SUCCESS.
4. Then: validate samples, `card_fields` → `schema_card`, geo behaviour.

### B.8 Layout

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

## Next

| Priority | Action |
|----------|--------|
| 1 | Repair uus `pack.json` (readiness + civic ClusterLens + `min_size_by_lens`) |
| 2 | Nested copy + env + `resolve_pack` SUCCESS |
| 3 | GPT wave: invert GPT-SSR-15; optionally harden pack meta non-taxonomy gates |
| 4 | Post-load smoke: validate / card / geo |

---

## Links

| Doc | Role |
|-----|------|
| [D-SSR-11 architecture](./architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md) | Flexible vs hardcoded |
| [INDEX node-taxonomy](../tasks/backlog-stories/semantic-schema-runtime/INDEX.md) | SSR-31…33 Done |
| [Parent handoff](../../../docs/analysis/uus-veerenni-civic-v1-pack-validation-gateway-handoff-2026-09-03.md) | First VALID/FAIL inventory |
| Onboarding meta | [`node-onboarding/`](../../../GPT%20UI/instructions/node-onboarding/) |

---

## Claims hygiene

| Claim | Evidence |
|-------|----------|
| Contour2 no lockstep | `resolver.py` L282–295 (no `TAXONOMY_AXIS_VALUES` compare) |
| Contour1 open | `axes.py` `normalize_axis` L24–31 |
| README node-defined axes | `schema-packs/README.md` D-SSR-11 row |
| SSR-31/32/33 Done | Story Status + INDEX pkg-000088…090 |
| uus still missing readiness_policy | GPT flat pack.json exact_lenses (no readiness_policy key) |
| Taxonomy not current blocker | D-SSR-11 As-of-Done + B.3 |
| GPT-SSR-15 still lock-to-13 intent | GPT story file (invert pending) |

No uus pack repair and no GPT meta edit in this analysis refresh.
