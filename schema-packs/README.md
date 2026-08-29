# Schema packs (data) — GW-SSR-01 loader contract

**Not** a frozen universal YAML dialect. Keys below are **this gateway loader only** (SCHEMA-005: syntax implementation-specific for a single loader). Parent SCHEMA-003 states are representable; CL-001 is the **shape** of the clustering block, not the whole pack.

## On-disk layout

```text
schema-packs/<schema_id>/<schema_version>/
  pack.json              # manifest (JSON data — SEC-001: not executed)
  payload.schema.json    # JSON Schema for structured_payload
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
