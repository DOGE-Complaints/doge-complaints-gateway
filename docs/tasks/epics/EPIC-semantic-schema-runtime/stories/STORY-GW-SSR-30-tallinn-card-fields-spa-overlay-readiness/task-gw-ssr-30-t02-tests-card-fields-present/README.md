# task-gw-ssr-30-t02-tests-card-fields-present

## Task: tests — tallinn card_fields present (T02)

## Meta
- **Story:** [STORY-GW-SSR-30](../STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000087
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-02T13:56:06Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md`

## Purpose
Flip `test_tallinn_civic_absent_card_fields_is_civic_form` → expect present MVP list; optional `test_gw_ssr_30_*` load + `project_card_fields` smoke. Do **not** change `project_card_fields` logic.

## Code Facts
1. **As-of-Done:** `test_tallinn_civic_mvp_card_fields_present` + `tests/test_gw_ssr_30_tallinn_card_fields.py`.
2. SSR-11 projection tests unchanged algorithm — `tests/test_gw_ssr_11_*`.
3. **Historical:** `test_tallinn_civic_absent_card_fields_is_civic_form` asserted empty allowlist.

## Gap
After T01, absent-key test becomes stale and must flip to present MVP.

## Acceptance / DoD
- [x] Absent-key tallinn test updated (or replaced) to expect non-empty MVP `card_fields`
- [x] Optional `test_gw_ssr_30_*` smoke: resolve_pack + project_card_fields for MVP paths
- [x] No edits to `src/core/projection/card_fields.py` algorithm
- [x] Targeted pytest green
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/` (existing tallinn civic card_fields test + optional `test_gw_ssr_30_*.py`)

## Out of scope
SSR-11 redesign. Historical Issue backfill. SPA FE.
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
cd doge-complaints-gateway && python -m pytest -q tests/ -k "ssr_30 or tallinn_civic.*card_fields or card_fields" --tb=short
```
