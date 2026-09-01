# Schema packs (data) — GW-SSR-01 loader contract

**Not** a frozen universal YAML dialect. Keys below are **this gateway loader only** (SCHEMA-005: syntax implementation-specific for a single loader). Parent SCHEMA-003 states are representable; CL-001 is the **shape** of the clustering block, not the whole pack.

## On-disk layout

```text
schema-packs/<schema_id>/<schema_version>/
  pack.json              # manifest (JSON data — SEC-001: not executed)
  payload.schema.json    # JSON Schema for structured_payload
  taxonomy.json          # optional Contour2 vocabulary (SSR-26); required only when pack.json declares taxonomy_schema
```

Example ids (parent §29 Integration): `legal_process.v1`, `mobility_observation.v1`, `tallinn_civic.v1`

- Resolve key: `(schema_id, schema_version)` → directory `schema-packs/<schema_id>/<schema_version>/`
- Packs root: env `SCHEMA_PACKS_ROOT` or default `<gateway-root>/schema-packs/`

## Loader keys (`pack.json`)

| Key | Type | Meaning |
|-----|------|---------|
| `schema_id` | string | Pack identity (folder name) |
| `schema_version` | string | Pack version (folder name) |
| `payload_schema` | string | Filename of JSON Schema (relative to pack dir) |
| `field_policy` | object | Map `dotted.path` → SCHEMA-003 state |
| `exact_lenses` | array | ≥1 exact-lens block (CL-001 example **shape**) |
| `compatible_profiles` | array of string, optional | If set, `policy_context.profile_ref` must be a member (RUNTIME-005 profile incompatibility) |
| `dual_civic_lenses` | boolean, optional | SSR-10 Path B. `true` = bound story also gets civic `ClusterLens` memberships from labels / `infer_signals_from_canonical` **and** pack exact-lenses from payload. Absent or `false` = T-wave exact-only. Not required on existing packs (`legal_process`, `tallinn_civic`). This loader only (SCHEMA-005) — not a frozen YAML dialect. |
| `card_fields` | array of string, optional | SSR-11. Dotted paths from `structured_payload` that MAY appear as **named** leaves on `GET /node/issues` under sidecar `schema_card` (flat keys = the dotted path). Absent, `null`, or `[]` = civic card form (no sidecar). This loader only (SCHEMA-005). `field_policy` `forbidden` / `node_private` are never projected even if listed. Do **not** dump the whole payload. Existing packs without the key stay civic-form. |
| `node_clustering` | object, required | SSR-19/20. Civic `ClusterLens` knobs for this node pack. This loader only (SCHEMA-005) — **not** a frozen YAML dialect. Missing / invalid → loader/`ConfigError`. Factory/handlers read this block (not AppConfig semantic `CLUSTER_*`). Cron stays env (`CLUSTER_CRON_*`). |
| `geo_intake` | object, required | SSR-23. Pack policy for envelope sidecar `geo_detail` + merge with `narrative.location_query`. This loader only (SCHEMA-005) — **not** a frozen YAML dialect. Missing / invalid → loader/`ConfigError`. No env override. |
| `taxonomy_schema` | string, optional | SSR-26. Filename relative to pack dir (symmetric with `payload_schema`). **Absent** = no taxonomy block (`SchemaContext.taxonomy is None`); on-disk `taxonomy.json` without this key is **not** auto-loaded. **Present** = file **required**; missing file → loader `UnsupportedVersionError`. This loader only (SCHEMA-005) — **not** a frozen YAML dialect. Tallinn official seed = SSR-28. Operator copy-paste manual = SSR-29 (placeholder). |

### `taxonomy.json` blocks (SSR-26; Contour2 pack vocabulary)

Wire Contour1 (`narrative.taxonomy` / GW-TAX-01) is **unchanged**. This file is pack SSOT for GPT byte-copy vocabulary + `axis_to_signal_map` — not a second wire blob.

| Block | Notes |
|-------|--------|
| `schema_id` / `schema_version` | Must match `pack.json` |
| `axes[]` | Non-empty; each ∈ gateway `TAXONOMY_AXIS_VALUES`; **set must equal** all 13 |
| `internal_axes[]` | Each ∈ `axes[]` |
| `canonical_keys` | Object keyed by axis; entries `{key, meaning?}`; no duplicate `key` per axis |
| `axis_to_signal_map` | Keys ∈ axes; values non-empty dotted paths (e.g. `signals.civic_domain`) |
| `dispositions` | Subset of label dispositions; default all five if omitted |

Do **not** invent a frozen YAML dialect here. Full operator manual / GPT lockstep checklist → SSR-29 (placeholder until that story).

### `field_policy` states (SCHEMA-003, representable)

