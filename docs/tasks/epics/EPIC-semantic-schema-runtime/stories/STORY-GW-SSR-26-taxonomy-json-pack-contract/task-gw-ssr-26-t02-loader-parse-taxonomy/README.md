# task-gw-ssr-26-t02-loader-parse-taxonomy

## Task: implement — _parse_taxonomy_pack + load_pack wire (T02)

## Meta
- **Story:** [STORY-GW-SSR-26](../STORY-GW-SSR-26-taxonomy-json-pack-contract.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000083
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-01T12:55:39Z
- **Completed:** 2026-09-01T13:00:37Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md`

## Purpose
Реализовать `_parse_taxonomy_pack(pack_dir, manifest, expected)`: absent `taxonomy_schema` → `None`; present → require file; validate identity, axes lockstep (= all 13), internal_axes ⊆ axes, canonical_keys (no dup), axis_to_signal_map, dispositions. Wire in `load_pack()` after `card_fields`. Pattern: optional like `_parse_card_fields`; filename indirection like `payload_schema`.

## Code Facts
1. **As-of-Done (SSR-26 pkg-000083):** `_parse_taxonomy_pack` — [`resolver.py:250–412`](../../../../../../../src/core/schema/resolver.py); wired in `load_pack` — [`:515`](../../../../../../../src/core/schema/resolver.py) `taxonomy=_parse_taxonomy_pack(...)`.
2. Optional parse patterns still used — `_parse_dual_civic_lenses` / `_parse_card_fields`; absent `taxonomy_schema` → `None` (orphan file ignored).
3. Missing/invalid → `UnsupportedVersionError` — [`errors.py`](../../../../../../../src/core/schema/errors.py).
4. Imports: `TAXONOMY_AXIS_VALUES`, `LABEL_DISPOSITION_VALUES`.
5. **Historical (pre-P3 / P1 scaffold):** `load_pack` ended dual + `card_fields` only (`resolver.py:344–345` then); no taxonomy wire.

## Acceptance / DoD
- [x] `taxonomy_schema` absent → `ctx.taxonomy is None`
- [x] Present + missing file → `UnsupportedVersionError` (message includes taxonomy file missing)
- [x] Axes/identity/dup validation fail-fast
- [x] `resolve_pack(SchemaRef("legal_process","v1"))` behavior unchanged (taxonomy None)
- [x] Orphan file without manifest key does **not** auto-load
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/resolver.py`

## Out of scope
Tallinn official seed/manifest key (→28). Wire taxonomy path. ClusterLens.
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
rg -n "_parse_taxonomy_pack|taxonomy_schema|taxonomy=" doge-complaints-gateway/src/core/schema/resolver.py
cd doge-complaints-gateway && python3 -c "from core.schema.resolver import resolve_pack; from core.schema.contracts import SchemaRef; c=resolve_pack(SchemaRef('legal_process','v1')); assert c.taxonomy is None"
```
