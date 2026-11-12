# Story acceptance gate — STORY-GW-SSR-29

- **Story:** taxonomy docs + operator copy-paste seam
- **Package:** `pkg-000086-20260901-gw-ssr-29-taxonomy-docs-operator-copy-paste-seam.yaml`
- **Result:** PASS
- **Date:** 2026-09-01T13:49:03Z

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR29-01: three-file layout + dual contour | PASS | manual §Три пака layout + §Taxonomy dual contour |
| AC-GW-SSR29-02: checklist in manual **and** story | PASS | manual §Operator copy-paste 1–6; backlog §Operator checklist |
| AC-GW-SSR29-03: INDEX links GPT-SSR-05 + wave 26/28/29 | PASS | `INDEX.md` taxonomy-pack table + Siblings + Progress 3/3 |
| AC-GW-SSR29-04: deprecation note story-label-taxonomy.md | PASS | manual + backlog deprecation policy |
| AC-GW-SSR29-05: no wire/GW-TAX-01 behavior-change claim | PASS | dual contour prose; «Не делать… GW-TAX-01»; no «wire taxonomy moved to payload» |
| AC-GW-SSR29-06: geo § + taxonomy § coexist | PASS | §Три уровня geo + §Taxonomy dual contour in same manual |

## Commands (live verification — P3 only)

```text
--verify ok 6 (pkg-000086) + ok date-check
utc_now: 2026-09-01T13:49:03Z
rg taxonomy.json|dual contour|byte-identical → manual green
rg "wire taxonomy moved to payload" → empty
docs-only: no src/ edits; no GPT UI materialize
§Актуальная точка not rewritten
```
