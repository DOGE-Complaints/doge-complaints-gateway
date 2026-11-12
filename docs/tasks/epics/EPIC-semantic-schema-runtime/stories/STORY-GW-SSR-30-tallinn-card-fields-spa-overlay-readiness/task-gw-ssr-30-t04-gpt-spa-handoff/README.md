# task-gw-ssr-30-t04-gpt-spa-handoff

## Task: docs — GPT pack.json + SPA L10N handoff (T04)

## Meta
- **Story:** [STORY-GW-SSR-30](../STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000087
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-02T13:56:06Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md`

## Purpose
Document operator copy of updated tallinn `pack.json` → GPT `instructions/schema-packs/tallinn_civic/v1/` (SSR-29 checklist); list SPA L10N ids for MVP paths. Do **not** commit GPT without operator review.

## Code Facts
1. SSR-29 operator copy-paste seam — manual + schema-packs README.
2. SPA L10N pattern — `schemaRuntime.cardField.<dotted-path>` (story Architecture / Pitfalls).
3. MVP paths — `signals.desired_outcome` / `affected_group` / `service_object`.

## Gap
After pack Declare, GPT SSOT copy and SPA label keys must be listed for siblings — not executed blindly in gateway P3.

## Acceptance / DoD
- [x] Handoff note lists gateway → GPT `pack.json` path + byte-copy reminder (SSR-29)
- [x] L10N id list for three MVP paths documented
- [x] No GPT UI tree materialize / commit in this pkg without operator
- [x] BULLRUN phases complete when closed

## Where to change
- Pipeline story handoff section and/or schema-packs README note / run-summary (P3)
- Optional link from SSR-29 manual checklist (paths only)

## Out of scope
GPT UI commit. SPA overlay FE. Invent L10N beyond listed paths.
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
rg -n "cardField\.signals\.(desired_outcome|affected_group|service_object)|tallinn_civic/v1/pack\.json" doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness/
```
