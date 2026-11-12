# task-gw-ssr-25-t05-story-acceptance-gate

## Task: analyze — story acceptance + G25

## Meta
- **Story:** [STORY-GW-SSR-25](../STORY-GW-SSR-25-geo-detail-clustering-docs.md)
- **Type:** gate
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:31:59Z
- **Package:** pkg-000082
- **Skill declared:** python-pro
- **Depends on:** T01–T04 Done
- **Scaffolded:** 2026-08-30T21:20:50Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-25-geo-detail-clustering-docs.md` Target / AC + runbook §6.4

## Purpose
Story acceptance + G25. Commands from runbook §6.4 **verbatim**. PASS: civic clustering зелёный; pack membership по `geo.*`; мануал modes / mirror / два пути; T-wave G3 на месте; offline suite зелёный; ClusterLens=10. After PASS: INDEX/dashboard Status for SSR-25; pie T-wave **no**; **стоп волны**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-06/07/12/26.

## Code Facts
1. **As-of-Done (SSR-25 pkg-000082):** G25 PASS 2026-08-30T21:27:05Z — [`story-acceptance-gate-STORY-GW-SSR-25.md`](./story-acceptance-gate-STORY-GW-SSR-25.md); [`run-summary-20260830-2127-gw-ssr-25-p3.md`](../../../../../../run-reports/run-summary-20260830-2127-gw-ssr-25-p3.md).
2. Story AC — [`STORY-GW-SSR-25-geo-detail-clustering-docs.md`](../STORY-GW-SSR-25-geo-detail-clustering-docs.md) §Target / AC
3. G25 commands — [`orchestrator-geo-detail-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md) §6.4
4. `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-25.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-25-t05.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G25: `test_gw_ssr_25_*` + `test_clustering_engine.py` + **full** offline pytest; docs; ClusterLens=10
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/12/26.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-25.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3)

## Out of scope
- Implementing missing product gaps; start SSR-06/07/12/26
- Overlay bans (every task):
  - Civic/pack cluster regression; manuals `geo_intake`; README/matrix; tests `test_gw_ssr_25_*`.
  - G25 = **full** offline pytest (`-m "not live_integration"`) + `test_clustering_engine.py` + `test_gw_ssr_25_*`.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет invent HTTP geo-filter API. Нет IDX / QRY / `story_dimensions`. Нет GPT UI / instruction pack. Нет SPA map overlay.
  - Civic `geo_filter_bucket` остаётся `admin_*`. Не dual-source env+pack для geo knobs (D-SSR-9).
  - **Нет SSR-06/07/12.** Не reopen 01–24 product. Не стартовать 26.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
# P3 only (G25) — from workspace root:
python3 -m pytest -q -m "not live_integration" doge-complaints-gateway/tests/test_gw_ssr_25_*.py
python3 -m pytest -q -m "not live_integration" doge-complaints-gateway/tests/test_clustering_engine.py
python3 -m pytest -q -m "not live_integration" doge-complaints-gateway
rg -n "geo_intake|geo_detail" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "GET /tallinn/issues stays" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
rg -n "class ClusterLens" -A 14 doge-complaints-gateway/src/core/cluster/types.py
```
