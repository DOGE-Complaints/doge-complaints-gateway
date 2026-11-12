# task-gw-ssr-26-t00-contract-readme

## Task: add — document taxonomy_schema + taxonomy.json (T00)

## Meta
- **Story:** [STORY-GW-SSR-26](../STORY-GW-SSR-26-taxonomy-json-pack-contract.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000083
- **Skill declared:** python-pro
- **Depends on:** SSR-25 Done (G25)
- **Scaffolded:** 2026-09-01T12:55:39Z
- **Completed:** 2026-09-01T13:00:37Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md`

## Purpose
Зафиксировать layout 3 файла + таблицу `taxonomy_schema` + блоки `taxonomy.json` в `schema-packs/README.md`. Cross-link manual placeholder до SSR-29. Не frozen YAML dialect; не дублировать полный manual.

## Code Facts
1. **As-of-Done (SSR-26 pkg-000083):** README documents layout 3 files + `taxonomy_schema` + `taxonomy.json` blocks — [`schema-packs/README.md:11`](../../../../../../../schema-packs/README.md), [`:33`](../../../../../../../schema-packs/README.md), [`:35–46`](../../../../../../../schema-packs/README.md).
2. Orphan `taxonomy.json` may exist without manifest key — [`tallinn_civic/v1/taxonomy.json`](../../../../../../../schema-packs/tallinn_civic/v1/taxonomy.json); still **not** auto-loaded (no `taxonomy_schema` in pack.json).
3. **Historical (pre-P3 / P1 scaffold):** README had **no** `taxonomy` / `taxonomy_schema` (rg empty); layout documented 2 files only.
4. Story T00 — backlog [`STORY-GW-SSR-26-….md`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md) §T00.

## Acceptance / DoD
- [x] `schema-packs/README.md` documents layout including `taxonomy.json`
- [x] Table / key `taxonomy_schema` present
- [x] Blocks of `taxonomy.json` summarized; placeholder cross-link for SSR-29 manual
- [x] Not: frozen YAML dialect; not full manual duplicate
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/README.md`

## Out of scope
Frozen YAML dialect invent. Tallinn seed (→28). Full taxonomy manual (→29).
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
rg -n "taxonomy_schema|taxonomy\.json" doge-complaints-gateway/schema-packs/README.md
```
