# task-gw-ssr-29-t03-gateway-index-hygiene

## Task: docs — gateway INDEX taxonomy wave hygiene (T03)

## Meta
- **Story:** [STORY-GW-SSR-29](../STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000086
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-09-01T13:43:47Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md`

## Purpose
Update `backlog-stories/semantic-schema-runtime/INDEX.md`: taxonomy-pack table 26/28/29 + GPT-SSR-05/06/09 + gap analysis cross-links. Progress line → Done **only when package executes** (not at P1 scaffold).

## Code Facts
1. **As-of-Done (SSR-29 pkg-000086):** [`INDEX.md`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) taxonomy-pack 26/28/29 **Done (Awaiting Commits)**; Progress **3/3**; GPT-SSR-05/06/09 + G-TAX-01 siblings.
2. **Historical (pre-P3 / P1 scaffold):** INDEX row 29 Todo; Progress SSR-29 Todo — do not mark Done while package incomplete.

## Acceptance / DoD
- [x] Wave table links GPT siblings + gap analysis
- [x] Progress / status Done only at package completion (P3 gate), not P1
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md`

## Out of scope
Root backlog INDEX invent. Bullrun §Актуальная точка.
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
rg -n "SSR-29|GPT-SSR-05|taxonomy-pack" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
```
