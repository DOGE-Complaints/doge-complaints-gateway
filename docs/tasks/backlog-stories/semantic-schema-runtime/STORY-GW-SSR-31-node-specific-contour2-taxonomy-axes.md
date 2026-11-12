# STORY-GW-SSR-31 — Node-specific Contour2 taxonomy axes (pack loader)

## Meta
- **Key:** `STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — pkg-000088 G31 PASS 2026-09-04T12:55:28Z
- **Приоритет:** P1 — node-taxonomy wave (sequence **31**)
- **Тип:** implement (Contour2 loader + tests)
- **Architecture SSOT:** [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](../../../analysis/architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md) (**D-SSR-11**)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md)
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [INDEX §Git branch](./INDEX.md)
- **Зависит от:** SSR-26 Done
- **Blocks:** soft SSR-33 docs wording; uus Contour2 load after pack.json civic/exact repair
- **Parallel:** [GW-SSR-32](./STORY-GW-SSR-32-node-specific-contour1-wire-axes.md) (Contour1 — other module)
- **Sibling conflict:** [GPT-SSR-15](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-15-taxonomy-meta-axis-lockstep.md) (locks meta to 13 — invert later; not this story)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)

---

# Layer 1 — Постановка задачи

## Зачем простыми словами

Loader Contour2 требует, чтобы `taxonomy.json` содержал **ровно 13** осей из `TAXONOMY_AXIS_VALUES`. Нода вроде Uus Veerenni законно описывает **свою** таксономию (24 оси). Gateway должен принимать **любой** непустой уникальный набор осей из pack data; tallinn 13 остаётся exemplar в данных, не законом в коде.

## Scope

- Remove Contour2 axis membership + set-equality lockstep in `_parse_taxonomy_pack`.
- Keep structural validation (dupe axes, `internal_axes ⊆ axes`, keys ∈ axes, dispositions).
- Adapt SSR-26 / SSR-28 tests and helpers so tallinn seed still asserts **its data** has 13 without forbidding N-axis packs.
- Prove uus-shaped 24-axis tmp pack **loads** Contour2.

## Out of scope

- Contour1 `normalize_axis` (→ SSR-32).
- Docs/README/manuals (→ SSR-33).
- uus `pack.json` readiness_policy / civic ClusterLens repair.
- `ClusterLens` expand; pack → `vocabulary.py`.
- GPT meta / GPT-SSR-15 edit.

## Short AC (Layer 1)

- [x] **AC-GW-SSR31-01:** Pack with node-defined axes (≠13 / extras / missing tallinn axes) loads when structurally valid.
- [x] **AC-GW-SSR31-02:** Structural rejects unchanged (dupe axis, unknown key in maps, internal ⊈ axes, bad dispositions).
- [x] **AC-GW-SSR31-03:** Tallinn official seed still loads; tests do not require code lockstep for all packs.
- [x] **AC-GW-SSR31-04:** `TAXONOMY_AXIS_VALUES` no longer used as Contour2 reject SSOT in resolver.

---

# Layer 2 — Реализация (техническая проработка)

## Verified as-built (pre-P3) → As-of-Done (post-P3 / G31)

| Fact | Evidence |
|------|----------|
| Contour2 axes | **As-of-Done:** pack-defined; no membership/set-eq to 13 — [`resolver.py`](../../../../src/core/schema/resolver.py) `_parse_taxonomy_pack`. **Historical (pre-P3):** L293–303 `unknown axis` + `must equal all 13`. |
| Structural checks | internal_axes ⊆ axes; canonical_keys / axis_to_signal_map keys ∈ axes; dispositions ∈ `LABEL_DISPOSITION_VALUES` — **unchanged** |
| Optional Contour2 | Absent `taxonomy_schema` → `taxonomy is None` |
| Tests | **As-of-Done:** SSR-26 ≠13 load + structural; SSR-28 tallinn **content** 13; SSR-31 24-axis SUCCESS. **Historical:** SSR-26 `unknown axis` frozen-set; SSR-28 implied loader lockstep. |
| README | [`schema-packs/README.md`](../../../../schema-packs/README.md) L44 «set must equal all 13» — **residual → SSR-33** (out of this story) |
| uus | 24-axis tmp load proven in `test_gw_ssr_31_*` (no uus pack.json product edit) |

## Target behaviour

```text
axes[]:
  - non-empty array
  - each entry non-empty string (strip; preserve or lower — match current strip-only Contour2 style)
  - no duplicates
  - NO check against TAXONOMY_AXIS_VALUES
  - NO set-equality to 13

