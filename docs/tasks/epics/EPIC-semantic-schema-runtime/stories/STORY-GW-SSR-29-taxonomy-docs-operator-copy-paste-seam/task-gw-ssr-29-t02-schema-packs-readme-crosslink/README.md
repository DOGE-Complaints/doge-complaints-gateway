# task-gw-ssr-29-t02-schema-packs-readme-crosslink

## Task: docs — schema-packs README cross-link (T02)

## Meta
- **Story:** [STORY-GW-SSR-29](../STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000086
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-01T13:43:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md`

## Purpose
After SSR-26 T00 tables, add cross-link from `schema-packs/README.md` to manual §taxonomy / operator copy-paste. Replace SSR-29 placeholder wording. No second full shape table.

## Code Facts
1. **As-of-Done (SSR-29 pkg-000086):** [`schema-packs/README.md`](../../../../../../../schema-packs/README.md) cross-links manual §Taxonomy dual contour / §Operator copy-paste (SSR-29); no second shape table.
2. Manual target — `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`.
3. **Historical (pre-P3 / P1 scaffold):** README had taxonomy_schema + SSR-28 seed; SSR-29 still **placeholder**.

## Acceptance / DoD
- [x] Cross-link to manual taxonomy / copy-paste section resolves
- [x] No duplicate SSR-26 taxonomy.json shape tables
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/README.md`

## Out of scope
Manual body (→T01). GPT UI README (operator step 4 / GPT-SSR-05).
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
rg -n "schema-packs-node-data-model-ru|copy-paste|SSR-29" doge-complaints-gateway/schema-packs/README.md
```
