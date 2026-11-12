# task-gw-ssr-29-t01-manual-taxonomy-copy-paste

## Task: docs — manual taxonomy dual contour + copy-paste (T01)

## Meta
- **Story:** [STORY-GW-SSR-29](../STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000086
- **Skill declared:** python-pro
- **Depends on:** SSR-26 + SSR-28 Done
- **Scaffolded:** 2026-09-01T13:43:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md`

## Purpose
Edit `schema-packs-node-data-model-ru.md`: 3-file pack layout; §taxonomy dual contour; §operator copy-paste steps 1–6; §Как добавить модель optional taxonomy.json; deprecation note for GPT `story-label-taxonomy.md` as SSOT when JSON copied. Coexist with SSR-27 geo §. No full manual rewrite; no SSR-26 shape-table dump.

## Code Facts
1. **As-of-Done (SSR-29 pkg-000086):** Manual documents 3-file layout (`taxonomy.json` when `taxonomy_schema` set), §Taxonomy dual contour, §Operator copy-paste 1–6, deprecation — [`schema-packs-node-data-model-ru.md`](../../../../../../../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md). Coexists with §Три уровня geo (SSR-27).
2. Dual contour / checklist SSOT — backlog SSR-29; tallinn seed paths — `schema-packs/tallinn_civic/v1/`.
3. **Historical (pre-P3 / P1 scaffold):** Manual §Три пака / §Как добавить still **2-file layout prose**; no taxonomy §.

## Acceptance / DoD
- [x] Pack layout shows pack.json + payload.schema.json + taxonomy.json (when taxonomy_schema set)
- [x] Dual contour table (wire vs pack taxonomy vs payload vs inbound)
- [x] Operator copy-paste steps 1–6 + byte-identical + shasum example
- [x] Deprecation note: GPT story-label-taxonomy.md no longer SSOT for keys after JSON copy
- [x] Grep gate: taxonomy.json, dual contour, byte-identical
- [x] No wire/GW-TAX-01 behavior-change claim
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`

## Out of scope
GPT operator manual rewrite (GPT-SSR-09). README cross-link (→T02). INDEX Done (→T03).
- Overlay bans (every task):
  - **Docs-only** — no `src/` / loader / pack JSON product edits (SSR-26/28 Done).
  - **No** GPT UI materialize / byte-copy commit in this pkg (checklist + paths only).
  - **No** claim that wire envelope or GW-TAX-01 behavior changes.
  - **No** duplicate SSR-26 README shape tables in manual — link instead.
  - **No** mark INDEX taxonomy wave Done before builder package Done.
  - Stay `semantic-schema-runtime`. Не переписывать bullrun §«Актуальная точка».
  - Merge with SSR-27 geo § without contradictory layout bullets.
  - No SSR-06/07/12 invent. Do not reopen 01–28 product.
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "taxonomy\.json|dual contour|byte-identical|story-label-taxonomy" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
