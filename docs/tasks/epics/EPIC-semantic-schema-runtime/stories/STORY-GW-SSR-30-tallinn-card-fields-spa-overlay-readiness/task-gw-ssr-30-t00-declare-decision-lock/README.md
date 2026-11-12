# task-gw-ssr-30-t00-declare-decision-lock

## Task: docs — Declare decision lock (T00)

## Meta
- **Story:** [STORY-GW-SSR-30](../STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000087
- **Skill declared:** python-pro
- **Depends on:** SSR-11 Done; operator Declare 2026-09-02
- **Scaffolded:** 2026-09-02T13:56:06Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md`

## Purpose
Record **Declare** locked in pipeline Meta + INDEX hygiene note: WAIVE N/A. Do not re-open WAIVE without operator.

## Code Facts
1. **As-of-Done (SSR-30 pkg-000087):** Declare locked in pipeline Meta + INDEX; WAIVE N/A.
2. Backlog Meta Operator 2026-09-02 Declare — `$storyFile`.
3. **Historical (pre-P3):** tallinn `pack.json` had no `card_fields`.

## Gap
Decision must stay Declare-locked in pipeline story Meta before pack mutate (T01).

## Acceptance / DoD
- [x] Pipeline story Meta states Declare locked; WAIVE N/A
- [x] INDEX still reflects Declare (not WAIVE) for row 30
- [x] No product pack/src edits in T00
- [x] BULLRUN phases complete when closed

## Where to change
- Pipeline story Meta / Status notes
- Optional INDEX Status wording (Declare lock only; Done → T03)

## Out of scope
Pack JSON mutate (→T01). SPA FE. SSR-11 redesign.
- Overlay bans (every task):
  - **Declare only** MVP three paths in tallinn `pack.json` — no invent paths.
  - **No** SSR-11 redesign; **no** `field_policy` `show_on_card`.
  - **No** SPA FE / spa-app product in this pkg.
  - **No** legal/mobility `card_fields` seed.
  - **No ClusterLens** add/remove. Enum stays 10.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - No GPT UI materialize without operator review (T04 handoff paths only).
  - Do not reopen 01–29 product.

## Verification commands
```bash
rg -n "Declare|WAIVE" doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
```
