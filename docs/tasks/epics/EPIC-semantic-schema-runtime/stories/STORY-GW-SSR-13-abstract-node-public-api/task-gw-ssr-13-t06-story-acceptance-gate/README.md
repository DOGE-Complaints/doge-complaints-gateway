# task-gw-ssr-13-t06-story-acceptance-gate

## Task: analyze — story acceptance + G13

## Meta
- **Story:** [STORY-GW-SSR-13](../STORY-GW-SSR-13-abstract-node-public-api.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000069
- **Skill declared:** python-pro
- **Depends on:** T01–T05 Done
- **Scaffolded:** 2026-08-29T18:50:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md` Target / AC + runbook §6.4
- **Gate Date:** 2026-08-29T18:55:15Z

## Purpose
Story acceptance + G13. Commands from runbook §6.4. After PASS: INDEX/dashboard Status for SSR-13; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-11/14/15 in this pkg. **Do not HALT** on red `test_req24_*` / `test_gw_ssr_05_*` `@app.get("/tallinn/issues")` (→ G15).

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-13-….md`](../STORY-GW-SSR-13-abstract-node-public-api.md) §Target / AC (verbatim)
- G13 commands — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.4
- Gate **Date:** only after `--print-utc-now` post live `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-13.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-13-t06.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G13: `/tallinn/` empty in `src/core/api`; five `/node/…` families in asgi + `PUBLIC_ROUTES`; three SPA repos without `/tallinn/` in URL; spa-16 = `GET /node/issues`; no alias
- [x] Red gateway pytest on old `/tallinn/` path **allowed** until G15 — do not HALT for `test_req24_*` / `test_gw_ssr_05_*`
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/11/12/14/15.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-13.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-11/14/15
- INDEX/runbook §8 + fence hard bans:
  - **Hard cut `/tallinn/*` — NO alias.** Do not keep both prefixes.
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`.
  - Не расширять `ClusterLens` (`types.py` :10–22).
  - `CLUSTER_GEO_SCOPE=settlement:tallinn` и pack id `tallinn_civic` **stay**.
  - Overlay UI spa-app — **not this story** (SSR-11).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/11/12/14/15. Не reopen 01–05/08–10.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Полный pytest URL / rename `test_req24_*` — **SSR-15 / G15**, не G13 HALT.
  - Не коммитить spa-app nested git без явной команды (P8 skip spa git).
  - Полный API_REFERENCE / manuals — SSR-14.
  - REQ-45 GPT — out.

## Verification commands
```bash
# P3 only (G13) — from workspace root:
rg -n "/tallinn/" doge-complaints-gateway/src/core/api
rg -n "/node/issues|/node/network-pulse|/node/emerging-signals" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "/tallinn/" spa-app/src/repositories/GatewayIssueRepository.js spa-app/src/repositories/GatewayNetworkPulseRepository.js spa-app/src/repositories/GatewayEmergingSignalsRepository.js
rg -n "GET /node/issues|/tallinn/issues" spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md
# Do not HALT G13 if test_req24_* / test_gw_ssr_05_* still assert @app.get("/tallinn/issues")
```
