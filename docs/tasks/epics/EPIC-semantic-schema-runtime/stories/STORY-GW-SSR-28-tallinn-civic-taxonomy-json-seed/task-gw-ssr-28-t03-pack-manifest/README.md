# task-gw-ssr-28-t03-pack-manifest

## Task: implement — taxonomy_schema in tallinn pack.json (T03)

## Meta
- **Story:** [STORY-GW-SSR-28](../STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000085
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-09-01T13:31:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md`

## Purpose
Add `"taxonomy_schema": "taxonomy.json"` to tallinn_civic/v1/pack.json only. After this, orphan-ignore ends — loader requires file.

## Code Facts
1. **As-of-Done (SSR-28 pkg-000085):** Tallinn [`pack.json`](../../../../../../../schema-packs/tallinn_civic/v1/pack.json) declares `"taxonomy_schema": "taxonomy.json"`; loader requires file; orphan-ignore ended.
2. legal/mobility remain without `taxonomy_schema` (taxonomy None).
3. **Historical (pre-P3 / P1 scaffold):** Tallinn pack had **no** `taxonomy_schema`; on-disk orphan `taxonomy.json` was ignored by SSR-26 loader.

## Acceptance / DoD
- [x] tallinn pack.json declares taxonomy_schema
- [x] legal/mobility unchanged (no taxonomy_schema)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json`

## Out of scope
legal/mobility manifests. GPT copy.
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
rg -n 'taxonomy_schema' doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json
rg -n 'taxonomy_schema' doge-complaints-gateway/schema-packs/legal_process/v1/pack.json doge-complaints-gateway/schema-packs/mobility_observation/v1/pack.json || true
```
