# task-gw-ssr-11-t04-story-acceptance-gate

## Task: analyze — story acceptance + G11

## Meta
- **Story:** [STORY-GW-SSR-11](../STORY-GW-SSR-11-pack-declared-issue-projection.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000070
- **Skill declared:** python-pro
- **Depends on:** T00–T03 Done
- **Scaffolded:** 2026-08-29T19:08:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-11-pack-declared-issue-projection.md` Target / AC + runbook §6.5
- **Gate Date:** 2026-08-29T19:13:51Z

## Purpose
Story acceptance + G11. Commands from runbook §6.5. After PASS: INDEX/dashboard Status for SSR-11; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-14/15 in this pkg.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-11-….md`](../STORY-GW-SSR-11-pack-declared-issue-projection.md) §Target / AC (verbatim)
- G11 commands — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.5
- Gate **Date:** only after `--print-utc-now` post live `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-11.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-11-t04.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G11: public dict **не** содержит целиком `structured_payload`; civic Issues без новых required keys; path канон `/node/issues`; factory civic default на месте; spa overlay UI не в diff
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/12/14/15.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-11.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-14/15
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`. `GET /node/issues` stays (`asgi_app.py:462`).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12/14/15. Не reopen 01–05/08–10/13.
  - Не вызывать / не реализовывать `SchemaRuntime.project` (stub `runtime.py:68–72` stays `NotImplementedError`).
  - Не dump `structured_payload` на карточку; не проецировать `forbidden` / `node_private`.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
# P3 only (G11) — from workspace / gateway:
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_11_*.py
rg -n "structured_payload" src/core/projection/dto.py
rg -n "/node/issues" src/core/api/asgi_app.py
rg -n "require_actionable_canonical_type: bool = True" src/core/promotion/gates.py
```
