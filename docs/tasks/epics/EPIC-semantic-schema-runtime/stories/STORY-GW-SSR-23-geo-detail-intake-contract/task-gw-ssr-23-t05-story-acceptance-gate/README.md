# task-gw-ssr-23-t05-story-acceptance-gate

## Task: analyze — story acceptance + G23

## Meta
- **Story:** [STORY-GW-SSR-23](../STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Type:** gate
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:44:21Z
- **Package:** pkg-000080
- **Skill declared:** python-pro
- **Depends on:** T00–T04 Done
- **Scaffolded:** 2026-08-30T20:29:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md` Target / AC + runbook §6.2

## Purpose
Story acceptance + G23. Commands from runbook §6.2 **verbatim**. PASS: accept detail; invalid/require miss → 4xx; optional omit → 202; packs с `geo_intake`; ClusterLens=10. After PASS: INDEX/dashboard Status for SSR-23; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-24/06/07/12.

## Code Facts
1. Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
2. Story AC — [`STORY-GW-SSR-23-geo-detail-intake-contract.md`](../STORY-GW-SSR-23-geo-detail-intake-contract.md) §Target / AC
3. G23 commands — [`orchestrator-geo-detail-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md) §6.2
4. `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-23.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-23-t05.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G23: pytest 23; packs `geo_intake`; ClusterLens=10
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-24/06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-23.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3)

## Out of scope
- Implementing missing product gaps; start SSR-24/06/07/12
- Overlay bans (every task):
  - Parse `geo_detail`; pack `geo_intake`; three packs; tests `test_gw_ssr_23_*`.
  - **No SQL migration** (→24). Do not add street/houses columns this pkg.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет IDX / QRY. Нет GPT UI.
  - **No global require-geo** without pack `geo_intake`.
  - Не dump raw `geo_detail` в public Issue card.
  - Не класть новые geo cols в `required_columns_ready`.
  - **Нет SSR-06/07/12.** Не reopen 01–22 product. Не стартовать 24…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.
  - Не invent второй binding; sidecar class = `gpt_signals` (root, рядом с `schema_binding`).
  - Не drop `location_query`. Scope gate SSR-22 остаётся.

## Verification commands
```bash
# P3 only (G23) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_23_*.py
rg -n "geo_intake|geo_detail" schema-packs/README.md src/core/
rg -n "geo_intake" schema-packs/tallinn_civic/v1/pack.json schema-packs/legal_process/v1/pack.json schema-packs/mobility_observation/v1/pack.json
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```
