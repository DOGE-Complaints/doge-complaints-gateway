# task-gw-ssr-29-t06-story-acceptance-gate

## Task: analyze — story acceptance + G29 (T06)

## Meta
- **Story:** [STORY-GW-SSR-29](../STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000086
- **Skill declared:** python-pro
- **Depends on:** T01–T05 Done
- **Scaffolded:** 2026-09-01T13:43:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md`

## Purpose
Story acceptance gate. PASS iff AC-GW-SSR29-01…06. Docs-only; no wire/GW-TAX-01 behavior-change claim; geo§ + taxonomy§ coexist; INDEX Done only with package.

## Code Facts
- Template — story-acceptance-gate-template.md
- Story AC — backlog SSR-29 §Target / AC
- SSR-27 geo § already in manual — coexistence check

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-29.md` PASS/FAIL + evidence (P3)
- [x] `acceptance-verification-gw-ssr-29-t06.md` signed (Date post P3)
- [x] AC-GW-SSR29-01…06 covered
- [x] Live `--project gateway --verify` recorded
- [x] Do **not** rewrite §«Актуальная точка»
- [x] BULLRUN phases complete

## Where to change
- This folder gate artifacts (P3)

## Out of scope
P3 product invent; GPT copy execution
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
cd doge-complaints-gateway
rg -n "taxonomy\.json|dual contour|byte-identical|GPT-SSR-05" docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md schema-packs/README.md docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
