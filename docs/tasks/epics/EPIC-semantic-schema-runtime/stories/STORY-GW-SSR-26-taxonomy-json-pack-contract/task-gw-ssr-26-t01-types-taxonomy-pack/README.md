# task-gw-ssr-26-t01-types-taxonomy-pack

## Task: implement — TaxonomyPack on SchemaContext (T01)

## Meta
- **Story:** [STORY-GW-SSR-26](../STORY-GW-SSR-26-taxonomy-json-pack-contract.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000083
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-09-01T12:55:39Z
- **Completed:** 2026-09-01T13:00:37Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md`

## Purpose
Frozen dataclasses: `TaxonomyCanonicalKey(key, meaning=None)`; `TaxonomyPack(schema_id, schema_version, axes, internal_axes, canonical_keys, axis_to_signal_map, dispositions)`; extend `SchemaContext` with `taxonomy: TaxonomyPack | None = None`.

## Code Facts
1. **As-of-Done (SSR-26 pkg-000083):** `TaxonomyCanonicalKey` + `TaxonomyPack` — [`contracts.py:89–107`](../../../../../../../src/core/schema/contracts.py); `SchemaContext.taxonomy: TaxonomyPack | None = None` — [`:122`](../../../../../../../src/core/schema/contracts.py).
2. 13 axes SSOT unchanged — [`axes.py`](../../../../../../../src/core/taxonomy/axes.py) `TAXONOMY_AXIS_VALUES`.
3. Dispositions SSOT unchanged — [`disposition.py`](../../../../../../../src/core/taxonomy/disposition.py) `LABEL_DISPOSITION_VALUES`.
4. `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py).
5. **Historical (pre-P3 / P1 scaffold):** `SchemaContext` ended at `card_fields` — **no** `taxonomy` (`contracts.py:89–100` then).

## Acceptance / DoD
- [x] `TaxonomyCanonicalKey` + `TaxonomyPack` importable from `core.schema.contracts`
- [x] `SchemaContext.taxonomy: TaxonomyPack | None = None`
- [x] Не менять `TAXONOMY_AXIS_VALUES`; не трогать `ClusterLens`
- [x] pycompile / import clean
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/contracts.py`

## Out of scope
Change axes enum/tuple. ClusterLens. Loader wire (→T02).
- Overlay bans (every task):
  - **No tallinn seed** (SSR-28 owns official `taxonomy.json` + manifest key).
  - **No ClusterLens** add/remove. Enum stays 10 (`types.py:10–22`).
  - **No wire taxonomy** — `parse_taxonomy_payload` / GW-TAX-01 / `story_labels` untouched.
  - **No** replace `vocabulary.py` with pack read.
  - Orphan on-disk `taxonomy.json` **without** `taxonomy_schema` must **not** auto-load.
  - Loader optional at introduction; legal/mobility stay without taxonomy.
  - **Нет `GET /schema-active`.** Нет invent HTTP geo-filter. Нет IDX / `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет new SQL.
  - **Нет SSR-06/07/12.** Не reopen 01–25 product. Не стартовать 27/28/29 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
cd doge-complaints-gateway
python3 -c "from core.schema.contracts import TaxonomyPack, SchemaContext"
rg -n "TaxonomyPack|taxonomy" src/core/schema/contracts.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```
