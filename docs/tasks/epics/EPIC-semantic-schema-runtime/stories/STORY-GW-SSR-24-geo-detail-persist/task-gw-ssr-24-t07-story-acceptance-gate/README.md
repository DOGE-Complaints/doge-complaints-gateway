# task-gw-ssr-24-t07-story-acceptance-gate

## Task: analyze — story acceptance + G24

## Meta
- **Story:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist.md)
- **Type:** gate
- **Status:** 🔵 Done · P4 PASS 2026-08-30T21:07:09Z
- **Package:** pkg-000081
- **Skill declared:** python-pro
- **Depends on:** T01–T06 Done
- **Scaffolded:** 2026-08-30T20:55:32Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md` Target / AC + runbook §6.3

## Purpose
Story acceptance + G24. Commands from runbook §6.3 **verbatim**. PASS: round-trip street/range/houses/coords; new cols не в `required_columns_ready`; migration на диске; полный offline pytest зелёный; ClusterLens=10. After PASS: INDEX/dashboard Status for SSR-24; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-25/06/07/12.

## Code Facts
1. Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
2. Story AC — [`STORY-GW-SSR-24-geo-detail-persist.md`](../STORY-GW-SSR-24-geo-detail-persist.md) §Target / AC
3. G24 commands — [`orchestrator-geo-detail-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md) §6.3
4. `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-24.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-24-t07.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G24: `test_gw_ssr_24_*` + cross-layer + **full** offline pytest; omit-probe; migration on disk; ClusterLens=10
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-25/06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-24.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3)

## Out of scope
- Implementing missing product gaps; start SSR-25/06/07/12
- Overlay bans (every task):
  - StoryGeoSnapshot depth; sqlite/supabase; migration; omit-probe; mirror; lifecycle preserve.
  - Tests `test_gw_ssr_24_*`. G24 = **full** offline pytest (`-m "not live_integration"`) + `test_stories_schema_cross_layer_invariant.py`.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет IDX / QRY / `story_dimensions`. Нет GPT UI.
  - Не dump raw `geo_detail` в public Issue card.
  - Новые geo cols **не** в `required_columns_ready` (omit-probe как `geo_admin_*`).
  - Не drop `geo_admin_*`. Civic `geo_filter_bucket` (admin_*) stays.
  - Hosted apply migration = operator proof как SSR-09 (артефакт на диске обязателен; не live_integration).
  - **Нет SSR-06/07/12.** Не reopen 01–23 product. Не стартовать 25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
# P3 only (G24) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_24_*.py
python3 -m pytest -q -m "not live_integration" tests/test_stories_schema_cross_layer_invariant.py
python3 -m pytest -q -m "not live_integration"
rg -n "required_columns_ready" -A 20 src/core/infrastructure/db_supabase.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
ls supabase/migrations/*geo* 2>/dev/null || ls supabase/migrations/ | tail -5
```
