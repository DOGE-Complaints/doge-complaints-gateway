# STORY-GW-SSR-28 — tallinn_civic/v1 taxonomy.json seed (pack data)

## Meta
- **Key:** `STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** Done (Awaiting Commits)
- **Приоритет:** P1 — taxonomy-pack wave (sequence **28**)
- **Тип:** implement (pack data materialization)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md)
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** [GW-SSR-26](./STORY-GW-SSR-26-taxonomy-json-pack-contract.md) Done (loader parses file)
- **Blocks:** [GW-SSR-29](./STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md) (checklist needs real paths)
- **Siblings (GPT):** [GPT-SSR-05](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-05-taxonomy-json-pack-copy-paste.md) · [GPT-SSR-09](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-09-use-case-audit-core-consume-json.md)

## Зачем простыми словами

Loader (SSR-26) без **реального файла** бесполезен для copy-paste. Активная нода `tallinn_civic/v1` должна иметь **`taxonomy.json`**, собранный из согласованных источников — не «придуманный заново» vocabulary.

Без seed GPT-SSR-05 / GPT-SSR-09 capstone **заблокированы** на taxonomy path; tallinn requiredness policy SSR-26 не проверяется на prod pack.

---

## Verified as-built (2026-09-01)

| Fact | Evidence |
|------|----------|
| `pack.json` tallinn | [`schema-packs/tallinn_civic/v1/pack.json`](../../../../schema-packs/tallinn_civic/v1/pack.json) — **`taxonomy_schema`: `taxonomy.json`** (P3 Done) |
| `taxonomy.json` | Seeded 13 axes / 182 keys from GPT §4/§5/§6; loader green |
| Required signals | `field_policy`: `signals.civic_domain`, `signals.failure_pattern` = `required` |
| GPT axis→signal today | [`data-model.md` §2.3](../../../../GPT%20UI/instructions/schema-packs/tallinn_civic/v1/data-model.md) |
| GPT taxonomy SSOT | [`story-label-taxonomy.md`](../../../../GPT%20UI/instructions/story-label-taxonomy.md) v0.2.3 |
| Overlap vocab (spot-check) | [`vocabulary.py`](../../../../src/core/cluster/vocabulary.py) `CIVIC_DOMAIN_VOCABULARY`, `FAILURE_PATTERN_VOCABULARY` ⊆ taxonomy keys for mapped axes |

---

## Sources of truth (explicit chain — no invent)

| Content | SSOT for extraction | Gateway cross-check |
|---------|---------------------|---------------------|
| 13 axes | GPT §3 + [`axes.py`](../../../../src/core/taxonomy/axes.py) | `set(axes) == TAXONOMY_AXIS_VALUES` |
| Canonical keys §4 | GPT `story-label-taxonomy.md` **§4.1–4.10** tables (`### 4.N …`) | Contract test: per-axis key set |
| Metadata-only keys | GPT **§5** (`location_context`, demoted `affected_scope` candidates) | Include in `canonical_keys` with meaning note |
| Internal-only keys | GPT **§6** | Split: `risk_privacy_safety` vs `confidence_state` per §6 prose |
| `internal_axes` | Story spec | `["risk_privacy_safety", "confidence_state"]` |
| Min `axis_to_signal_map` | GPT data-model §2.3 | Covers all `field_policy: required` signal paths |
| Dispositions | [`disposition.py`](../../../../src/core/taxonomy/disposition.py) | Five values in JSON array |

### Extraction algorithm (T01 — implement as script, not hand-wave)

```
1. For each ### 4.N heading in story-label-taxonomy.md:
   map heading → axis name (table in SSR-26 story / §4 index)
   parse markdown table rows | `key` | meaning |
2. §5: parse | `axis` | candidate examples | → expand backtick tokens into canonical_keys[axis]
3. §6: parse internal table → assign keys:
   risk_privacy_safety: pii_present, redaction_needed, limited_depth, minor_context, health_context, violence_context
   confidence_state: confirmed_by_user, gpt_hypothesis, needs_clarification, low_confidence, conflict_unresolved
4. Dedupe per axis; HARD STOP if §4 key missing vs prior GPT export
5. Do NOT parse §7 disposition table into canonical_keys (dispositions live in top-level array)
```

**Expected volume:** ~170–190 keys total (13 axes); order-of-magnitude gate, not hard AC.

---

## Scope / Out of scope

**In:**

- Materialize [`schema-packs/tallinn_civic/v1/taxonomy.json`](../../../../schema-packs/tallinn_civic/v1/taxonomy.json)
- Update [`pack.json`](../../../../schema-packs/tallinn_civic/v1/pack.json): `"taxonomy_schema": "taxonomy.json"`
- Contract tests `tests/test_gw_ssr_28_taxonomy_seed.py`
- Enable tallinn required taxonomy load (SSR-26 policy)

