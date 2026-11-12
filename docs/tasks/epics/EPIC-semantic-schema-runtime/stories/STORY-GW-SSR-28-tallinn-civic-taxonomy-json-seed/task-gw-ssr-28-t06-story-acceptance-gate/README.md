# task-gw-ssr-28-t06-story-acceptance-gate

## Task: analyze — story acceptance + G28 (T06)

## Meta
- **Story:** [STORY-GW-SSR-28](../STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000085
- **Skill declared:** python-pro
- **Depends on:** T01–T05 Done
- **Scaffolded:** 2026-09-01T13:31:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md`

## Purpose
Story acceptance gate. PASS iff AC-GW-SSR28-01…06. ClusterLens=10; no invent vocabulary; legal/mobility still taxonomy None.

## Code Facts
- Template — story-acceptance-gate-template.md
- Story AC — backlog SSR-28 §Target / AC
- SSR-26 tests — `tests/test_gw_ssr_26_*`

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-28.md` PASS/FAIL + evidence (P3)
- [x] `acceptance-verification-gw-ssr-28-t06.md` signed (Date post P3)
- [x] AC-GW-SSR28-01…06 covered
- [x] Live `--project gateway --verify` recorded
- [x] Do **not** rewrite §«Актуальная точка»; do not start SSR-29
- [x] BULLRUN phases complete

## Where to change
- This folder gate artifacts (P3)

## Out of scope
P3 product gaps invent; start SSR-29
- Overlay bans (every task):
  - **No invent** taxonomy vocabulary — extract only from GPT `story-label-taxonomy.md` §4/§5/§6 + axes/disposition lockstep.
  - **No ClusterLens** add/remove. Enum stays 10.
  - **No** legal/mobility `taxonomy_schema` / taxonomy.json seed.
  - **No** silent renames vs GPT §4.
  - **No** GPT UI materialize / GPT-SSR-05 copy in this pkg.
  - Orphan `taxonomy.json` without manifest = **not** Done.
  - Stay `semantic-schema-runtime`. Не переписывать bullrun §«Актуальная точка».
  - No SSR-06/07/12. Do not start SSR-29 product. Do not reopen 01–27.
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
cd doge-complaints-gateway
.venv/bin/python -m pytest -q tests/test_gw_ssr_28_*.py tests/test_gw_ssr_26_*.py
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
