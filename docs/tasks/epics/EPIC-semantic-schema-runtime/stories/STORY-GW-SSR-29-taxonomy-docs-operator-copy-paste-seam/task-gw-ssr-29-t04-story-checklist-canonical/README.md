# task-gw-ssr-29-t04-story-checklist-canonical

## Task: docs — story checklist canonical lockstep (T04)

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
Keep backlog story §Operator checklist as canonical; ensure manual mirrors steps 1–6 (no silent drift). Touch story only if wording must align with published manual.

## Code Facts
- Canonical — backlog [`STORY-GW-SSR-29-….md`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md) §Operator checklist
- Manual consumer — T01

## Acceptance / DoD
- [x] Story steps 1–6 match manual operator §
- [x] Deprecation policy present in both
- [x] BULLRUN phases complete

## Where to change
- backlog story SSR-29 (align only if needed)
- manual (via T01)

## Out of scope
Performing GPT copy. CI shasum automation story.
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
rg -n "Edit SSOT|byte-identical|shasum|inbound-validation" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
