# task-gw-ssr-28-t02-compose-taxonomy-json

## Task: implement — write tallinn_civic/v1/taxonomy.json (T02)

## Meta
- **Story:** [STORY-GW-SSR-28](../STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000085
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-01T13:31:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md`

## Purpose
Materialize `schema-packs/tallinn_civic/v1/taxonomy.json` per SSR-26 shape from T01 inventory. `schema_id`/`schema_version` match pack. Valid JSON UTF-8 trailing newline. ~170–190 keys order-of-magnitude (not hard AC).

## Code Facts
1. **As-of-Done (SSR-28 pkg-000085):** Official seed — [`taxonomy.json`](../../../../../../../schema-packs/tallinn_civic/v1/taxonomy.json) · `schema_id`/`schema_version` tallinn_civic/v1 · 13 axes · 182 keys · regenerated from GPT §4/§5/§6 via [`ssr28_gpt_taxonomy_extract.py`](../../../../../../../tests/helpers/ssr28_gpt_taxonomy_extract.py).
2. Shape lockstep — SSR-26 `TaxonomyPack` / README taxonomy.json blocks; dispositions five; `axis_to_signal_map` covers required signals.
3. **Historical (pre-P3 / P1 scaffold):** WIP orphan file may exist on disk — **not** Done until regenerate from SSOT + T03 manifest wire; do not invent keys.

## Acceptance / DoD
- [x] File exists; json.load OK; trailing newline
- [x] schema_id/schema_version = tallinn_civic / v1
- [x] 13 axes; internal_axes = risk_privacy_safety + confidence_state
- [x] dispositions five values; axis_to_signal_map covers required signals (min topic_domain + failure_mode)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/tallinn_civic/v1/taxonomy.json`

## Out of scope
Manifest key (→T03). legal/mobility seeds.
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
python3 -c "import json; p='doge-complaints-gateway/schema-packs/tallinn_civic/v1/taxonomy.json'; d=json.load(open(p)); print(d['schema_id'], len(d['axes']), sum(len(v) for v in d['canonical_keys'].values()))"
```
