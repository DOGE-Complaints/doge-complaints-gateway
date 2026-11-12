# task-gw-ssr-08-t06-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-SSR-08](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000066
- **Skill declared:** python-pro
- **Depends on:** T00–T05 Done
- **Scaffolded:** 2026-08-29T17:47:38Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md` T06 + Target / AC

## Purpose
Story acceptance + G8. Pack load + membership; civic path intact; нет нового HTTP / `story_dimensions`. SSR-06/07/12 not in DoD. G8 commands from runbook. After PASS: INDEX/dashboard Status for SSR-08; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-09 in this pkg.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-08-….md`](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md) §Target / AC (verbatim)
- G8 commands — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.1
- Gate **Date:** only after `--print-utc-now` post live pytest + `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no) — **not** `gateway-mvp-dashboard.md`

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-08.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-08-t06.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G8: pytest `test_gw_ssr_08_*` + civic clustering; `rg ClusterLens`; `test -f schema-packs/tallinn_civic/v1/pack.json`; `rg story_dimensions|/schema-filter`
- [x] Live verify commands + `--project gateway --verify` recorded
- **Date:** 2026-08-29T17:52:54Z
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/09/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-08.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold. No product code.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-09
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22). 10 members stay.
  - Не править `lens_dimension` под pack (`engine.py` :66–79). Pack **не** via civic `lens_dimension`.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / новый intake path / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать / не ставить в очередь SSR-06/07/12.
  - `build_index` / `project` — stub/no-op (`runtime.py` :62–72).
  - Не переименовывать `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0*`.
  - Civic path без binding **must stay**.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не новый Python engine; не прогонять bound story через civic engine (dual → SSR-10).
  - Pack cluster_id namespace `schema:…`; civic `_persist_memberships` / `_create_issue_for_cluster` as-is не для pack.

## Verification commands
```bash
# P3 only (G8):
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_08_*.py
.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_clustering_engine.py tests/test_gw_tax_02_cluster_axis_expansion.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
test -f schema-packs/tallinn_civic/v1/pack.json
rg -n "story_dimensions|/schema-filter|generic.filter" src/core/api/asgi_app.py
```
