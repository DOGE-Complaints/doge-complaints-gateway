# task-gw-ssr-11-t02-project-pack-issue-fields

## Task: implement — pack Issue named projection (T02)

## Meta
- **Story:** [STORY-GW-SSR-11](../STORY-GW-SSR-11-pack-declared-issue-projection.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000070
- **Skill declared:** python-pro
- **Depends on:** T00–T01
- **Scaffolded:** 2026-08-29T19:08:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-11-pack-declared-issue-projection.md` T02

## Purpose
Pack-promoted Issue: only allowlist leafs (or named sidecar). Filter `forbidden` / `node_private` even if listed. Civic `DOGEIssue` / `to_public_dict` — no new required keys. Public path remains `GET /node/issues`. Do **not** implement `SchemaRuntime.project`.

## Code Facts
- Public card — [`dto.py:26–50`](../../../../../../../src/core/projection/dto.py) `to_public_dict` no `structured_payload`
- Projection input civic-only — [`input.py:8–31`](../../../../../../../src/core/projection/input.py)
- `field_policy` — [`field_policy.py:19–32`](../../../../../../../src/core/schema/field_policy.py) `forbidden` raises; `node_private` in-process only
- Issue create — [`issue_create.py:252,307,333,399`](../../../../../../../src/core/application/issue_create.py) `to_public_dict()`
- `project` stub — [`runtime.py:68–72`](../../../../../../../src/core/schema/runtime.py) `NotImplementedError` — **do not implement**
- Public read — [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py) `GET /node/issues`

## Acceptance / DoD
- [x] Public Issue **не** содержит целиком `structured_payload`
- [x] `forbidden` / `node_private` не утекают even if listed in allowlist
- [x] Civic Issues без новых required keys; civic form unchanged when no binding / no key
- [x] Public read path = `GET /node/issues`, не `/tallinn/issues`
- [x] `SchemaRuntime.project` stays `NotImplementedError`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/projection/dto.py` (`:26–50`)
- `doge-complaints-gateway/src/core/projection/input.py` (`:8–31`) as needed
- `doge-complaints-gateway/src/core/application/issue_create.py` `to_public_dict()` call sites
- **Not** `src/core/schema/runtime.py:68–72`

## Out of scope
- Менять civic extraction_policy as-is для всех; implement `SchemaRuntime.project`; overlay UI; new civic required keys
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
rg -n "structured_payload" doge-complaints-gateway/src/core/projection/dto.py
rg -n "NotImplementedError" doge-complaints-gateway/src/core/schema/runtime.py
rg -n "GET /node/issues" doge-complaints-gateway/src/core/api/asgi_app.py
```
