# Story acceptance gate — STORY-GW-SSR-31

- **Story:** Contour2 node-specific taxonomy axes
- **Package:** `pkg-000088-20260904-gw-ssr-31-node-specific-contour2-taxonomy-axes.yaml`
- **Result:** PASS
- **Date:** 2026-09-04T12:55:28Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR31-01: ≠13 structurally valid pack loads | PASS | SSR-26 node-defined 2-axis + SSR-31 uus-shaped 24-axis |
| AC-GW-SSR31-02: structural rejects unchanged | PASS | canonical_keys axis ∉ axes; duplicate axis; (SSR-26 suite) |
| AC-GW-SSR31-03: tallinn seed still loads; content 13 | PASS | `test_gw_ssr_28_*` seed content + resolve |
| AC-GW-SSR31-04: Contour2 no TAXONOMY_AXIS_VALUES accept/reject | PASS | `rg TAXONOMY_AXIS_VALUES resolver.py` empty |
| AC-GW-SSR31-05: legal/mobility taxonomy None | PASS | SSR-26 + SSR-31 tests |

## Commands (live verification — P3)

```text
--verify ok 5 (pkg-000088) + ok date-check
utc_now: 2026-09-04T12:55:28Z
.venv/bin/python -m pytest -q tests/test_gw_ssr_26_taxonomy_loader.py tests/test_gw_ssr_28_taxonomy_seed.py tests/test_gw_ssr_31_node_taxonomy_contour2.py
→ 20 passed
ClusterLens=10; no Contour1/docs/uus pack.json; §Актуальная точка not rewritten
```
