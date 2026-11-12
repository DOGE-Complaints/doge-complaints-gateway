# task-gw-ssr-11-t00-pack-card-fields-contract

## Task: implement — pack card-fields key + wire shape (R1)

## Meta
- **Story:** [STORY-GW-SSR-11](../STORY-GW-SSR-11-pack-declared-issue-projection.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000070
- **Skill declared:** python-pro
- **Depends on:** SSR-05 Done; SSR-13 Done (G13 PASS; `GET /node/issues`)
- **Scaffolded:** 2026-08-29T19:08:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-11-pack-declared-issue-projection.md` R1

## Purpose
Fix loader key name + JSON shape on `GET /node/issues` (named fields or named sidecar, **не** dump). Document key in `schema-packs/README.md` (SCHEMA-005 this-loader-only, like `dual_civic_lenses`). Refine nested object vs flat keys. Do not invent SPA overlay names. Do not break REQ-09 `type`/`status`. G11: Pack MAY declare card fields; absent = civic form.

## Code Facts
- Loader keys no card allowlist — [`schema-packs/README.md:20–28`](../../../../../../../schema-packs/README.md)
- `SchemaContext` — [`contracts.py:52–59`](../../../../../../../src/core/schema/contracts.py) no card allowlist attr
- Loader `load_pack` — [`resolver.py:73–117`](../../../../../../../src/core/schema/resolver.py) parses `field_policy` + `dual_civic_lenses` only
- Public read — [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py) `GET /node/issues`
- G11 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.5

## Acceptance / DoD
- [x] Pack MAY объявить card fields; absent = текущая civic-форма карточки
- [x] Key name documented in `schema-packs/README.md` after refine (not frozen dialect)
- [x] Wire shape on `GET /node/issues` is named (or named sidecar), не dump `structured_payload`
- [x] REQ-09 `type`/`status` enums not broken
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/README.md` (loader table)
- `doge-complaints-gateway/src/core/schema/contracts.py` (`SchemaContext` field; name from this refine)

## Out of scope
- Invent SPA routes; dump payload; implement `SchemaRuntime.project`; overlay UI
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
rg -n "card.field|card_fields|allowlist" doge-complaints-gateway/schema-packs/README.md \
  doge-complaints-gateway/src/core/schema/contracts.py || true
rg -n "GET /node/issues" doge-complaints-gateway/src/core/api/asgi_app.py
```
