# task-gw-ssr-27-t07-story-acceptance-gate

## Task: analyze — story acceptance + G27 (T07)

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084
- **Skill declared:** python-pro
- **Depends on:** T00–T06 Done
- **Scaffolded:** 2026-09-01T13:12:45Z
- **Completed:** 2026-09-01T13:21:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`

## Purpose
Story acceptance gate. PASS iff AC-GW-SSR27-01…06: README; loader optional; detail_level wire→Issue.geo; instance rule types; SSR-22 regression; GPT-SSR-08 pack blocks available for copy. ClusterLens=10; no HTTP geo-filter.

## Code Facts
- Template — story-acceptance-gate-template.md
- Story AC — backlog SSR-27 §Target / AC
- SSR-22 tests — `tests/test_gw_ssr_22_*`

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-27.md` PASS/FAIL + evidence (P3)
- [x] `acceptance-verification-gw-ssr-27-t07.md` signed (Date post P3)
- [x] AC-GW-SSR27-01…06 covered
- [x] Live `--project gateway --verify` recorded
- [x] Do **not** rewrite §«Актуальная точка»; do not start 28/29
- [x] BULLRUN phases complete

## Where to change
- This folder gate artifacts (P3)

## Out of scope
P3 product gaps invent; start SSR-28/29
- Overlay bans (every task):
  - **No ClusterLens** add/remove. Enum stays 10 (`types.py:10–22`).
  - Civic `geo_filter_bucket` stays `admin_*` only.
  - **Do not** merge node `geo_scope` with `gpt_instance_territory` semantics.
  - **No** invent HTTP geo-filter / `GET /schema-active` / IDX / `story_dimensions`.
  - **No** street/house on Issue projection (REQ-51 §3).
  - **No** invented coords `(0.0,0.0)` for address-only (SSR-24 rule).
  - SSR-24 migration test keeps SSR-24-only column set — split `geo_detail_level` assertions.
  - Tallinn instance seed Option A omit / Option B demo settlement tallinn — **OP at P3**; no invent district/bbox.
  - **Нет GPT UI** materialize here. Parallel-safe vs taxonomy 26/28/29.
  - **Нет SSR-06/07/12.** Не reopen 01–26 product. Не стартовать 28/29 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
cd doge-complaints-gateway
.venv/bin/python -m pytest -q tests/test_gw_ssr_27_*.py tests/test_gw_ssr_22_*.py
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
