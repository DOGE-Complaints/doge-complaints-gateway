# task-gw-ssr-13-t03-openapi-node-paths

## Task: docs — OpenAPI `/node/…` paths (T03)

## Meta
- **Story:** [STORY-GW-SSR-13](../STORY-GW-SSR-13-abstract-node-public-api.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000069
- **Skill declared:** python-pro
- **Depends on:** T01 canon paths
- **Scaffolded:** 2026-08-29T18:50:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md` T03

## Purpose
Paths `/node/…` in `openapi.yaml` for the five families. Minimum path rewrite only. Full manuals / `API_REFERENCE.md` → SSR-14.

## Code Facts
- OpenAPI city paths — [`openapi.yaml:1008`](../../../../../../runtime-docs/api-reference/openapi.yaml) `/tallinn/network-pulse`; [`:1071`](../../../../../../runtime-docs/api-reference/openapi.yaml) emerging; [`:1126`](../../../../../../runtime-docs/api-reference/openapi.yaml) issues; [`:1301`](../../../../../../runtime-docs/api-reference/openapi.yaml) `{issue_id}`
- Description still names city — [`openapi.yaml:287`](../../../../../../runtime-docs/api-reference/openapi.yaml) `GET /tallinn/issues`
- G13 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.4

## Acceptance / DoD
- [x] OpenAPI paths for `GET/POST /node/issues`, `GET /node/issues/{issue_id}`, `GET /node/network-pulse`, `GET /node/emerging-signals`
- [x] Related descriptions in this file that name `/tallinn/` for those five families updated to `/node/`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml` (`:1008`, `:1071`, `:1126`, `:1301` and related descriptions)

## Out of scope
- Полный проход manuals / `API_REFERENCE.md` (→ SSR-14)
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
  - REQ-45 GPT — out.

## Verification commands
```bash
rg -n "/tallinn/|/node/" doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml
```