`required` · `optional` · `disabled` · `forbidden` · `node_private` · `derived` · `computed_aggregate_only`

### `exact_lenses[]` (CL-003 conceptual tokens)

| Token | pack.json field | Notes |
|-------|-----------------|-------|
| lens_id | `lens_id` | |
| source_fields / source_signals | `source_fields` | string array |
| algorithm | `algorithm` | e.g. `exact` |
| scope | `scope` | |
| scale | `scale` | |
| missing_value_policy | `missing_value_policy` | |
| min_size | `min_size` | |
| readiness policy | `readiness_policy` | maps to existing `PromotionGatePolicy` **3 knobs** |
| version | `version` | |

### `readiness_policy` → `PromotionGatePolicy` (SSR-05 mapping; numbers **in this file**)

| Knob | pack.json field | Civic Python default (do **not** copy into schema runtime) |
|------|-----------------|-----------------------------------------------------------|
| `min_readiness_score` | `min_readiness_score` | 70 in `gates.py` — unused here |
| `min_stories` | `min_stories` (from CL-003 `min_size`) | 2 in `gates.py` — unused here |
| `require_actionable_canonical_type` | `require_actionable_canonical_type` | civic `True`; pack examples use `false` |

Example packs carry **different** numbers (data, not code defaults).

### `node_clustering.civic` (SSR-19; CL civic contour)

**Not** `exact_lenses` (pack exact engine). Civic knobs live here so a node pack is the SSOT for `ClusteringEngine` / civic promote / dual + unbound (wiring = SSR-20).

| Field | Type | Notes |
|-------|------|-------|
| `active_lenses` | array of string | Known `ClusterLens` ids; non-empty; `primary_lens` must be a member |
| `primary_lens` | string | Must be a known lens id and ∈ `active_lenses` |
| `min_size` | integer | Positive (former env `CLUSTER_MIN_SIZE`; now pack-only) |
| `min_size_by_lens` | object | Map known lens id → positive int (former env `CLUSTER_MIN_SIZE_BY_LENS`) |
| `readiness_threshold` | integer | Range 1–100 |
| `signal_source` | string | `canonical` |
| `id_algorithm` | string | `legacy_hash` \| `sha256` |
| `geo_filter` | string | `district` \| `settlement` \| `region` \| `country` |
| `geo_scope` | string or `null` | Optional zone `<level>:<value>` (e.g. `settlement:tallinn`); `null` = no pack scope |
| `tie_breaker` | string | `alpha` |
| `type_resolution` | string | e.g. `canonical_priority` |

Example packs copy former EnvSpec defaults: min_size `5`; `min_size_by_lens` includes `composite_primary_micro=8`; readiness `60`; 10 civic lenses; primary `composite_primary_micro`; signal `canonical`; id `sha256`; geo_filter `country`; tie `alpha`; type `canonical_priority`. `tallinn_civic` sets `geo_scope` to `settlement:tallinn`; `legal_process` / `mobility_observation` use `null`. Do not put `CLUSTER_CRON_*` in pack.json. How-to: [schema-packs-node-data-model-ru.md](../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md) §два контура.

### Envelope sidecar `geo_detail` (SSR-23)

Root object next to `narrative` / `schema_binding` (same class as `gpt_signals` — **not** a second binding). Parse shared on stash+submit. Invalid → `IntakeValidationError`. Empty / omitted → absent.

| Field | Notes |
|-------|--------|
| `latitude` / `longitude` | Optional pair; both or neither |
| `address` | Optional object. Components: `country`, `region`, `settlement`, `district`, `street`; house depth is `house` **XOR** `house_range` **XOR** `houses[]` |
| `normalized_label` | Optional string |
| `confidence` / `provider` | Optional |

`location_query` stays for fuzzy resolve. Scope gate SSR-22 is unchanged (scope check only when `location_query` is present).

### `geo_intake` (SSR-23)

| Field | Type | Notes |
|-------|------|--------|
| `mode` | string | `optional` \| `require_location_or_detail` \| `require_detail` |
| `merge` | boolean | `true` = client `geo_detail` wins over provider miss / overlays admin leaves. Address-only + provider miss does **not** invent coordinates (→24). |
| `mirror_to_payload` | boolean | When `true`, write `structured_payload.geo.*` (district / settlement / region / country / street / house / house_range / houses) **before** pack validate |

Official three packs ship `mode=optional` so omit stays 202. `tallinn_civic` sets `mirror_to_payload=true` (has `geo.*` lens paths). `legal_process` / `mobility_observation` set `mirror_to_payload=false`. Persistence of street/houses columns is SSR-24. Clustering: civic still buckets `admin_*` only (`geo_filter`); pack exact joins mirrored `structured_payload.geo.*` — see [manual](../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md) §geo_detail.
