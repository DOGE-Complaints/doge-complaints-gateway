# task-gw-ssr-10-t04-story-acceptance-gate

## Task: analyze — story acceptance + G10

## Meta
- **Story:** [STORY-GW-SSR-10](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000068
- **Skill declared:** python-pro
- **Depends on:** T00–T03 Done
- **Scaffolded:** 2026-08-29T18:25:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md` Target / AC + runbook §6.3
- **Gate Date:** 2026-08-29T18:31:19Z

## Purpose
Story acceptance + G10. Commands from runbook §6.3. After PASS: INDEX/dashboard Status for SSR-10; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-11/13 in this pkg.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-10-….md`](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md) §Target / AC (verbatim)
- G10 commands — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.3
- Gate **Date:** only after `--print-utc-now` post live `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [ ] `story-acceptance-gate-STORY-GW-SSR-10.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [ ] `acceptance-verification-gw-ssr-10-t04.md` signed (Date post P3 verify only)
- [ ] All story Target / AC covered
- [ ] G10: dual fixture civic lens + pack `lens_id`; pack without dual key = exact-only; civic unbound green; `ClusterLens`=10; no new HTTP
- [ ] Live `--project gateway --verify` recorded
- [ ] BULLRUN phases complete
- [ ] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/11/12/13.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-10.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-11/13
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79) как default для всех packs.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/11/12/13. Не reopen 01–05/08/09.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
# P3 only (G10):
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_10_*.py
.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_clustering_engine.py tests/test_gw_ssr_04_*.py tests/test_gw_ssr_05_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "POLICE_STATION|police_station" src/core/cluster/types.py src/core/cluster/engine.py
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
```
