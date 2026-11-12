# task-gw-ssr-30-t01-tallinn-card-fields-mvp

## Task: data — tallinn MVP card_fields (T01)

## Meta
- **Story:** [STORY-GW-SSR-30](../STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md)
- **Type:** data
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000087
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-09-02T13:56:06Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md`

## Purpose
Add MVP `card_fields` allowlist to `schema-packs/tallinn_civic/v1/pack.json` only (3 M141 paths). Do not change legal/mobility; do not invent paths.

## Code Facts
1. **As-of-Done:** tallinn `pack.json` MVP `card_fields` three paths — `schema-packs/tallinn_civic/v1/pack.json`.
2. MVP paths exist in `field_policy` as `optional` (unchanged shape).
3. **Historical (pre-P3):** no `card_fields` key on tallinn.

## Gap
Absent allowlist ⇒ civic-only public Issues (no `schema_card` sidecar) for Tallinn.

## Acceptance / DoD
- [x] `pack.json` contains exactly the three MVP dotted paths (order as story)
- [x] No invent paths; no `geo.*`; no `canonical_type` / `civic_domain` / `failure_pattern` in allowlist
- [x] legal/mobility packs unchanged
- [x] No `field_policy` shape change; no SSR-11 code change
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json`

## Out of scope
Tests (→T02). Docs INDEX (→T03). Projection algorithm.
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
python3 -c "import json; d=json.load(open('doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json')); assert d['card_fields']==['signals.desired_outcome','signals.affected_group','signals.service_object']"
```
