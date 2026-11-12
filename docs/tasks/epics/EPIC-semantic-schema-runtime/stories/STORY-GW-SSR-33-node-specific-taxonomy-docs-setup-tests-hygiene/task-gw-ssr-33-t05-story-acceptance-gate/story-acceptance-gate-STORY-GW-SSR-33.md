# Story acceptance gate — STORY-GW-SSR-33

- **Story:** Node-specific taxonomy docs / setup / usage / test hygiene
- **Package:** `pkg-000090-20260904-gw-ssr-33-node-specific-taxonomy-docs-setup-tests-hygiene.yaml`
- **Result:** PASS
- **Date:** 2026-09-04T13:28:42Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR33-01: README axes node-defined; no lockstep-to-13 | PASS | `schema-packs/README.md` axes row: Node-defined (D-SSR-11 / SSR-31); «must equal all 13» only as negated phrase; tallinn exemplar |
| AC-GW-SSR33-02: Manual dual contour + setup 1–6 | PASS | `schema-packs-node-data-model-ru.md` §Taxonomy dual contour (D-SSR-11) + §Authoring node taxonomy steps 1–6 + GPT-SSR-15 invert note |
| AC-GW-SSR33-03: INDEX + test inventory 31/32/33 | PASS | `INDEX.md` node-taxonomy section + test inventory table; status Done pkg-000090 |
| AC-GW-SSR33-04: GPT-SSR-15 invert handoff recorded | PASS | INDEX sibling handoff + manual note; **no** GPT file edit |
| AC-GW-SSR33-05: uus gap handoff As-of-Done | PASS | `uus-veerenni-…-2026-09-04.md`: taxonomy lockstep **obsolete**; Contour2/1 As-of-Done; remaining blockers civic/exact |

## Commands (live verification — P3)

```text
--verify ok 5 (pkg-000090)
utc_now: 2026-09-04T13:28:42Z
rg "must equal all 13" schema-packs/README.md → only negated in node-defined axes row
No resolver.py / axes.py / ClusterLens product edits in this story
§Актуальная точка not rewritten; push=no; branch=semantic-schema-runtime
```
