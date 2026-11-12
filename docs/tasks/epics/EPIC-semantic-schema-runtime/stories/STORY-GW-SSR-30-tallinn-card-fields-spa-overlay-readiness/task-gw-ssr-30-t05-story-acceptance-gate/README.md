# task-gw-ssr-30-t05-story-acceptance-gate

## Task: analyze — story acceptance + G30 (T05)

## Meta
- **Story:** [STORY-GW-SSR-30](../STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000087
- **Skill declared:** python-pro
- **Depends on:** T00–T04 Done
- **Scaffolded:** 2026-09-02T13:56:06Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md`

## Purpose
Story acceptance gate G30. PASS iff AC-GW-SSR30-01…06. `resolve_pack(tallinn)` → `card_fields` == MVP tuple; ClusterLens=10; no HTTP invent. Do not backfill all Issues.

## Code Facts
- Template — story-acceptance-gate-template.md
- Story AC — backlog SSR-30 §Target / AC
- Mechanism — SSR-11 Done; declare-only this story

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-30.md` PASS/FAIL + evidence (P3)
- [x] `acceptance-verification-gw-ssr-30-t05.md` signed (Date post P3 live verify)
- [x] AC-GW-SSR30-01…06 covered
- [x] Live `--project gateway --verify` recorded
- [x] ClusterLens enum still 10; no new public HTTP
- [x] Do **not** rewrite §«Актуальная точка»
- [x] BULLRUN phases complete

## Where to change
- This folder gate artifacts (P3)

## Out of scope
P3 invent HTTP; historical reproject; SPA FE; SSR-11 redesign.
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
cd doge-complaints-gateway
python3 -c "from pathlib import Path; import sys; sys.path.insert(0,'src'); from core.schema.resolver import resolve_pack; ctx=resolve_pack(Path('schema-packs/tallinn_civic/v1')); assert list(ctx.card_fields)==['signals.desired_outcome','signals.affected_group','signals.service_object']"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