unchanged: schema_id/version match; file required if taxonomy_schema set;
  internal_axes ⊆ axes; canonical_keys/axis_to_signal_map keys ∈ axes;
  dispositions enum; duplicate canonical key reject
```

## Touch list (P3)

| Path | Change |
|------|--------|
| [`src/core/schema/resolver.py`](../../../../src/core/schema/resolver.py) | Delete membership + lockstep block (~L293–303); keep loop for non-empty + dupe |
| [`tests/test_gw_ssr_26_taxonomy_loader.py`](../../../../tests/test_gw_ssr_26_taxonomy_loader.py) | Replace «unknown axis vs frozen set» with: (a) uus-shaped multi-axis pack loads; (b) axis in `canonical_keys` not in `axes[]` still fails; (c) duplicate axis still fails |
| [`tests/test_gw_ssr_28_taxonomy_seed.py`](../../../../tests/test_gw_ssr_28_taxonomy_seed.py) | Assert tallinn **file/content** has 13 / equals reference set as **seed invariant**, not «loader rejects other sets» |
| [`tests/helpers/ssr28_gpt_taxonomy_extract.py`](../../../../tests/helpers/ssr28_gpt_taxonomy_extract.py) | Stop treating `TAXONOMY_AXIS_VALUES` as reject for arbitrary inventory; keep as tallinn extract expected set if helper is tallinn-only |
| New test module optional | `tests/test_gw_ssr_31_node_taxonomy_contour2.py` — preferred home for 24-axis load SUCCESS |

## Setup

- tmp_path nested `schema-packs/<id>/<ver>/` (existing SSR-26 pattern).
- No new env vars.
- Fixtures may copy uus axes list from GPT flat taxonomy or inline minimal 24/N-axis stub with matching maps.

## Concrete AC (P3 gate)

- [x] **AC-GW-SSR31-01:** tmp pack declaring `taxonomy_schema` with axes set **≠** `TAXONOMY_AXIS_VALUES` (e.g. uus-shaped or `{topic_domain, signal_type}`) → `resolve_pack` SUCCESS; `ctx.taxonomy.axes` matches file.
- [x] **AC-GW-SSR31-02:** `canonical_keys` key for axis not in `axes[]` → `UnsupportedVersionError`; duplicate `axes[]` entry → error; `internal_axes` entry not in axes → error.
- [x] **AC-GW-SSR31-03:** Official `tallinn_civic/v1` still `resolve_pack` SUCCESS; seed test asserts data lockstep to reference 13 **as content**.
- [x] **AC-GW-SSR31-04:** Resolver Contour2 path does not call/compare `TAXONOMY_AXIS_VALUES` for accept/reject (grep-clean or unused import removed).
- [x] **AC-GW-SSR31-05:** Regression: legal/mobility without `taxonomy_schema` → `taxonomy is None`.

## DoD

- Pytest green for touched modules; ClusterLens still 10; no uus pack.json edit; arch-doc cited in PR/notes.

## Claims (Layer 2)

**As-of-Done:** Contour2 unlock + tests landed; G31 PASS 2026-09-04T12:55:28Z (pkg-000088).  
**Historical:** As-built lockstep and test paths verified 2026-09-04 against repo; implementation not started (pre-P3 claim).