**Не включать в JSON:**

- Interview prose — GPT `interview-overlay.md`
- Privacy / admission rules — GPT `inbound-validation.md`
- OpenAPI / wire schema

**Out:**

- `mobility_observation/v1`, `legal_process/v1` taxonomy files
- Auto-generator tooling (future story)
- Silent renames vs GPT §4
- GPT-side copy (GPT-SSR-09 P3; SSR-29 documents path)

---

## `axis_to_signal_map` MVP

Minimum (required by AC):

| Axis | Signal path |
|------|-------------|
| `topic_domain` | `signals.civic_domain` |
| `failure_mode` | `signals.failure_pattern` |

Optional axes → optional `signals.*` per `field_policy` — **document as residual**; expand in later pack revision.

**AC-GW-SSR28-04 test:**

```python
required_signals = {path for path, state in manifest["field_policy"].items()
                    if state == "required" and path.startswith("signals.")}
mapped = set(taxonomy["axis_to_signal_map"].values())
assert required_signals <= mapped
```

---

## Подзадачи (детализация)

### T01 — Extract / inventory

- Script or tabular pass: GPT §4 + §5 + §6 → per-axis key sets
- Diff vs [`vocabulary.py`](../../../../src/core/cluster/vocabulary.py) overlap axes only (`topic_domain`, `failure_mode`)
- Output: inventory artifact in test or inline assertion (no silent renames)

**Gate:** `test_canonical_keys_inventory_matches_gpt_md_section_four` green

**Pitfall:** naive grep picks `needs_clarification` from §7 into wrong axis — use section-scoped parser only.

---

### T02 — Compose `taxonomy.json`

- Write file per GW-SSR-26 shape
- `schema_id` / `schema_version` match pack
- Valid JSON, UTF-8, trailing newline

**Gate:** manual `json.load` + loader `resolve_pack(SchemaRef("tallinn_civic","v1"))` returns non-None taxonomy

---

### T03 — Pack manifest

Add to tallinn `pack.json` (only this pack):

```json
"taxonomy_schema": "taxonomy.json"
```

**Не:** touch legal/mobility manifests

---

### T04 — Validate / tests

Create `tests/test_gw_ssr_28_taxonomy_seed.py`:

| Test | Assert |
|------|--------|
| `test_manifest_declares_taxonomy_schema` | key + file on disk |
| `test_taxonomy_axes_lockstep_thirteen` | 13 axes |
| `test_required_signals_covered_by_axis_to_signal_map` | AC-GW-SSR28-04 |
| `test_canonical_keys_inventory_matches_gpt_md_section_four` | AC-GW-SSR28-05 |
| `test_vocabulary_overlap_axes_subset_of_taxonomy_keys` | civic_domain + failure_pattern frozensets |
| `test_tallinn_resolve_requires_taxonomy_pack` | loader roundtrip |

Regression: `tests/test_gw_ssr_26_*`, `tests/test_gw_ssr_01_*`

---

### T05 — Handoff indicator

- File ready for byte-copy (SSR-29 checklist)
- **Не** perform GPT copy in gateway P3 (operator / GPT-SSR-05)

---

## Target / AC

- [x] **AC-GW-SSR28-01:** `taxonomy.json` exists under `tallinn_civic/v1/`.
- [x] **AC-GW-SSR28-02:** `pack.json` references `"taxonomy_schema": "taxonomy.json"`.
- [x] **AC-GW-SSR28-03:** All 13 axes; lockstep `TAXONOMY_AXIS_VALUES`.
- [x] **AC-GW-SSR28-04:** `axis_to_signal_map` values cover all required `signals.*` in `field_policy`.
- [x] **AC-GW-SSR28-05:** Canonical keys match GPT §4+§5+§6 extraction (test-backed; zero silent renames).
- [x] **AC-GW-SSR28-06:** `resolve_pack(tallinn_civic/v1)` succeeds with taxonomy loaded.

---

## Dependencies

- GW-SSR-26 Done
- Feeds GW-SSR-29
- Unblocks GPT-SSR-05 T04, GPT-SSR-09 partial P3

---

## Residual

- Full optional axis→signal map for all optional `signals.*`
- mobility/legal taxonomy seeds
- Operator `shasum` CI diff (SSR-29 residual tooling)

---

## Pitfalls (from dry-run)

1. **Duplicate keys** in one axis → loader hard fail (SSR-26). Regenerate, don't hand-edit governance block.
2. **Orphan JSON** without manifest update → tests pass file existence but prod load ignores file.
3. **§4 vs §6 confusion** — `canonical` disposition token is **not** a label key; lives only in `dispositions[]`.
