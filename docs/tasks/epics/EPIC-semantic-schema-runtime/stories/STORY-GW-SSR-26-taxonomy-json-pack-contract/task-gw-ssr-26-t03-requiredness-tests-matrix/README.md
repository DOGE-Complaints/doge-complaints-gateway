# task-gw-ssr-26-t03-requiredness-tests-matrix

## Task: tests — requiredness / invalid axis / duplicate key matrix (T03)

## Meta
- **Story:** [STORY-GW-SSR-26](../STORY-GW-SSR-26-taxonomy-json-pack-contract.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000083
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-09-01T12:55:39Z
- **Completed:** 2026-09-01T13:00:37Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md`

## Purpose
Закрыть matrix из story T03 через tmp_path / copied pack fragments (pattern `test_gw_ssr_11_card_fields_loader.py`): legal/mobility → None; manifest declares + file missing → error; invalid axis → unknown axis; duplicate canonical key → duplicate key. **Не** seed tallinn official tree.

## Code Facts
- Story matrix — backlog SSR-26 §T03
- Pattern tmp_path — [`tests/test_gw_ssr_11_card_fields_loader.py`](../../../../../../../tests/test_gw_ssr_11_card_fields_loader.py)
- Official packs have no `taxonomy_schema` — `schema-packs/*/v1/pack.json` (rg empty)
- Orphan tallinn taxonomy.json exists but must not auto-load without manifest key

## Acceptance / DoD
- [x] legal/mobility load → `taxonomy is None`
- [x] declared + missing file → `UnsupportedVersionError` match `taxonomy file missing`
- [x] invalid axis → match `unknown axis`
- [x] duplicate canonical key → match `duplicate key`
- [x] No official tallinn seed in this task
- [x] BULLRUN phases complete

## Where to change
- Cases may land in `tests/test_gw_ssr_26_taxonomy_loader.py` (shared with T04) or helpers; T04 owns file creation if not yet present

## Out of scope
SSR-28 tallinn seed + `test_tallinn_loads_taxonomy_when_manifest_declares_schema`.
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
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_26_*.py -k "missing or invalid or duplicate or legal or mobility"
```
