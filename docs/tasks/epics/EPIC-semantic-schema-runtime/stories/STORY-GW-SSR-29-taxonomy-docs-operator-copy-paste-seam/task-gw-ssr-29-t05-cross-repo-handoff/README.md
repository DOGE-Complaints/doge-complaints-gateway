# task-gw-ssr-29-t05-cross-repo-handoff

## Task: docs — cross-repo handoff paths (T05)

## Meta
- **Story:** [STORY-GW-SSR-29](../STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000086
- **Skill declared:** python-pro
- **Depends on:** T01–T04
- **Scaffolded:** 2026-09-01T13:43:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md`

## Purpose
Document expected GPT-side files after operator copy (paths for GPT-SSR-05). Gateway SSOT ↔ GPT mirror table. Do **not** commit GPT JSON from gateway P3 without operator review.

## Code Facts
- Gateway SSOT — `schema-packs/tallinn_civic/v1/{pack,payload.schema,taxonomy}.json`
- GPT mirror — `GPT UI/instructions/schema-packs/tallinn_civic/v1/`
- Sibling — GPT-SSR-05 / GPT-SSR-09

## Acceptance / DoD
- [x] Path table published (pipeline story and/or manual handoff)
- [x] Explicit: gateway P3 does not edit GPT UI instructions / commit GPT JSON
- [x] BULLRUN phases complete

## Where to change
- pipeline story and/or manual §copy-paste
- optional one-line in `schema-packs/README.md`

## Out of scope
GPT-SSR-05 P3. spa/identity docs.
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
rg -n "GPT UI/instructions/schema-packs|GPT-SSR-05|byte-identical" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md | head
```
