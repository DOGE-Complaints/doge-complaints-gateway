# Story acceptance gate — STORY-GW-SSR-30

- **Story:** tallinn card_fields / SPA overlay readiness
- **Package:** `pkg-000087-20260902-gw-ssr-30-tallinn-card-fields-spa-overlay-readiness.yaml`
- **Result:** PASS
- **Date:** 2026-09-02T14:00:46Z

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR30-01: Declare recorded; WAIVE N/A | PASS | pipeline Meta Declare locked; INDEX row 30 Done (Awaiting Commits) |
| AC-GW-SSR30-02: tallinn MVP `card_fields` three paths; policy not forbidden/node_private | PASS | `pack.json` + `field_policy` optional for all three |
| AC-GW-SSR30-03: loader non-empty `card_fields`; schema_card MAY when leaves resolve | PASS | `resolve_pack` MVP tuple; `project_card_fields` smoke; SSR-11 unchanged |
| AC-GW-SSR30-04: N/A (WAIVE cancelled) | PASS | N/A |
| AC-GW-SSR30-05: no new public HTTP; no payload dump; no field_policy shape change | PASS | no src projection edits; ClusterLens=10 |
| AC-GW-SSR30-06: residuals documented | PASS | pipeline As-of-Done + README SSR-30 handoff |

## Commands (live verification — P3 only)

```text
--verify ok 6 (pkg-000087) + ok date-check
utc_now: 2026-09-02T14:00:46Z
resolve_pack tallinn card_fields == MVP tuple; ClusterLens=10
.venv/bin/python -m pytest -q tests/test_gw_ssr_30_tallinn_card_fields.py tests/test_gw_ssr_11_card_fields_loader.py → 9 passed
§Актуальная точка not rewritten
pkg-000087 YAML immutable
```
