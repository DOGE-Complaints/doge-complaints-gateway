# task-gw-ssr-30-t03-index-spa-docs-note

## Task: docs — INDEX + spa Declare note (T03)

## Meta
- **Story:** [STORY-GW-SSR-30](../STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000087
- **Skill declared:** python-pro
- **Depends on:** T01 (and preferably T02)
- **Scaffolded:** 2026-09-02T13:56:06Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md`

## Purpose
Update gateway INDEX row 30 status/progress for Declare package; add spa api-req note that Tallinn is Declare (not civic-only forever). Do **not** implement SPA overlay.

## Code Facts
1. **As-of-Done (SSR-30 pkg-000087):** INDEX row 30 **Done (Awaiting Commits)**; Progress SSR-30 Done — `backlog-stories/semantic-schema-runtime/INDEX.md`.
2. **As-of-Done:** spa-16 Tallinn Declare note for MVP `card_fields` — `spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md`.
3. Gap G-CARD-01 — cross-project analysis linked from story (context only).
4. **Historical (pre-P3 / P1 scaffold):** INDEX row 30 Todo (deep-spec ready); spa-16 still «tallinn may omit → civic-only».

## Gap
**Closed (P3):** INDEX + spa-16 Declare reflected. **Historical gap text:** «civic-only forever unless Declare reflected after pack mutate» — no longer live.

## Acceptance / DoD
- [x] INDEX row 30 / Progress reflects package state (Declare; not WAIVE)
- [x] spa api-req (or linked note) records Tallinn Declare for `card_fields`
- [x] No SPA overlay UI / typedef / map edits
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md`
- spa api-req note path from story Meta (sibling docs only — no spa-app product FE)

## Out of scope
SPA SSR-02 implementation. GPT byte-copy commit (→T04 paths only).
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
rg -n "SSR-30|card_fields|Declare" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
```
