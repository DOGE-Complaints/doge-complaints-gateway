# task-gw-ssr-13-t05-sibling-req-node-paths

## Task: docs — spa-16 + REQ-51 sibling `/node/issues` (T05)

## Meta
- **Story:** [STORY-GW-SSR-13](../STORY-GW-SSR-13-abstract-node-public-api.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000069
- **Skill declared:** python-pro
- **Depends on:** T01 / T04 canon path
- **Scaffolded:** 2026-08-29T18:50:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md` T05

## Purpose
Patch spa-16 «Keep `GET /tallinn/issues`» → `GET /node/issues`; patch REQ-51 sibling row/table to `/node/issues`.

## Code Facts
- spa-16 stale — [`16-semantic-schema-spa-compatibility.md:24`](../../../../../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md) «Keep `GET /tallinn/issues`»; [`:5`](../../../../../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md) sibling contract city; [`:43`](../../../../../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md) `GET {base}/tallinn/issues`
- REQ-51 sibling — [`51-semantic-schema-runtime.md:5`](../../../../../../requirements/51-semantic-schema-runtime.md) `GET /tallinn/issues` remains; [`:59`](../../../../../../requirements/51-semantic-schema-runtime.md) `asgi_app.py:462`
- G13 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.4

## Acceptance / DoD
- [x] spa-16 и REQ-51 sibling называют `/node/issues`, не город
- [x] spa-16 does not say «Keep `GET /tallinn/issues`»
- [x] BULLRUN phases complete

## Where to change
- `spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md` (`:5`, `:24`, `:43`)
- `doge-complaints-gateway/docs/requirements/51-semantic-schema-runtime.md` (`:5`, `:59`)

## Out of scope
- REQ-45 GPT; invent overlay field names; rewrite T-wave G3
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

## Verification commands
```bash
rg -n "GET /node/issues|/tallinn/issues" \
  spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md \
  doge-complaints-gateway/docs/requirements/51-semantic-schema-runtime.md
```
