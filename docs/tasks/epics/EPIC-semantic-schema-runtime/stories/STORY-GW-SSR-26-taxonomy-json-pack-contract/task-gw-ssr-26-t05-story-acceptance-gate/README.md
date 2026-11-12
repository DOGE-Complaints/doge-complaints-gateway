# task-gw-ssr-26-t05-story-acceptance-gate

## Task: analyze — story acceptance + G26 (T05)

## Meta
- **Story:** [STORY-GW-SSR-26](../STORY-GW-SSR-26-taxonomy-json-pack-contract.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000083
- **Skill declared:** python-pro
- **Depends on:** T00–T04 Done
- **Scaffolded:** 2026-09-01T12:55:39Z
- **Completed:** 2026-09-01T13:00:37Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md`

## Purpose
Story acceptance gate. PASS iff AC-GW-SSR26-01…05 + story T05 checklist: `pytest tests/test_gw_ssr_26_* -q` green; `pytest tests/test_gw_ssr_01_* tests/test_gw_ssr_11_* -q` regression green; no edits to `cluster/vocabulary.py`, wire `parse_taxonomy_payload`, `ClusterLens`; live `--project gateway --verify` PASS. Sync INDEX/dashboard Status on PASS (P3) — not this P1 scaffold.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — backlog SSR-26 §Target / AC + §T05
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-26.md` with AC checklist PASS/FAIL + evidence paths (P3)
- [x] `acceptance-verification-gw-ssr-26-t05.md` signed (Date post P3 verify only)
- [x] AC-GW-SSR26-01…05 covered
- [x] G26 commands green; ClusterLens=10; no wire/vocab edits
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; do not start 27/28/29

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-26.md` (P3)
- Sync SSR INDEX / dashboard on PASS (P3) — not this P1 scaffold

## Out of scope
Implementing missing product gaps; P3 execution; start SSR-27/28/29/06/07/12
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
# P3 only (G26) — from doge-complaints-gateway:
python3 -m pytest -q tests/test_gw_ssr_26_*.py
python3 -m pytest -q tests/test_gw_ssr_01_*.py tests/test_gw_ssr_11_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
# from workspace root:
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
