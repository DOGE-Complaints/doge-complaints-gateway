# Story acceptance gate — STORY-GW-SSR-32

- **Story:** Contour1 wire taxonomy axes
- **Package:** `pkg-000089-20260904-gw-ssr-32-node-specific-contour1-wire-axes.yaml`
- **Result:** PASS
- **Date:** 2026-09-04T13:13:31Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR32-01: custom axis on wire accepted | PASS | `test_parse_taxonomy_payload_accepts_custom_axis`; `test_intake_accepts_custom_axis_on_wire` |
| AC-GW-SSR32-02: empty / non-string axis rejected | PASS | `test_normalize_axis_rejects_empty_and_non_string`; `test_intake_rejects_blank_axis` |
| AC-GW-SSR32-03: unmapped axis civic skip intact | PASS | `test_civic_skip_unmapped_axes_no_invented_dimension` |
| AC-GW-SSR32-04: classic 13-axis wire still passes | PASS | `test_classic_thirteen_axis_wire_still_parses` |

## Commands (live verification — P3)

```text
--verify ok 4 (pkg-000089)
utc_now: 2026-09-04T13:13:31Z
.venv/bin/python -m pytest -q tests/test_gw_ssr_32_contour1_wire_axes.py
→ 9 passed
rg Unsupported taxonomy axis axes.py → empty
ClusterLens=10; no Contour2/docs/vocabulary expand; §Актуальная точка not rewritten
```
