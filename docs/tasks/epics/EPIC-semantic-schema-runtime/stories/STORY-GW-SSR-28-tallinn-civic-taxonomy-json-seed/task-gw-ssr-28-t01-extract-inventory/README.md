# task-gw-ssr-28-t01-extract-inventory

## Task: implement — extract GPT §4/§5/§6 key inventory (T01)

## Meta
- **Story:** [STORY-GW-SSR-28](../STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000085
- **Skill declared:** python-pro
- **Depends on:** SSR-26 Done (loader)
- **Scaffolded:** 2026-09-01T13:31:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md`

## Purpose
Section-scoped extract from GPT `story-label-taxonomy.md` §4+§5+§6 → per-axis canonical key sets. Diff overlap vs `vocabulary.py` (`topic_domain`, `failure_mode`). Gate: inventory test matches GPT §4. No invent; no §7 disposition tokens as keys.

## Code Facts
- GPT SSOT — [`story-label-taxonomy.md`](../../../../../../../../GPT%20UI/instructions/story-label-taxonomy.md)
- Axes lockstep — [`axes.py`](../../../../../../../src/core/taxonomy/axes.py)
- Vocab overlap — [`vocabulary.py`](../../../../../../../src/core/cluster/vocabulary.py)
- Story extraction algorithm — backlog SSR-28 §T01

## Acceptance / DoD
- [x] Section-scoped parser / inventory (script or test helper) for §4/§5/§6
- [x] Overlap axes subset check vs vocabulary frozensets prepared
- [x] HARD STOP path if §4 key missing vs prior export (documented in test)
- [x] Do not parse §7 into canonical_keys
- [x] BULLRUN phases complete

## Where to change
- helper under `tests/` or `scripts/` + used by T04; inventory assertions

## Out of scope
Compose final taxonomy.json (→T02). Manifest (→T03).
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
rg -n "canonical_keys_inventory|story-label-taxonomy" doge-complaints-gateway/tests/test_gw_ssr_28_*.py
```
