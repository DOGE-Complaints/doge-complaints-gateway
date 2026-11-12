# task-gw-ssr-13-t04-spa-gateway-url-clients

## Task: implement — three Gateway*Repository URLs + tests (T04)

## Meta
- **Story:** [STORY-GW-SSR-13](../STORY-GW-SSR-13-abstract-node-public-api.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000069
- **Skill declared:** python-pro
- **Depends on:** T01 canon `/node/*`
- **Scaffolded:** 2026-08-29T18:50:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md` T04

## Purpose
Three repositories + unit/contract tests fetch `/node/…`. No overlay card fields. No form builder. spa nested git: **no commit this pkg** (P8 skip spa git unless operator later commands).

## Code Facts
- SPA Issue — [`GatewayIssueRepository.js:77–85`](../../../../../../../../spa-app/src/repositories/GatewayIssueRepository.js) `/tallinn/issues`
- SPA Pulse — [`GatewayNetworkPulseRepository.js:24`](../../../../../../../../spa-app/src/repositories/GatewayNetworkPulseRepository.js) `/tallinn/network-pulse`
- SPA Emerging — [`GatewayEmergingSignalsRepository.js:32`](../../../../../../../../spa-app/src/repositories/GatewayEmergingSignalsRepository.js) `/tallinn/emerging-signals`
- SPA tests city URLs — `GatewayIssueRepository.test.js`; `GatewayNetworkPulseRepository.test.js`; `GatewayEmergingSignalsRepository.test.js`; [`GatewayIssueRepository.contract.test.js:17`](../../../../../../../../spa-app/src/repositories/__tests__/GatewayIssueRepository.contract.test.js)
- G13 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.4

## Acceptance / DoD
- [x] SPA три репозитория бьют в `/node/…`
- [x] Matching `__tests__` + contract test fetch `/node/` (not `/tallinn/`)
- [x] BULLRUN phases complete

## Where to change
- `spa-app/src/repositories/GatewayIssueRepository.js` (`:77–85`)
- `spa-app/src/repositories/GatewayNetworkPulseRepository.js` (`:24`)
- `spa-app/src/repositories/GatewayEmergingSignalsRepository.js` (`:32`)
- matching `__tests__` + `GatewayIssueRepository.contract.test.js`

## Out of scope
- Overlay UI; form builder; spa nested git commit; spa-15 full rewrite (T05 = spa-16 + REQ-51 only)
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
rg -n "/tallinn/" \
  spa-app/src/repositories/GatewayIssueRepository.js \
  spa-app/src/repositories/GatewayNetworkPulseRepository.js \
  spa-app/src/repositories/GatewayEmergingSignalsRepository.js
rg -n "/node/" \
  spa-app/src/repositories/GatewayIssueRepository.js \
  spa-app/src/repositories/GatewayNetworkPulseRepository.js \
  spa-app/src/repositories/GatewayEmergingSignalsRepository.js \
  spa-app/src/repositories/__tests__
```
