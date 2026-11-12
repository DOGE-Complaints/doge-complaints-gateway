# Story acceptance gate — STORY-GW-SSR-26

- **Story:** taxonomy.json pack contract + loader
- **Package:** `pkg-000083-20260901-gw-ssr-26-taxonomy-json-pack-contract.yaml`
- **Result:** PASS
- **Date:** 2026-09-01T13:00:37Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR26-01: README documents `taxonomy_schema` + `taxonomy.json` | PASS | `schema-packs/README.md` layout + key table + blocks |
| AC-GW-SSR26-02: Loader exposes taxonomy on `SchemaContext` when declared | PASS | `_parse_taxonomy_pack` + `load_pack` wire; `test_declared_taxonomy_loads_when_valid` |
| AC-GW-SSR26-03: legal/mobility load with `taxonomy is None` | PASS | `test_legal_and_mobility_load_without_taxonomy` |
| AC-GW-SSR26-04: Invalid / duplicate → loader error (test-backed) | PASS | `test_invalid_axis_*` + `test_duplicate_canonical_key_fails` + missing-file |
| AC-GW-SSR26-05: ClusterLens + GW-TAX-01 wire unchanged | PASS | `len(ClusterLens)==10`; no edits to `vocabulary.py` / `parse_taxonomy_payload` callers beyond load |

## Commands (live verification — P3 only)

```text
--verify ok 6 (pkg-000083)
utc_now: 2026-09-01T13:00:37Z
pytest -q tests/test_gw_ssr_26_*.py → 6 passed
pytest -q tests/test_gw_ssr_01_*.py tests/test_gw_ssr_11_*.py → 36 passed
combined SSR-26+01+11 → 42 passed
ClusterLens → 10
rg taxonomy_schema|taxonomy.json → schema-packs/README.md
orphan tallinn taxonomy.json without taxonomy_schema → taxonomy is None
```
